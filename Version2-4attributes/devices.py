
from config import ACTUATER_TYPE, CAMRA_PRO, CLOUD_COST_UNIT_TIME, CLOUD_CPU_SPEED, CPU_SPEED1, CPU_SPEED2, CPU_SPEED3, DATA_SIZE1, DATA_SIZE2, DATA_SIZE3, DATA_SIZE4, FD_BANDWIDTH1, FD_BANDWIDTH2, FD_BANDWIDTH3,  FD_CAPACITY1, FD_CAPACITY2, FD_CAPACITY3, FD_RAM1, FD_RAM2, FD_RAM3, GPSPOS_PRO, INDLOOP_PRO, INTERVEL_GAP, LATENCY_CS_FR, LATENCY_ED_FR, MAX_JOBS, MAX_RS, MAX_SIMULATION_TIME, MICWAVE_PRO, NO_INSTRUCTIONS1, NO_INSTRUCTIONS2, NO_INSTRUCTIONS3, NO_INSTRUCTIONS4, RAM_SWAP_UNIT, ROAD_DISPLAY, SENSER_TYPE, SENSERS_PER_CLUSTER, SLOT_TIME
import random

from tasks import Job, g_logentry,TimeTrackerJb, TimeTrackerTsk
g_devid = 0

class DeviceTime:
    def __init__(self):
        self.tm = 0.
    def set_time(self, tm):
        self.tm = tm
    def add_time(self,tm):
        self.tm += tm
    def get_time(self):
        return self.tm
    
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
        self.bw = 1

        self.netwrkutil = 0.

    def get_CPUSpeed(self):
        return self.cpu_speed
    
    def ExecutesJob(self,jb,sim_time,slotno):
        if (self.devTime.get_time() < sim_time+SLOT_TIME):
            self.slot_no_task_ex += 1
            jb.set_ex_devid(self.id)
            swap_time = 0
            duration = jb.setExecutionDetails(LATENCY_CS_FR + self.devTime.get_time() - sim_time,swap_time,self.id, self.cpu_speed,slotno,self.bw)
            self.devTime.add_time(duration)
            self.slot_busy_time = self.slot_busy_time + duration
        else:
            jb.writetoDataset(0)
            jb.NoValidTask = True

    def clear(self,sim_time):
        self.total_job_count = self.total_job_count +self.slot_no_task_ex
        self.slot_no_task_ex = 0
        self.busy_time += self.slot_busy_time
        self.slot_busy_time =0
        self.devTime.set_time(sim_time)
        
    def WriteSlotSummary(self):
        g_logentry.WriteStringToSlotsLog("Cloud Exicuted:"+str(self.slot_no_task_ex)+"Tasks \n")
        
    def PrintNoTasksExecuted(self):
        print("Cloud executed :"+str(self.total_job_count)+" Tasks" + "\n       Time Used:"+str(self.busy_time)  + "\n       Cost:"+ str(self.busy_time*self.cost_per_unit_time))
#        print("Network Utilization :" + str(self.netwrkutil) + "MBs")        


class FogDevice :
    def __init__(self,name):
        global g_devid
        g_devid += 1
        self.id = g_devid

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
            duration = jb.setExecutionDetails(LATENCY_ED_FR /self.bandwidth  + self.devTime.get_time() - sim_time,swap_time, self.id, self.cpu_speed,slotno, self.bandwidth)
            self.devTime.add_time(duration)
            self.slot_busy_time = self.slot_busy_time + duration
        else:
            g_cs.ExecutesJob(jb,sim_time,slotno)
#            jb.writetoDataset()

    def ComputeSlotLoad(self):
        msg = "Cluster:"+ self.name 
        g_logentry.WriteStringToSlotsLog(msg)
        msg = " No Tasks Exicuted:"+str(self.slot_no_task_ex)
        g_logentry.WriteStringToSlotsLog(msg)			
        self.noTasksExecuted = self.noTasksExecuted + self.slot_no_task_ex	
        
        msg = " CPU (MIPS):"+str(self.cpu_speed) +" Busy Time:" + str(self.slot_busy_time) + "\n" 
        g_logentry.WriteStringToSlotsLog(msg) 
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


g_cs = Cloud()
