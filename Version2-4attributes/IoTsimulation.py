
import random

import numpy as np

#import RLAgent
from config import AI_RM, ALPHA, BETA, DEFAULT_RM, GAMA, MAX_JOBS, MAX_RS, MAX_SIMULATION_TIME, RM_TYPE, SENSERS_PER_CLUSTER, SLOT_TIME
from devices import Actuater, g_cs, Sensor, FogDevice, g_logentry
from GeneticAlg import Chromosome,GeneticAlgorithm
from DL_MODEL import _build_model
from tasks import g_tasksTimetracker

#max number of allowed tasks for dataset { numSens * numOfFDs * 3 }
MaxTasksInSlot = MAX_JOBS
#number of Cluster-Fog devices 
numOfFDs = MAX_RS - 2
#number of Sensor per cluster
numSens = SENSERS_PER_CLUSTER

resource_mg_string  = ['DEFAULT_RM' ,'GA_RM','AI_RM' ]

#create task list with empty 
g_jobQ = []
g_ClusterRs = []
g_Sensors = []
g_Actuaters = []

#create cluster-fog and edge devices and connects them according to network topology
for i in range(numOfFDs):
    fr = FogDevice ("ClusterFR:")
    g_ClusterRs.append(fr)

for fr in g_ClusterRs:
    for j in range(numSens):
        #create sensers
        # create a random device from the list
        s_typelist = [1, 2, 3, 4]
        s_type=random.choice(s_typelist)
        ed = Sensor( "Sensor_"+str(fr.id)+"_"+str(j), s_type)
        #set the cluster id to newly created edge
        ed.setClusterId(fr.id)
        g_Sensors.append(ed)

    act = Actuater("Actuater"+str(fr.id))
    act.setClusterId(fr.id)
    g_Actuaters.append(act)

#returns cluster fog resource from its Id
def  getClusterFromID(id):
    for device in  g_ClusterRs:
        if device.id == id:
            return device
    return None

print("Cluster-Fds (FogDevices)")
for device in  g_ClusterRs:
    print("   " + device.name + "    CPU Speed(MIPS):" + str(device.cpu_speed) +" RAM(MB)" +str(device.ram))
    print("   " + "Cluster BandWidth:" + str(device.bandwidth ))
print("Sensor Devices " )
for device in g_Sensors:
    print ("   "+device.name +' [Id:' +str(device.id) + "] (Connected to ClusterFR:"+ str(device.connected_cl_id) + ")")
print("Actuater Devices " )
for device in g_Actuaters:
    print ("   " +device.name +' [Id:' + str(device.id) + "]  (Connected to ClusterFR:"+ str(device.connected_cl_id) + ")")

print ('Resource managemnt stratergy: '+ resource_mg_string[RM_TYPE])
print("Simulation Started")
sl_no = 0
sim_time = 0.

# write dataset header
for ds in range(MaxTasksInSlot):
    g_logentry.writeToDataset('TaskType, TaskCodeSize, TaskDataSize,BandWidth,')

for ds in range(MaxTasksInSlot):
    g_logentry.writeToDataset(' Resource_Id,')

g_logentry.writeToDataset('\n')

#deep learning AI resource manager
model = _build_model()
if RM_TYPE == AI_RM:
    model.load_weights('DL_MODULE_4RMV2.weights.h5')

if RM_TYPE != DEFAULT_RM:
    print ('Alpha:'+ str(ALPHA)+ ', Beta:'+str(BETA) + ', Gama:'+str(GAMA) )

while MAX_SIMULATION_TIME > sim_time:

    #clean buffer of cluster-fog devises to receive tasks
    for device in g_ClusterRs:
        device.clean(sim_time)
    g_cs.clear(sim_time)
    
    sl_no+=1
	#all edge devices will place tasks for execution and are add to task list
    for device in g_Sensors:
        job = device.CreateUploadJob(sim_time,sl_no)
        if job is not None:
            g_jobQ.append(job)

    msg = "\nSlot No:"+str(sl_no)+ " Tasks:"+str(len(g_jobQ)) +"\n"
    #write slot number and number of tasks to slot_log file
    g_logentry.WriteStringToSlotsLog(msg)
    g_logentry.WriteStringToSlotsLog("-------------------------------------------------------------\n")

    len_ofjobQ = len(g_jobQ)
    if len_ofjobQ > 0:
#        print ('slot no:' + str(sl_no) + ' No Tasks:'+ str(len_ofjobQ))
        match RM_TYPE:
            case 0:
                for job in g_jobQ:
                    clustrFogNode = getClusterFromID(job.getDestinatinFogID())
                    if clustrFogNode != None:
                        sz1 = job.get_size()
                        clustrFogNode.ExecutesJob(job,sim_time,sl_no)
                        if sz1==0:
                            job.NoValidTask = True

            case 1:
            #GA resource manager
                GA = GeneticAlgorithm(g_ClusterRs,g_jobQ)
                GA.GenarateOptomalChromosome()
                Cr = GA.returnBESTCRM()
#                Cr.printassignment()
                for j in range(len(g_jobQ)):
                    FR_ID = Cr.getRs(j)
                    if FR_ID!=None and FR_ID < len(g_ClusterRs) :
                        g_ClusterRs[FR_ID].ExecutesJob(g_jobQ[j],sim_time,sl_no)
                    if FR_ID!=None and FR_ID == len(g_ClusterRs) :
                        g_cs.ExecutesJob(g_jobQ[j],sim_time,sl_no)
                    if FR_ID==None:
                        clster= getClusterFromID(g_jobQ[j].getDestinatinFogID())
                        clster.ExecutesJob(g_jobQ[j],sim_time,sl_no)
                        g_jobQ[j].NoValidTask = True #verifing purpus
            case 2:

                list_tasks = []

                for j in range(len(g_jobQ)):
                    tp = g_jobQ[j].get_type()
                    sz = g_jobQ[j].get_codesize()
                    dsz = g_jobQ[j].get_dataBytes()
                    bw = 0
                    list_tasks.append(tp)
                    list_tasks.append(sz)
                    list_tasks.append(dsz)
                    list_tasks.append(bw)
                    
#                print ('slot no:' + str(sl_no) + ' No Tasks:'+ str(len_ofjobQ))    
                for r in range(MaxTasksInSlot - len_ofjobQ):
                    list_tasks.append(0)
                    list_tasks.append(0)
                    list_tasks.append(0)
                    list_tasks.append(0)
#                print(list_tasks)
                input_jobs = np.array([list_tasks])
                result = model.predict( input_jobs,verbose = 0 )

                for j in range(len(g_jobQ)):
                    FR_ID = np.argmax(result[j][0])
                    sz1 = g_jobQ[j].get_size()
                    if FR_ID==None :
                        g_jobQ[j].writetoDataset(0)
                        g_jobQ[j].NoValidTask = True
                    elif FR_ID == 0:
                        g_jobQ[j].writetoDataset(0)
                        g_jobQ[j].NoValidTask = True
                    elif FR_ID == 1 :
                        g_cs.ExecutesJob(g_jobQ[j],sim_time,sl_no)                        
                    else :
                        g_ClusterRs[FR_ID-2].ExecutesJob(g_jobQ[j],sim_time,sl_no)
                    if sz1==0:
                        g_jobQ[j].NoValidTask = True
                  
    for r in range(MaxTasksInSlot - len_ofjobQ):
        g_logentry.writeToDataset(' 0 , 0, 0, 0,')

    for job in g_jobQ:
        g_logentry.writeToDataset( str (job.get_ex_devid()) + ',')

    for r in range(MaxTasksInSlot - len_ofjobQ):
        g_logentry.writeToDataset('0,')

    new_JobQ = []
    for j in g_jobQ :
        if j.NoValidTask:
            pass
#            jobsTimetracker.RecordTimeDetails(j)
        else:
            new_JobQ.append(j)

    g_jobQ = new_JobQ.copy()
    sim_time = sim_time + SLOT_TIME

    #write the summary of execution of task at each slot to slot_summary log file
    for device in g_ClusterRs:
        device.ComputeSlotLoad()
    
    g_logentry.writeToDataset('\n')
    g_cs.WriteSlotSummary()

print("Simulation Completed")
print("-----------Results--------------------")
print("Total Simulation Time:"+ str(MAX_SIMULATION_TIME))
print("Total Number of Slots:"+ str(sl_no))		

g_tasksTimetracker.PrintTimeDetails()
print()
for device in g_ClusterRs:
    device.PrintResult(sl_no )
    print()

g_cs.PrintNoTasksExecuted()
print()

print("\nYou could see:")
print("              " + g_logentry.fnameTasks + " for details on each tasks ")
print("              " + g_logentry.fnameSlots + " for summary of each slot")
print("---------------------------------------");	
