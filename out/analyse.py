'''
Script computes clone similarity!
'''

import csv
import os
import sys
import numpy as np
import subprocess
import json
import bisect
import multiprocessing as mp
import time
import store
import shutil


releases = []
LOCs = []
DIR = "../usr/jquery-data/"

def cleanDir(path):
    print("Cleaning %s" % path)
    if not (len(path) == 0 or path[-1] == '/'):
        raise ValueError('%s is not a valid path' % path)
    for root, dirs, files in os.walk(path):
        for name in files:
            if (not name.endswith(".js")) or (name.endswith(".min.js")):
                assert os.path.exists(path + name)
                os.remove(path + name)
        for directory in dirs:
            if directory in ['dist', 'test', 'build']:
                assert os.path.exists(path + directory)
                shutil.rmtree(path + directory)
            else:
                cleanDir(path + directory + '/')

def release(path):
    without_dir = path[len(DIR):path.index("/", len(DIR))]

class Segments:
    segments = []

    def add(self, seg):
        if not self.segments:
            self.segments = seg.copy()
        else:
            index_left = bisect.bisect_left(self.segments, seg[0])
            index_right = bisect.bisect_right(self.segments, seg[1])
            if index_left % 2 == 0 and index_right % 2 == 0:
                del self.segments[index_left:index_right]
                self.segments.insert(index_left, seg[1])
                self.segments.insert(index_left, seg[0])
            if index_left % 2 == 1 and index_right % 2 == 0:
                del self.segments[index_left:index_right]
                self.segments.insert(index_left, seg[1])
            if index_left % 2 == 1 and index_right % 2 == 1:
                del self.segments[index_left:index_right]
            if index_left % 2 == 0 and index_right % 2 == 1:
                del self.segments[index_left:index_right]
                self.segments.insert(index_left, seg[0])
    
    def lines(self):
        c = 0
        for i in range(len(self.segments)//2):
            c += (self.segments[2*i+1] - self.segments[2*i] + 1)
        return c

    def __str__(self):
        strings = []
        if self.segments:
            for i in range(len(self.segments)//2):
                strings.append(str([self.segments[2*i], self.segments[2*i+1]]))
        return ", ".join(strings)
       

def CalculateCloneSegments(json_object):
    lines = {}
    for item in json_object:
        for instance in item['instances']:
            segments = lines.get(instance['path'], None)
            if segments:
                segments.add(instance['lines'])
            else:
                segments = Segments()
                segments.add(instance['lines'])
                lines[instance['path']] = segments

    return sum(lines[path].lines() for path in lines)

def RunJsInspect(result_queue, command, i_1, i_2):
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    string = result.stdout.decode('utf-8')
    parsed = json.loads(string)
    Cij = CalculateCloneSegments(parsed)
    result_queue.put( (i_1, i_2, Cij ))


if __name__ == "__main__":
    START_TIME = time.time()
    if (len(sys.argv) <= 1):
        raise ValueError("Not enough arguments")
    t_parameter = str(sys.argv[1])

    with open(DIR + 'jquery_releases.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            releases.append(row)
    
    print("\nFOUND %d RELEASES" % len(releases))
    
    #releases = releases[:6]
    # tmp = releases.copy()#[:3]
    # releases = [tmp[0]]
    # releases.append(tmp[14])

    RESULTS = store.Results()
    LOCs = store.LOCStore()

    RESULT_QUEUE = mp.Queue()
    try:
        print("\nCLEANING CODE\n")
        
        for release in releases:
            cleanDir(DIR[2:] + release['tag'] + '/src/')

        print("\nCOUNTING LINES OF JAVASCRIPT PER RELEASE\n")

        for release in releases:
            #cloc --json 1.0
            if LOCs.get(release['tag']) == None:
                #cloc --json 1.0
                path = DIR + release['tag'] + '/src'
                result = subprocess.run('cloc --json "' + path + '"', stdout=subprocess.PIPE, shell=True)
                string = result.stdout.decode('utf-8')
                parsed = json.loads(string)
                JSlines = parsed['JavaScript']['code'] + parsed['JavaScript']['comment'] + parsed['JavaScript']['blank'] #TODO do we need all this?
                LOCs.add(release['tag'], JSlines)


        print("\nCOMPUTING PAIRWISE SIMILARITY\n")

        QUEUE = []
        for i_1, release_1 in enumerate(releases):
            for i_2, release_2 in enumerate(releases[:i_1]):
                if RESULTS.has(release_1['tag'], release_2['tag']):
                    continue
                path_1 = DIR + release_1['tag'] + '/src'
                path_2 = DIR + release_2['tag'] + '/src'
                command = 'jsinspect -t ' + t_parameter + ' -r json --truncate 1 "' + path_1 + '" "' + path_2 + '"'
                QUEUE.append( (command, i_1, i_2) )
        
        np.random.shuffle(QUEUE) # To expose fatal errors more quickly, hopefully
        
        PROCESSES = []
        while QUEUE:
            cmd, i_1, i_2 = QUEUE.pop(0)
            p = mp.Process(target=RunJsInspect, args=(RESULT_QUEUE, cmd, i_1, i_2,))
            PROCESSES.append(p)
        
        RUNNING_PROCESSES = []

        NUM_SEQ = 10

        while PROCESSES or RUNNING_PROCESSES:
            print("%d running, %d to go." % (len(RUNNING_PROCESSES), len(PROCESSES)))
            if len(RUNNING_PROCESSES) >= NUM_SEQ or not PROCESSES:
                p = RUNNING_PROCESSES.pop(0)
                p.join()
            else:
                p = PROCESSES.pop(0)
                p.start()
                RUNNING_PROCESSES.append(p)
    except Exception as e:
        if isinstance(e, json.decoder.JSONDecodeError):
            print("\n\nDECODE ERROR")
        raise e
    finally:
        while not RESULT_QUEUE.empty():
            (i, j, Cij ) = RESULT_QUEUE.get()
            tag_i = releases[i]['tag']
            tag_j = releases[j]['tag']
            metric = Cij / (LOCs.get(tag_i) + LOCs.get(tag_j))
            RESULTS.add(tag_i, tag_j, metric)
            print("Calculated metric: %3.6f between %s and %s" % (metric, tag_i, tag_j))
        
        RESULTS.save()
        LOCs.save()

        print("\n\nSAVED metrics and LOCs\n\n")

    print("\nDONE AFTER %4.2f SECS" % (time.time() - START_TIME))


    # FALLBACK CODE for non-multiprocess
    # for i_1, release_1 in enumerate(releases):
    #     for i_2, release_2 in enumerate(releases[:i_1]):
    #         print("\n\n RUNNING %d AND %d" % (i_1, i_2))
    #         path_1 = DIR + release_1['tag'] + '/src'
    #         path_2 = DIR + release_2['tag'] + '/src'
    #         result = subprocess.run('jsinspect -t ' + t_parameter + ' -r json "' + path_1 + '" "' + path_2 + '"', stdout=subprocess.PIPE, shell=True)
    #         string = result.stdout.decode('utf-8')
    #         parsed = json.loads(string)
    #         print("\n\n DONE %d AND %d" % (i_1, i_2))
    #         Cij = CalculateCloneSegments(parsed)
    #         metric = Cij / (LOCs[i_1] + LOCs[i_2])
    #         RESULT[i_1, i_2] = metric
    #         print("Calculated metric: %3.6f" % metric)
