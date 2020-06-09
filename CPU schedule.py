from queue import Queue
import copy



class Process:
    def __init__(self, idStr, id, cpuBurst, arrivalTime, priority ):
        self.idStr = idStr
        self.id = id
        self.cpuBurst = cpuBurst
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.leftTime = cpuBurst
        self.turnAround = 0
        self.waiting = 0
        self.do = False
        
class ScheduleMethod:
    def __init__( self ):
        self.FCFSrecord = '-'
        self.RRrecord = '-'
        self.PSJFrecord = '-'
        self.NSJFrecord = '-'
        self.PPrecord = '-'  
        self.FCFSdoneList = [] 
        self.RRdoneList = []
        self.PSJFdoneList = []
        self.NSJFdoneList = []
        self.PPdoneList = [] 
    
    def __del__(self):
        ''''''
    
    def CheckProcessIn(self, processList, waitingQueue,timeLine ):
        while len( processList ) > 0:
            if timeLine >= processList[0].arrivalTime:
                waitingQueue.append(  processList.pop( 0 ) )
            else:
                break
        
                 
    def FCFS( self, processList ):
        processList = sorted(processList ,key=lambda x: ( x.arrivalTime, x.id ))
        processNum = len( processList )
        waitingQueue = []
        timeLine = processList[0].arrivalTime
        
        self.CheckProcessIn( processList, waitingQueue, timeLine )
        currentProcess = waitingQueue.pop( 0 )
            
        while len( self.FCFSdoneList ) != processNum :
            timeLine = currentProcess.cpuBurst + timeLine
            currentProcess.turnAround = timeLine - currentProcess.arrivalTime
            currentProcess.waiting = currentProcess.turnAround - currentProcess.cpuBurst
            for i in range( currentProcess.cpuBurst ):
                self.FCFSrecord = self.FCFSrecord + currentProcess.idStr 
            self.FCFSdoneList.append( currentProcess )
            self.CheckProcessIn( processList, waitingQueue, timeLine )
            if len(waitingQueue) > 0:
                    currentProcess = waitingQueue.pop( 0 )
            
            
        self.FCFSdoneList = sorted( self.FCFSdoneList ,key=lambda x:  x.id )  
            
    def RR( self, processList, timeSlice ):
        processList = sorted(processList ,key=lambda x: ( x.arrivalTime, x.id ))
        processNum = len( processList )
        waitingQueue = []
        timeLine = processList[0].arrivalTime
        
        self.CheckProcessIn( processList, waitingQueue ,timeLine )
        currentProcess = waitingQueue.pop( 0 )
        
        while len( self.RRdoneList ) != processNum :
            for i in range( timeSlice ):
                if currentProcess.leftTime > 0:
                    currentProcess.leftTime -= 1
                    currentProcess.do = True
                    timeLine += 1
                    self.RRrecord = self.RRrecord + currentProcess.idStr 
                else:
                    break
            
            if currentProcess.leftTime == 0:
                currentProcess.turnAround = timeLine - currentProcess.arrivalTime
                currentProcess.waiting = currentProcess.turnAround - currentProcess.cpuBurst
                self.RRdoneList.append( currentProcess )
                if len( waitingQueue ) > 0 :
                    currentProcess = waitingQueue.pop( 0 )
                self.CheckProcessIn( processList, waitingQueue, timeLine )
                
            else:
                self.CheckProcessIn( processList, waitingQueue, timeLine )
                waitingQueue.append( currentProcess )
                currentProcess = waitingQueue.pop( 0 )
            
          
        self.RRdoneList = sorted( self.RRdoneList ,key=lambda x:  x.id )  
        
    def PSJF( self, processList ):
        processList = sorted(processList ,key=lambda x: ( x.arrivalTime, x.leftTime, x.id ))
        processNum = len( processList )
        waitingQueue = []
        timeLine = processList[0].arrivalTime
        
        self.CheckProcessIn( processList, waitingQueue ,timeLine )
        currentProcess = waitingQueue.pop( 0 )
        
        while len( self.PSJFdoneList ) != processNum :
            currentProcess.leftTime -= 1
            currentProcess.do = True
            timeLine += 1
            self.PSJFrecord = self.PSJFrecord + currentProcess.idStr 
            
            if currentProcess.leftTime == 0:
                currentProcess.turnAround = timeLine - currentProcess.arrivalTime
                currentProcess.waiting = currentProcess.turnAround - currentProcess.cpuBurst
                self.PSJFdoneList.append( currentProcess )
                if len(waitingQueue) > 0:
                    currentProcess = waitingQueue.pop( 0 )
                    
            self.CheckProcessIn( processList, waitingQueue, timeLine )
            waitingQueue = sorted( waitingQueue ,key=lambda x:  ( x.leftTime, x.do, x.arrivalTime, x.id ) )
            
            if( len(waitingQueue) > 0 ):
                if waitingQueue[0].leftTime < currentProcess.leftTime:
                    waitingQueue.append( currentProcess ) 
                    currentProcess = waitingQueue.pop( 0 )
                    waitingQueue = sorted( waitingQueue ,key=lambda x:  ( x.leftTime, x.do, x.arrivalTime, x.id ) )
          
        self.PSJFdoneList = sorted( self.PSJFdoneList ,key=lambda x:  x.id )  
            
    def NSJF( self, processList ):
        processList = sorted(processList ,key=lambda x: ( x.arrivalTime, x.cpuBurst, x.id ))
        processNum = len( processList )
        waitingQueue = []
        timeLine = processList[0].arrivalTime
        
        self.CheckProcessIn( processList, waitingQueue, timeLine )
        currentProcess = waitingQueue.pop( 0 )
            
        while len( self.NSJFdoneList ) != processNum :
            timeLine = currentProcess.cpuBurst + timeLine
            currentProcess.turnAround = timeLine - currentProcess.arrivalTime
            currentProcess.waiting = currentProcess.turnAround - currentProcess.cpuBurst
            for i in range( currentProcess.cpuBurst ):
                self.NSJFrecord = self.NSJFrecord + currentProcess.idStr 
            self.NSJFdoneList.append( currentProcess )
            self.CheckProcessIn( processList, waitingQueue, timeLine )
            waitingQueue = sorted( waitingQueue ,key=lambda x:  x.cpuBurst )
            if len(waitingQueue) > 0:
                    currentProcess = waitingQueue.pop( 0 )
          
        self.NSJFdoneList = sorted( self.NSJFdoneList ,key=lambda x:  x.id )  
        
    def PP( self, processList ):
        processList = sorted(processList ,key=lambda x: ( x.arrivalTime, x.priority, x.id ))
        processNum = len( processList )
        waitingQueue = []
        timeLine = processList[0].arrivalTime
        
        self.CheckProcessIn( processList, waitingQueue ,timeLine )
        currentProcess = waitingQueue.pop( 0 )
        
        while len( self.PPdoneList ) != processNum :
            currentProcess.leftTime -= 1
            currentProcess.do = True
            timeLine += 1
            self.PPrecord = self.PPrecord + currentProcess.idStr 
            
            if currentProcess.leftTime == 0:
                currentProcess.turnAround = timeLine - currentProcess.arrivalTime
                currentProcess.waiting = currentProcess.turnAround - currentProcess.cpuBurst
                self.PPdoneList.append( currentProcess )
                if len(waitingQueue) > 0:
                    currentProcess = waitingQueue.pop( 0 )
                    
            self.CheckProcessIn( processList, waitingQueue, timeLine )
            waitingQueue = sorted( waitingQueue ,key=lambda x:  ( x.priority, x.do, x.arrivalTime, x.id ) )
            
            if( len( waitingQueue ) > 0 ):
                if waitingQueue[0].priority < currentProcess.priority:
                    waitingQueue.append( currentProcess ) 
                    currentProcess = waitingQueue.pop( 0 )
                    waitingQueue = sorted( waitingQueue ,key=lambda x:  ( x.priority, x.do, x.arrivalTime, x.id ) )
            
          
        self.PPdoneList = sorted( self.PPdoneList ,key=lambda x:  x.id ) 
        
    def OutPut( self, task, fileName ) :
        output = open( fileName +"_output.txt", 'w' )
        if task == 1:
            output.write( '==    FCFS==\n' )
            output.write( self.FCFSrecord )
            output.write( '\n' )
            output.write("===========================================================\n\n")
            output.write("Waiting Time\nID      FCFS\n===========================================================\n") 
            for index in range( len(self.FCFSdoneList) ):
                output.write( str( self.FCFSdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.FCFSdoneList[index].waiting ) )
                output.write( '\t\t' )
            output.write("===========================================================\n\nTurnaround Time\nID      FCFS    \n===========================================================\n") # print labels
            for index in range( len( self.FCFSdoneList ) ):
                output.write( str( self.FCFSdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.FCFSdoneList[index].turnAround ) )
                output.write( '\t\t' )
            output.write("===========================================================")
            
            
        elif task == 2:
            output.write( '==      RR==\n' )
            output.write( self.RRrecord )
            output.write( '\n' )
            output.write("===========================================================\n\n")
            output.write("Waiting Time\nID      RR\n===========================================================\n") 
            for index in range( len(self.RRdoneList) ):
                output.write( str( self.RRdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.RRdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================\n\nTurnaround Time\nID      RR    \n===========================================================\n") # print labels
            for index in range( len( self.RRdoneList ) ):
                output.write( str( self.RRdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.RRdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================")

        elif task == 3:
            output.write( '==    PSJF==\n' )
            output.write( self.PSJFrecord )
            output.write( '\n' )
            output.write("===========================================================\n\n")
            output.write("Waiting Time\nID      PSJF\n===========================================================\n") 
            for index in range( len(self.PSJFdoneList) ):
                output.write( str( self.PSJFdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.PSJFdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================\n\nTurnaround Time\nID      PSJF    \n===========================================================\n") # print labels
            for index in range( len( self.PSJFdoneList ) ):
                output.write( str( self.PSJFdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.PSJFdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================")
            
        elif task == 4:
            output.write( '==Non-PSJF==\n' )
            output.write( self.NSJFrecord )
            output.write( '\n' )
            output.write("===========================================================\n\n")
            output.write("Waiting Time\nID      NPSJF\n===========================================================\n") 
            for index in range( len(self.NSJFdoneList) ):
                output.write( str( self.NSJFdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.NSJFdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================\n\nTurnaround Time\nID      NSJF    \n===========================================================\n") # print labels
            for index in range( len( self.NSJFdoneList ) ):
                output.write( str( self.NSJFdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.NSJFdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================")

        elif task == 5:
            output.write( '== Priority==\n' )
            output.write( self.PPrecord )
            output.write( '\n' )
            output.write("===========================================================\n\n")
            output.write("Waiting Time\nID      Priority\n===========================================================\n") 
            for index in range( len(self.PPdoneList) ):
                output.write( str( self.PPdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.PPdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================\n\nTurnaround Time\nID      PP    \n===========================================================\n") # print labels
            for index in range( len( self.PPdoneList ) ):
                output.write( str( self.PPdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.PPdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( '\n' )
            output.write("===========================================================")

        elif task == 6:
            output.write( '==    FCFS==\n' )
            output.write( self.FCFSrecord )
            output.write( '\n' )
            output.write( '==      RR==\n' )
            output.write( self.RRrecord )
            output.write( '\n' )
            output.write( '==    PSJF==\n' )
            output.write( self.PSJFrecord )
            output.write( '\n' )
            output.write( '==Non-PSJF==\n' )
            output.write( self.NSJFrecord )
            output.write( '\n' )
            output.write( '== Priority==\n' )
            output.write( self.PPrecord )
            output.write( '\n' )
            output.write("===========================================================\n\n")
            output.write("Waiting Time\nID      FCFS    RR      PSJF    NPSJF   Priority\n===========================================================\n")
            for index in range( len(self.FCFSdoneList) ):
                output.write( str( self.FCFSdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.FCFSdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( str( self.RRdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( str( self.PSJFdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( str( self.NSJFdoneList[index].waiting ) )
                output.write( '\t\t' )
                output.write( str( self.PPdoneList[index].waiting ) )
                output.write( '\n' )
            output.write("===========================================================\n\nTurnaround Time\nID      FCFS    RR      PSJF    NPSJF   Priority\n===========================================================\n") # print labels
            for index in range( len( self.FCFSdoneList ) ):
                output.write( str( self.FCFSdoneList[index].id ) )
                output.write( '\t\t' )
                output.write( str( self.FCFSdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( str( self.RRdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( str( self.PSJFdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( str( self.NSJFdoneList[index].turnAround ) )
                output.write( '\t\t' )
                output.write( str( self.PPdoneList[index].turnAround ) )
                output.write( '\n' )
            output.write("===========================================================")
def main():
    processList = []
    fileName = input('請輸入檔案名稱or輸入0離開\n')
    
    while fileName != "0" :
        f = open( fileName + '.txt', 'r')
        task, timeSlice = [int(num) for num in f.readline().split()]
        f.readline()
        
        while True:
            inputLine = f.readline()
            if not inputLine :  # EOF  
                break
            
            id, cpuBurst, arrivalTime, priority = [ int(num) for num in inputLine.split() ]
            if( id >= 10 ):
                idStr = chr( id+ 55 )
            else:
                idStr = str( id )
            processList.append( Process( idStr, id, cpuBurst, arrivalTime, priority ) ) 
    
        if task == 1:
            method =  ScheduleMethod()
            method.FCFS( copy.deepcopy( processList ) )
            method.OutPut( task, fileName )
        elif task == 2:
            method = ScheduleMethod()
            method.RR( copy.deepcopy( processList ), timeSlice )
            method.OutPut( task, fileName )
        elif task == 3:
            method = ScheduleMethod()
            method.PSJF( copy.deepcopy( processList ) )
            method.OutPut( task, fileName )
        elif task == 4:
            method = ScheduleMethod()
            method.NSJF( copy.deepcopy( processList ) )
            method.OutPut( task, fileName )
        elif task == 5:
            method = ScheduleMethod()
            method.PP( copy.deepcopy( processList ) )
            method.OutPut( task, fileName )
        elif task == 6:
            method = ScheduleMethod()
            method.FCFS( copy.deepcopy( processList ) )
            method.RR( copy.deepcopy( processList ), timeSlice )
            method.PSJF( copy.deepcopy( processList ) )
            method.NSJF( copy.deepcopy( processList ) )
            method.PP( copy.deepcopy( processList ) )
            method.OutPut( task, fileName )
        
        processList.clear()
        del method
        fileName = input('請輸入檔案名稱or輸入0離開\n')

    print('bye')
    f.close()

if __name__ == '__main__':
    main()