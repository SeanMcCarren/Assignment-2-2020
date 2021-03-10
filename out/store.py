import subprocess
import json



class LOCStore:
    def __init__(self, DIR = ''):
        self.DIR = DIR
        self.DONE = {}
        try:
            with open(self.DIR + 'LOCs.txt', mode='r') as f:
                lines = f.readlines()
            for line in lines:
                spl = line.split(",")
                self.DONE[spl[0]] = int(spl[1])
        except FileNotFoundError:
            pass
    
    def get(self, release):
        return self.DONE.get(release, None)
    
    def add(self, release, lines):
        self.DONE[release] = lines
    
    def save(self):
        with open(self.DIR + 'LOCs.txt', mode='w+') as f:
            for key in self.DONE:
                LOC = self.DONE[key]
                f.write(key + ',' + str(LOC) + '\n')

class Results:
    def __init__(self, DIR = ''):
        self.DIR = DIR
        self.DONE = {}
        try:
            with open(self.DIR + 'results.txt', mode='r') as f:
                lines = f.readlines()
            for line in lines:
                spl = line.split(",")
                key = self.__key__(spl[0], spl[1])
                self.DONE[key] = float(spl[2])
        except FileNotFoundError:
            pass
    
    def __key__(self, v1, v2):
        if v1 < v2 :
            return v1 + "," + v2
        else :
            return v2 + "," + v1

    def add(self, ver1, ver2, metric):
        key = self.__key__(ver1, ver2)
        self.DONE[key] = metric
    
    def has(self, ver1, ver2):
        key = self.__key__(ver1, ver2)
        result = self.DONE.get(key, None)
        return result != None
    
    def get(self, ver1, ver2):
        if self.has(ver1, ver2) == False:
            raise IndexError
        key = self.__key__(ver1, ver2)
        return self.DONE[key]

    def save(self):
        with open(self.DIR + 'results.txt', mode='w+') as f:
            for key in self.DONE:
                metric = self.DONE[key]
                f.write(key + ',' + str(metric) + '\n')

