
from datetime import datetime 
from config import ACTUATER_TYPE, CAMRA_PRO, CLOUD_COST_UNIT_TIME, CLOUD_CPU_SPEED, CPU_SPEED1, CPU_SPEED2, CPU_SPEED3, DATA_SIZE1, DATA_SIZE2, DATA_SIZE3, DATA_SIZE4, FD_BANDWIDTH1, FD_BANDWIDTH2, FD_BANDWIDTH3,  FD_CAPACITY1, FD_CAPACITY2, FD_CAPACITY3, FD_RAM1, FD_RAM2, FD_RAM3, GPSPOS_PRO, INDLOOP_PRO, INTERVEL_GAP, LATENCY_CS_FR, LATENCY_ED_FR, MAX_SIMULATION_TIME, MICWAVE_PRO, NO_INSTRUCTIONS1, NO_INSTRUCTIONS2, NO_INSTRUCTIONS3, NO_INSTRUCTIONS4, RAM_SWAP_UNIT, ROAD_DISPLAY, SENSER_TYPE, SLOT_TIME
import random

g_jobserno = 0
g_taskid = 0
g_devid = 0

resource_mg_string  = ['DEFAULT_RM' ,'GA_RM','AI_RM' ]
# class STATE:
#     def __init__(self):
#         self.no_fognodes = 0.
#         self.no_jobs= 0

taskType_strings = ['CAMRA_SEN','GPSPOS_SEN','INDLOOP_SEN','MICWAVE_SEN','CONT_DISPLAY','ROAD_DISPLAY','CAMRA_PRO',
                    'INDLOOP_PRO' ,'GPSPOS_PRO','MICWAVE_PRO','CAMRA_STORE','INDLOOP_STORE','GPSPOS_STORE','MICWAVE_STORE']

class DeviceTime:
    def __init__(self):
        self.tm = 0.
    def set_time(self, tm):
        self.tm = tm
    def add_time(self,tm):
        self.tm += tm
    def get_time(self):
        return self.tm
    
class DeviceJobQ:
    def __init__(self):
        self.tq = []
    def add_t(self, tsk):
        self.tq.append(self,tsk)
    def next_t( self):
        tsk = self.tq.pop()
        return tsk

class TimeTrackerJb:
    def __init__(self):
        self.maxTimetakenbyJob = 0.
        self.minTimetakenbyJob= 1000.
        self.sumTimetakenbyJob= 0.
        self.no_jobs=0

    def RecordTimeDetails(self,jb):
        if (jb.comp_tmstamp > self.maxTimetakenbyJob):
            self.maxTimetakenbyJob = jb.comp_tmstamp
        if (jb.comp_tmstamp < self.minTimetakenbyJob):
            self.minTimetakenbyJob = jb.comp_tmstamp
        self.sumTimetakenbyJob = self.sumTimetakenbyJob + jb.comp_tmstamp
        self.no_jobs+=1

    def PrintTimeDetails(self,strng = 'Jobs:'):
        avgTimetakenbyJob = self.sumTimetakenbyJob /self.no_jobs
        imd = (self.maxTimetakenbyJob - self.minTimetakenbyJob) / avgTimetakenbyJob
        print("Total Number of Jobs:" + str(self.no_jobs ))
        print()
        print("max Timetaken for "+strng + str(self.maxTimetakenbyJob ))
        print("min Timetaken for "+strng + str(self.minTimetakenbyJob ))
        print("avg TimeTaken for "+strng + str(avgTimetakenbyJob ))

class TimeTrackerTsk:
    def __init__(self):
        self.maxTimetakenbyTsk = 0.
        self.minTimetakenbyTsk= 1000.
        self.sumTimetakenbyTsk= 0.
        self.no_tasks=0

    def RecordTimeDetails(self,tsk):
        if (tsk.time_taken > self.maxTimetakenbyTsk):
            self.maxTimetakenbyTsk = tsk.time_taken
        if (tsk.time_taken < self.minTimetakenbyTsk):
            self.minTimetakenbyTsk = tsk.time_taken
        self.sumTimetakenbyTsk = self.sumTimetakenbyTsk + tsk.time_taken
        self.no_tasks+=1

    def PrintTimeDetails(self,strng = 'Tasks:'):
        avgTimetakenbyTsks = self.sumTimetakenbyTsk /self.no_tasks
        imd = (self.maxTimetakenbyTsk - self.minTimetakenbyTsk) / avgTimetakenbyTsks
        print("Total Number of "+strng + str(self.no_tasks ))
        print()
        print("max Timetaken for "+strng + str(self.maxTimetakenbyTsk ))
        print("min Timetaken for "+strng + str(self.minTimetakenbyTsk ))
        print("avg TimeTaken for "+strng + str(avgTimetakenbyTsks ))

class Task:
    #jobid, task type,source device,slot
    def  __init__(self,jbid,tsktype, sr,slotno):
        #job id tells for which job this task belongs to
        global g_taskid
        g_taskid +=1
        self.id = g_taskid
        
        self.job_id =jbid
        self.task_type = tsktype
        self.slot_no = slotno

        self.fd_devid = 0
        self.sensor_id = sr # source or creater device id

        self.duration = 0.
        self.delay = 0
        self.sb_timestamp = 0.
        self.time_taken = 0.
        
        self.destId = 0 #executer Id
        self.dataBytes = 0
        
        match tsktype:
            case 1:
                self.no_instructions = NO_INSTRUCTIONS1
                self.dataBytes = DATA_SIZE1
            case 2:
                self.no_instructions = NO_INSTRUCTIONS2
                self.dataBytes = DATA_SIZE2
            case 3:
                self.no_instructions = NO_INSTRUCTIONS3
                self.dataBytes = DATA_SIZE3
            case 4:
                self.no_instructions = NO_INSTRUCTIONS4
                self.dataBytes = DATA_SIZE4
            case 5:
                self.no_instructions = 0
                self.dataBytes = 0
            case 6:
                self.no_instructions = 0
                self.dataBytes = 0
            case 7:
                self.no_instructions = NO_INSTRUCTIONS1
                self.dataBytes = DATA_SIZE1
            case 8:
                self.no_instructions = NO_INSTRUCTIONS2
                self.dataBytes = DATA_SIZE2
            case 9:
                self.no_instructions = NO_INSTRUCTIONS3
                self.dataBytes = DATA_SIZE3
            case 10:
                self.no_instructions = NO_INSTRUCTIONS4
                self.dataBytes = DATA_SIZE4
            case _:
                self.no_instructions = 0
                self.dataBytes = 0
    def get_noInstructions(self):
        return self.no_instructions
    def get_dataBytes(self):
        return self.dataBytes
    def get_tasktype(self):
        return self.task_type-1
    def get_devid(self):
        return self.sensor_id
    
    def writeDetails(self):
        global logentry
        self.time_taken = self.duration + self.delay
        strVal ='slot Id:'+ str(self.slot_no) + ' TaskId:'+ str(self.id)+' JobId:'+str(self.job_id)+' CreaterId:'+str(self.sensor_id) + ' ClusterId:'+str(self.destId)+' submited at:'+ str(self.sb_timestamp) + ' time taken:' + str(self.time_taken) + '\n'
        logentry.writeTaskDetails(strVal)

    def writeDataset(self):
        logentry.writeToDataset(str(self.task_type-1) +', '+ str(self.no_instructions) +', '+str(self.dataBytes) +', ' )

    def setSlotNo(self, sn):
        self.slot_no = sn

    def setSubmitime(self, sim_time):
        self.sb_timestamp = sim_time
        
    def setExecutionstarttime(self, delay):
            self.ex_timestamp = self.sb_timestamp+ delay
            self.delay = delay

    def setExecutionduration(self , d):
        self.duration = d
        
    def get_timetaken(self):
        return self.time_taken
    
class Job:
    #senserId, clusterId, senser type, timestamp,slot no
    def  __init__(self, src, fd, sensertype, tm, slot_no):
        global g_jobserno
        g_jobserno +=1
        self.id = g_jobserno

        self.sorceSenser = src
        self.fd_devid = fd
        self.sensertype = sensertype
        
        #present slot
        self.slot_no = slot_no
        #created slot
        self.slot_noCr = slot_no
        #completed slot
        self.slot_noFi = 0

        #slot created time
        self.sb_timestamp = tm
        self.comp_tmstamp = 0
        self.NoValidTask = False

        self.tsk = Task(self.id, self.sensertype, src,slot_no)
        self.tsk.setSubmitime(tm)
        self.ex_dev_id = fd

    def getDestinatinFogID(self):
        return self.fd_devid

    def setSubmitime(self, sim_time):
        self.sb_timestamp = sim_time
        
    def setSlotNo(self, sn):
        self.slot_no = sn

    #created slot
    def set_Cr_SlotNo(self, sn):
        self.slot_noCr = sn

    def set_ex_devid(self, id):
        self.ex_dev_id = id

    def get_ex_devid(self):
        return self.ex_dev_id
    
    #completed slot
    def set_Fi_SlotNo(self, sn):
        self.slot_noFi = sn

#set the delay and execution duration to job
#delay to start task, ram swap time, executer resource_id, cpu_speed , current slot numbrer
    def setExecutionDetails(self, delay,swap_time, dst, speed,slotno):
        
        self.tsk.setExecutionstarttime(delay)
        self.tsk.destId = dst
        duration = self.tsk.no_instructions / speed + swap_time

        self.tsk.setExecutionduration(duration)
        self.tsk.writeDetails()
        self.tsk.writeDataset()
        tasksTimetracker.RecordTimeDetails(self.tsk)

        #adding each tasks delay and computation time
        self.comp_tmstamp = self.comp_tmstamp +self.tsk.time_taken  

        new_tasktype = ACTUATER_TYPE
        if duration!=0:
            match self.tsk.task_type:
                case 1:
                    new_tasktype = CAMRA_PRO
                case 2:
                    new_tasktype = GPSPOS_PRO
                case 3:
                    new_tasktype = INDLOOP_PRO
                case 4:
                    new_tasktype =  MICWAVE_PRO

            self.tsk = Task(self.id, new_tasktype , self.tsk.destId, slotno + 1) 
            self.tsk.setSubmitime(slotno*SLOT_TIME)
        else:
            self.NoValidTask = True
        return duration

    def get_noInstructions(self):
        no_inst = self.tsk.get_noInstructions()
        return no_inst
    
    def get_type(self):
        t_type = self.tsk.get_tasktype()
        return t_type

    def get_dataBytes(self):
        return self.tsk.get_dataBytes()
    
    def get_size(self):
        return self.get_noInstructions()
    
    def get_codesize(self):
        return self.get_noInstructions()
    
    def get_devise(self):
        dev_id = self.tsk.get_devid()
        return dev_id

    def writetoDataset(self):
        self.tsk.writeDataset()


class FileWrite:
    def __init__(self):
        current_time = datetime.now()
        dt_string = current_time.strftime("%d-%m-%Y%H-%M-%S")
        self.fnameSlots = "slots-" + dt_string +".txt"
        self.fnameTasks = "tasks-"  + dt_string +".txt"
        self.dataset = "dataset-"  + dt_string +".txt"
        print(self.fnameTasks)

    def writeTaskDetails(self,str):
        with open(self.fnameTasks, 'a') as f:
            f.write(str)
            f.close()

    def writeToDataset(self,str):
        with open(self.dataset, 'a') as f:
            f.write(str)
            f.close()

    def WriteStringToJobsLog(self, jb):
        with open(self.fnameTasks, 'a') as f:
            strval = "Id:"+str(jb.id) +" SlotNo:"+ str(jb.slotno)+" Source:"+jb.ed_name +" Size:"+ str(jb.no_instructions) +" Duration:"+ str(jb.duration) + " SubmitTime:"+str(jb.sb_timestamp) +" Destination:"+ jb.dest + " Executed at:"+str(jb.ex_timestamp) +" Delay:"+ str(jb.ex_timestamp+jb.duration-jb.sb_timestamp) +"\n"
            f.write(strval)
            f.close()

    def WriteStringToSlotsLog(self,str):
        with open(self.fnameSlots, 'a') as f:
            f.write(str)
            f.close()

class Actuater :
    def __init__(self,n,type = 0):
        global g_devid
        g_devid += 1
        self.id = g_devid
        self.tmO = DeviceTime()
        self.name = n
        self.type = type
        
    def setClusterId(self, n):
        self.connected_cl_id = n
    def ExecutesTask(self,tsk):
        tsk.writeDetails()
      
class Sensor :
    # NAME and type
    def __init__(self,n,d_type):
        self.name = n
        self.task_type = d_type

        global g_devid
        g_devid += 1
        self.id = g_devid

    def setClusterId(self, n):
        self.connected_cl_id = n

    def CreateUploadJob(self,tm,slot_no):
        job = Job (self.id, self.connected_cl_id, self.task_type, tm,slot_no)
        return job

class Cloud:
    def __init__(self) :
        global g_devid
        g_devid += 1
        self.id = g_devid
        
        self.devTime = DeviceTime()
        self.name = "Cloud Server"

        self.slot_no_task_ex = 0
        self.total_job_count =0 
        self.busy_time = 0 
        self.slot_busy_time =0

        self.cost_per_unit_time = CLOUD_COST_UNIT_TIME
        self.cpu_speed = CLOUD_CPU_SPEED

        self.netwrkutil = 0.

    def get_CPUSpeed(self):
        return self.cpu_speed
    
    def ExecutesJob(self,jb,sim_time,slotno):
        if (self.devTime.get_time() < sim_time+SLOT_TIME):
            self.slot_no_task_ex += 1
            jb.set_ex_devid(self.id)
            swap_time = 0
            duration = jb.setExecutionDetails(LATENCY_CS_FR + self.devTime.get_time() - sim_time,swap_time,self.id, self.cpu_speed,slotno)
            self.devTime.add_time(duration)
            self.slot_busy_time = self.slot_busy_time + duration
        else:
            jb.writetoDataset()

    def clear(self,sim_time):
        self.total_job_count = self.total_job_count +self.slot_no_task_ex
        self.slot_no_task_ex = 0
        self.busy_time += self.slot_busy_time
        self.slot_busy_time =0
        self.devTime.set_time(sim_time)
        
    def WriteSlotSummary(self):
        logentry.WriteStringToSlotsLog("Cloud Exicuted:"+str(self.slot_no_task_ex)+"Tasks \n")
        
    def PrintNoTasksExecuted(self):
        print("Cloud executed :"+str(self.total_job_count)+" Tasks" + "\n       Time Used:"+str(self.busy_time)  + "\n       Cost:"+ str(self.busy_time*self.cost_per_unit_time))
#        print("Network Utilization :" + str(self.netwrkutil) + "MBs")        


class FogDevice :
    def __init__(self,name):
        global g_devid
        g_devid += 1
        self.id = g_devid

        self.jobsQ= DeviceJobQ()
        self.devTime = DeviceTime()
        self.name = name + str(self.id)

        self.total_time = 0.
        self.total_Comp_time = 0.
        self.noTasksExecuted = 0

        self.cores =3
        self.busy_power = 107.339
        self.idle_power = 83.4333
        self.bandwidth = FD_BANDWIDTH1
        self.ram = FD_RAM1

        #slot level variables
        self.slot_no_task_ex= 0
        self.slot_busy_time = 0

        x = g_devid % 3
        match x:
            case 0:
                self.no_core = FD_CAPACITY1
                self.cpu_speed = CPU_SPEED1
                self.bandwidth = FD_BANDWIDTH1
                self.ram = FD_RAM1
                self.busy_power = 105.00
                self.idle_power = 80.00

            case 1:
                self.no_core = FD_CAPACITY2
                self.cpu_speed = CPU_SPEED2
                self.bandwidth = FD_BANDWIDTH2
                self.ram = FD_RAM2
                self.busy_power = 110.00
                self.idle_power = 82.00
            case 2:
                self.no_core = FD_CAPACITY3
                self.cpu_speed = CPU_SPEED3
                self.bandwidth = FD_BANDWIDTH3
                self.ram = FD_RAM3
                self.busy_power = 115.339
                self.idle_power = 85.00
                
        self.Ex_capicity = self.cpu_speed *SLOT_TIME

    def get_Ex_capicity(self):
        return self.Ex_capicity
    def get_CPUSpeed(self):
        return self.cpu_speed
    def get_bPower(self):
        return self.busy_power
    def get_iPower(self):
        return self.idle_power
    def getBANDWIDTH(self):
        return self.bandwidth
    def getRAM(self):
        return self.ram
    
    def clean(self,sim_time):
#        self.slot_core_balance = 0
        self.slot_busy_time = 0
        self.slot_no_task_ex = 0
        self.devTime.set_time(sim_time)
        
    def ExecutesJob(self,jb,sim_time,slotno):

        swap_ram_no = (jb.get_noInstructions() + jb.get_dataBytes()) / self.getRAM()
        swap_time = RAM_SWAP_UNIT
        if swap_ram_no >1:
            swap_time = RAM_SWAP_UNIT * swap_ram_no

        if (self.devTime.get_time() < sim_time+SLOT_TIME-(INTERVEL_GAP+swap_time)):
            self.slot_no_task_ex += 1
            jb.set_ex_devid(self.id)
            duration = jb.setExecutionDetails(LATENCY_ED_FR /self.bandwidth  + self.devTime.get_time() - sim_time,swap_time, self.id, self.cpu_speed,slotno)
            self.devTime.add_time(duration)
            self.slot_busy_time = self.slot_busy_time + duration
        else:
            #think of calling cloud
            cs.ExecutesJob(jb,sim_time,slotno)
#            jb.writetoDataset()

    def ComputeSlotLoad(self):
        msg = "Cluster:"+ self.name 
        logentry.WriteStringToSlotsLog(msg)
        msg = " No Tasks Exicuted:"+str(self.slot_no_task_ex)
        logentry.WriteStringToSlotsLog(msg)			
        self.noTasksExecuted = self.noTasksExecuted + self.slot_no_task_ex	
        
        msg = " CPU (MIPS):"+str(self.cpu_speed) +" Busy Time:" + str(self.slot_busy_time) + "\n" 
        logentry.WriteStringToSlotsLog(msg)
        self.total_Comp_time = self.total_Comp_time + self.slot_busy_time
        self.total_time = self.total_time + SLOT_TIME
        self.devTime.set_time(self.total_time)

    def PrintResult(self,  slot):
        total_idletime = self.total_time - self.total_Comp_time
        energy_utilised = total_idletime * self.idle_power +self.total_Comp_time * self.busy_power
        TH = self.noTasksExecuted / MAX_SIMULATION_TIME
        cpu_utilization = self.total_Comp_time / self.total_time *100;
        print("Device:"+ self.name )
        print("      Total Tasks Executed:"+str(self.noTasksExecuted))
        print("      Total Busy Time:" + str(self.total_Comp_time) )
        print("      Total Idle Time:" + str(total_idletime) )
        print("      Total Time:" + str(self.total_time ))
        print("      CPU Utilization:"+ str(cpu_utilization))
        print("      Total Power Utilised:" + str( energy_utilised ))
        print("      Throughput:" + str(TH ))

logentry = FileWrite()
jobsTimetracker = TimeTrackerJb()
tasksTimetracker = TimeTrackerTsk()
cs = Cloud()
