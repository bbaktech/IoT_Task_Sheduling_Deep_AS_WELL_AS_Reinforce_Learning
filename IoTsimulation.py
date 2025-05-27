
import random

import numpy as np

#import RLAgent
from config import MAX_JOBS, MAX_RS, MAX_SIMULATION_TIME, RM_TYPE, SENSERS_PER_CLUSTER, SLOT_TIME
from devices import Actuater,Sensor, FogDevice,cs, Job, logentry, jobsTimetracker,tasksTimetracker,resource_mg_string
from GeneticAlg import Chromosome,GeneticAlgorithm
from DL_MODEL import _build_model

#max number of allowed tasks for dataset { numSens * numOfFDs * 3 }
MaxTasksInSlot = MAX_JOBS
#number of Cluster-Fog devices 
numOfFDs = MAX_RS - 2
#number of Sensor per cluster
numSens = SENSERS_PER_CLUSTER

#create task list with empty 
jobQ = []
ClusterRs = []
Sensors = []
Actuaters = []

#create cluster-fog and edge devices and connects them according to network topology
for i in range(numOfFDs):
    fr = FogDevice ("ClusterFR:")
    ClusterRs.append(fr)

for fr in ClusterRs:
    for j in range(numSens):
        #create sensers
        # create a random device from the list
        s_typelist = [1, 2, 3, 4]
        s_type=random.choice(s_typelist)
        ed = Sensor( "Sensor_"+str(fr.id)+"_"+str(j), s_type)
        #set the cluster id to newly created edge
        ed.setClusterId(fr.id)
        Sensors.append(ed)

    act = Actuater("Actuater"+str(fr.id))
    act.setClusterId(fr.id)
    Actuaters.append(act)

#returns cluster fog resource from its Id
def  getClusterFromID(id):
    for device in  ClusterRs:
        if device.id == id:
            return device
    return None

print("Cluster-Fds (FogDevices)")
for device in  ClusterRs:
    print("   " + device.name + "    CPU Speed:" + str(device.cpu_speed) )
print("Sensor Devices " )
for device in Sensors:
    print ("   "+device.name +' [Id:' +str(device.id) + "] (Connected to ClusterFR:"+ str(device.connected_cl_id) + ")")
print("Actuater Devices " )
for device in Actuaters:
    print ("   " +device.name +' [Id:' + str(device.id) + "]  (Connected to ClusterFR:"+ str(device.connected_cl_id) + ")")

print ('Resource managemnt stratergy: '+ resource_mg_string[RM_TYPE])
print("Simulation Started")
sl_no = 0
sim_time = 0.

# write dataset header
for ds in range(MaxTasksInSlot):
    logentry.writeToDataset('TaskType, TaskSize, Device-Id,')

for ds in range(MaxTasksInSlot):
    logentry.writeToDataset(' Resource_Id,')

logentry.writeToDataset('\n')

#deep learning AI resource manager
model = _build_model()
model.load_weights('DL_MODULE_4RMV1.weights.h5')

while MAX_SIMULATION_TIME > sim_time:

    #clean buffer of cluster-fog devises to receive tasks
    for device in ClusterRs:
        device.clean(sim_time)
    cs.clear(sim_time)
    
    sl_no+=1
	#all edge devices will place tasks for execution and are add to task list
    for device in Sensors:
        job = device.CreateUploadJob(sim_time,sl_no)
        if job is not None:
            jobQ.append(job)

    msg = "\nSlot No:"+str(sl_no)+ " Tasks:"+str(len(jobQ)) +"\n"
    #write slot number and number of tasks to slot_log file
    logentry.WriteStringToSlotsLog(msg)
    logentry.WriteStringToSlotsLog("-------------------------------------------------------------\n")

    len_ofjobQ = len(jobQ)
    if len_ofjobQ > 0:
#        print ('slot no:' + str(sl_no) + ' No Tasks:'+ str(len_ofjobQ))
        match RM_TYPE:
            case 0:
                for job in jobQ:
                    clustrFogNode = getClusterFromID(job.getDestinatinFogID())
                    if clustrFogNode != None:
                        clustrFogNode.ExecutesJob(job,sim_time,sl_no)
            case 1:
            #GA resource manager
                GA = GeneticAlgorithm(ClusterRs,jobQ)
                GA.GenarateOptomalChromosome()
                Cr = GA.returnBESTCRM()
#                Cr.printassignment()
                for j in range(len(jobQ)):
                    FR_ID = Cr.getRs(j)
                    if FR_ID!=None and FR_ID < len(ClusterRs) :
                        ClusterRs[FR_ID].ExecutesJob(jobQ[j],sim_time,sl_no)
                    if FR_ID!=None and FR_ID == len(ClusterRs) :
                        cs.ExecutesJob(jobQ[j],sim_time,sl_no)
                    if FR_ID==None:
                        cl= getClusterFromID(jobQ[j].getDestinatinFogID())
                        cl.ExecutesJob(jobQ[j],sim_time,sl_no)
                        jobQ[j].NoValidTask = True
            case 2:
                # #deep learning AI resource manager
                # model = _build_model()
                # model.load_weights('DL_MODULE_4RMV1.weights.h5')

                list_tasks = []

                for j in range(len(jobQ)):
                    tp = jobQ[j].get_type()
                    sz = jobQ[j].get_size()
                    dev = jobQ[j].get_devise()
                    
                    list_tasks.append(tp)
                    list_tasks.append(sz)
                    list_tasks.append(dev)
                    
#                print ('slot no:' + str(sl_no) + ' No Tasks:'+ str(len_ofjobQ))    
                for r in range(MaxTasksInSlot - len_ofjobQ):
                    list_tasks.append(0)
                    list_tasks.append(0)
                    list_tasks.append(0)

                input_jobs = np.array([list_tasks])
                result = model.predict( input_jobs,verbose = 0 )

                for j in range(len(jobQ)):
                    FR_ID = np.argmax(result[j][0])
                    sz = jobQ[j].get_size()
                    if FR_ID==None :
                        jobQ[j].writetoDataset()
                        jobQ[j].NoValidTask = True
                    elif FR_ID == 0:
                        jobQ[j].writetoDataset()
                        jobQ[j].NoValidTask = True
                    elif FR_ID == 1 :
                        cs.ExecutesJob(jobQ[j],sim_time,sl_no)                        
                    else :
                        ClusterRs[FR_ID-2].ExecutesJob(jobQ[j],sim_time,sl_no)
                  
    for r in range(MaxTasksInSlot - len_ofjobQ):
        logentry.writeToDataset(' 0 , 0, 0,')

    for job in jobQ:
        logentry.writeToDataset( str (job.get_ex_devid()) + ',')

    for r in range(MaxTasksInSlot - len_ofjobQ):
        logentry.writeToDataset('0,')

    new_JobQ = []
    for j in jobQ :
        if j.NoValidTask:
            jobsTimetracker.RecordTimeDetails(j)
        else:
            new_JobQ.append(j)

    jobQ = new_JobQ.copy()
    sim_time = sim_time + SLOT_TIME

    #write the summary of execution of task at each slot to slot_summary log file
    for device in ClusterRs:
        device.ComputeSlotLoad()
    
    logentry.writeToDataset('\n')
    cs.WriteSlotSummary()

print("Simulation Completed")
print("-----------Results--------------------")
print("Total Simulation Time:"+ str(MAX_SIMULATION_TIME))
print("Total Number of Slots:"+ str(sl_no))		
# jobsTimetracker.PrintTimeDetails()
# print()
tasksTimetracker.PrintTimeDetails()
print()
for device in ClusterRs:
    device.PrintResult(sl_no )
    print()

cs.PrintNoTasksExecuted()
print()

print("\nYou could see:")
print("              " + logentry.fnameTasks + " for details on each tasks ")
print("              " + logentry.fnameSlots + " for summary of each slot")
print("---------------------------------------");	
