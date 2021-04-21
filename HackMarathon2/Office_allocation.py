import pandas as pd
import numpy as np
import copy

def office_allocation():
    #Working hours:
    WORK_BEGIN=8
    WORK_FINISH=18

    #Penalty factors:
    #Outside of given time limit: Hour difference*10
    HD=10
    #Room overfilled:
    OF=50

    #read data
    df_regs=pd.read_csv("Registrations.csv",index_col=0,sep=';')
    df_rooms=pd.read_csv("Rooms.csv",sep=';')


    #penalty calculator
    def penalty_calculator(day_matrix,schedule):
        penalty=0
        for row in range(schedule.shape[0]):
            for col in range(schedule.shape[1]):
                if schedule[row][col]!=-1:
                    for i in range(len(day_matrix)):
                        if day_matrix[i][0]==schedule[row][col]:
                            tmp_index=i
                    if col+8< day_matrix[tmp_index][2] or col+8>=day_matrix[tmp_index][3]:
                        penalty+=HD
                    if df_rooms.loc[df_rooms.index[row],'Spaces']<day_matrix[tmp_index][4]:
                        penalty+=OF
        return penalty

    def random_schedule(day,day_matrix):
        day_matrix_tmp=copy.copy(day_matrix)
        new_schedule=day
        flat_schedule=np.zeros(day.shape[0]*day.shape[1])
        for i in range(len(flat_schedule)):
            flat_schedule[i]=i
        #empty_rooms=np.ones(1,day.shape[0])
        for i in range(len(day_matrix_tmp)):
            if len(day_matrix_tmp)!=1:
                element=np.random.randint(0,len(day_matrix_tmp)-1)
            else: 
                element=0
            interval=int(day_matrix_tmp[element][3])-int(day_matrix_tmp[element][2])
            possible_times=[]
            for j in range(len(flat_schedule)):
                possible=True
                if j<=len(flat_schedule)-interval:
                    for k in range(interval):
                        if flat_schedule[j+k]!=flat_schedule[j]+k or flat_schedule[j]//day.shape[1]!=flat_schedule[j+k]//day.shape[1]:
                            possible=False
                else:
                    possible=False
                if possible==True:
                    possible_times.append(flat_schedule[j])
            #print(possible_times)
            time=np.random.randint(0,len(possible_times)-1)
            for z in range(interval):
                tmp_1=int(possible_times[time]//day.shape[1])
                tmp_2=int(possible_times[time]%day.shape[1]+z)
                new_schedule[tmp_1][tmp_2]=day_matrix_tmp[element][0]
                flat_schedule=np.delete(flat_schedule,np.where(flat_schedule ==(possible_times[time]+z)))
            day_matrix_tmp.pop(element)         

        return new_schedule

    combinations=[]
    for i in range(2**(df_rooms.shape[0])):
        binary=[]
        tmp=bin(i)
        tmp=str(tmp)
        difference=df_rooms.shape[0]-(len(tmp)-2)
        for i in range(difference):
            binary.append(0)
        for i in range(2,len(tmp)):
            if tmp[i]=='0':
                binary.append(0)
            else:
                binary.append(1)
        combinations.append(binary)

    def fine_search(day,schedule):
    
        for i in range(len(combinations)):
            tmp_schedule_right=copy.copy(schedule).tolist()
            tmp_schedule_left=copy.copy(schedule).tolist()
            for j in range(len(combinations[i])):
                if combinations[i][j]==1:
                    tmp_schedule_right[j].append(tmp_schedule_right[j][0])
                    tmp_schedule_right[j].pop(0)
                    tmp_schedule_right_np=np.array(tmp_schedule_right)
                    if penalty_calculator(day,tmp_schedule_right_np)==0:
                        return tmp_schedule_right_np
                    else:
                        tmp_schedule_left[j].insert(0,tmp_schedule_left[j][len(tmp_schedule_left[j])-1])
                        tmp_schedule_left[j].pop(len(tmp_schedule_left[j])-1)
                        tmp_schedule_left_np=np.array(tmp_schedule_left)
                        if penalty_calculator(day,tmp_schedule_left_np)==0:
                            return tmp_schedule_left_np
        return schedule


    Monday_matrix=[]
    Thuesday_matrix=[]
    Wednesday_matrix=[]
    Thursday_matrix=[]
    Friday_matrix=[]

    Week_matrix=[Monday_matrix,Thuesday_matrix,Wednesday_matrix,Thursday_matrix,Friday_matrix]

    for i,row in df_regs.iterrows():
        if df_regs.loc[df_regs.index[i],'Day']=='Monday':
            Monday_matrix.append([i,row.Head,row.From,row.To,row.Size])
        if df_regs.loc[df_regs.index[i],'Day']=='Thuesday':
            Thuesday_matrix.append([i,row.Head,row.From,row.To,row.Size])
        if df_regs.loc[df_regs.index[i],'Day']=='Wednesday':
            Wednesday_matrix.append([i,row.Head,row.From,row.To,row.Size])
        if df_regs.loc[df_regs.index[i],'Day']=='Thursday':
            Thursday_matrix.append([i,row.Head,row.From,row.To,row.Size])
        if df_regs.loc[df_regs.index[i],'Day']=='Friday':
            Friday_matrix.append([i,row.Head,row.From,row.To,row.Size])


    Room_matrix=np.zeros([df_rooms.shape[0],WORK_FINISH-WORK_BEGIN])
    Week_schedule=[]


    #Fillin weekly schedule with random numbers
    for i,day in enumerate(Week_matrix):
        pen=1000
        j=0
        while pen!=0:
            j+=1
            tmp_schedule=random_schedule(np.full((df_rooms.shape[0],WORK_FINISH-WORK_BEGIN),-1),Week_matrix[i])
            pen=penalty_calculator(Week_matrix[i],tmp_schedule)
            if pen<=40 and pen>0:
                tmp_schedule=fine_search(Week_matrix[i],tmp_schedule)
                pen=penalty_calculator(Week_matrix[i],tmp_schedule)

        Week_schedule.append(tmp_schedule)
        #Week_schedule.append(np.random.randint(-1,len(day),(df_rooms.shape[0],WORK_FINISH-WORK_BEGIN)))

    return Week_schedule