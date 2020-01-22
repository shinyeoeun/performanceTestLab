import csv
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

class memoryCheck(object):
    X_Time = []
    Y_Memory = []
    Y_Battery = []
    Y_Temperature = []
    Y_Cpu = []

    def __init__(self, count):
        self.counter = count
        self.alldata = [("timestamp", "batstatus", "memvalue")]

    def getValues(self):
        # result_mem = os.popen("adb shell dumpsys meminfo com.linecorp.yuki | grep TOTAL")
        result_mem = os.popen("adb shell dumpsys meminfo com.linecorp.yuki | findstr TOTAL")
        memvalue = result_mem.readline().split()[1].strip()

        result_temp = os.popen("adb shell dumpsys battery | findstr temperature")
        tempvalue = result_temp.readline().split()[1].strip()
        tempvalue_for_graph = tempvalue.split(":")[0]

        result_battery = os.popen("adb shell dumpsys battery | findstr level")
        batvalue = result_battery.readline().split()[1].strip()
        batvalue_for_graph = batvalue.split(":")[0]

        currenttime = self.getCurrentTime()
        print("current time: "+currenttime)
        print("Memory Usage: " + memvalue[:3])
        print("Battery remain: " + batvalue)
        print("Battery temperature: " + tempvalue)

        self.X_Time.append(currenttime)
        self.Y_Memory.append(int(memvalue[:2]))
        self.Y_Battery.append(batvalue_for_graph)
        self.Y_Temperature.append(tempvalue_for_graph)

    def getCurrentTime(self):
        currentTime = time.strftime("%H:%M:%S", time.localtime())
        return currentTime

    def pltgraphic(self):
        plt.figure(figsize=(10, 7))
        plt.style.use(['seaborn-dark'])

        plt.subplot(2, 1, 1)
        plt.plot(self.X_Time, self.Y_Memory, color='b', marker='o', label='memory(MB)')
        #plt.ylim(310, 330)
        plt.grid()
        plt.ylabel("Memory")

        plt.subplot(2, 1, 2)
        plt.plot(self.X_Time, self.Y_Battery, color='g', marker='o', label='Device Battery')
        plt.plot(self.X_Time, self.Y_Temperature, color='y', marker='s', label='Device Temperature')
        plt.grid(False)
        plt.legend(loc='upper right')
        plt.xlabel("Time")
        plt.ylabel("Value")

        plt.show()

    def SaveDataToCSV(self):
        csvfile = open('cpustatus.csv', 'w', encoding='utf8', newline='')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()


    def run(self):
        while self.counter > 0:
            self.getValues()
            self.counter = self.counter - 1
            time.sleep(3)

if __name__ == "__main__":
    memoryCheck = memoryCheck(10)
    memoryCheck.run()
    memoryCheck.pltgraphic()