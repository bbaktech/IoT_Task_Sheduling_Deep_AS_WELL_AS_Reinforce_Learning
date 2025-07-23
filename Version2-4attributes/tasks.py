
from datetime import datetime
from config import ACTUATER_TYPE, CAMRA_PRO, DATA_SIZE1,DATA_SIZE2,DATA_SIZE3,DATA_SIZE4, GPSPOS_PRO, INDLOOP_PRO, MICWAVE_PRO, NO_INSTRUCTIONS1, NO_INSTRUCTIONS2,NO_INSTRUCTIONS3, NO_INSTRUCTIONS4, SLOT_TIME

g_jobserno = 0
g_taskid = 0

taskType_strings = ['CAMRA_SEN','GPSPOS_SEN','INDLOOP_SEN','MICWAVE_SEN','CONT_DISPLAY','ROAD_DISPLAY','CAMRA_PRO',
                    'INDLOOP_PRO' ,'GPSPOS_PRO','MICWAVE_PRO','CAMRA_STORE','INDLOOP_STORE','GPSPOS_STORE','MICWAVE_STORE']

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
        g_logentry.writeTaskDetails(strVal)

    def writeDataset(self,bandwidth):
        g_logentry.writeToDataset(str(self.task_type-1) +', '+ str(self.no_instructions) +', '+str(self.dataBytes) +', ' +str(bandwidth) +', ' )

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
    def setExecutionDetails(self, delay,swap_time, dst, speed,slotno,bw):
        
        self.tsk.setExecutionstarttime(delay)
        self.tsk.destId = dst
        duration = self.tsk.no_instructions / speed + swap_time

        self.tsk.setExecutionduration(duration)
        self.tsk.writeDetails()
        self.tsk.writeDataset(bw)
        g_tasksTimetracker.RecordTimeDetails(self.tsk)

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
#            if self.get_noInstructions() ==0:
#                self.NoValidTask = True
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

    def writetoDataset(self,bw):
        self.tsk.writeDataset(bw)

g_tasksTimetracker = TimeTrackerTsk()
g_logentry = FileWrite()
