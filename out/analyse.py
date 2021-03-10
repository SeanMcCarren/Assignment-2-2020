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


releases = []
LOCs = []
DIR = "../usr/jquery-data/"

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

if __name__ == "__main__":
    assert len(sys.argv) > 1
    t_parameter = str(sys.argv[1])

    with open(DIR + 'jquery_releases.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            releases.append(row)
    
    print("\nFOUND %d RELEASES" % len(releases))
    
    # tmp = releases.copy()#[:3]
    # releases = [tmp[0]]
    # releases.append(tmp[14])

    RESULT = np.empty((len(releases),len(releases)), dtype=float)

    print("\nCOUNTING LINES OF JAVASCRIPT PER RELEASE\n")

    for release in releases:
        #cloc --json 1.0
        path = DIR + release['tag'] + '/src'
        result = subprocess.run('cloc --json "' + path + '"', stdout=subprocess.PIPE, shell=True)
        string = result.stdout.decode('utf-8')
        parsed = json.loads(string)
        JSlines = parsed['JavaScript']['code'] + parsed['JavaScript']['comment'] + parsed['JavaScript']['blank'] #TODO do we need all this?
        LOCs.append(JSlines)
        print("File %s: %d" % (path, JSlines))


    print("\nCOMPUTING PAIRWISE SIMILARITY\n")

    for i_1, release_1 in enumerate(releases):
        for i_2, release_2 in enumerate(releases[:i_1]):
            print("\n\n RUNNING %d AND %d" % (i_1, i_2))
            path_1 = DIR + release_1['tag'] + '/src'
            path_2 = DIR + release_2['tag'] + '/src'
            result = subprocess.run('jsinspect -t ' + t_parameter + ' -r json "' + path_1 + '" "' + path_2 + '"', stdout=subprocess.PIPE, shell=True)
            string = result.stdout.decode('utf-8')
            parsed = json.loads(string)
            print("\n\n DONE %d AND %d" % (i_1, i_2))
            Cij = CalculateCloneSegments(parsed)
            metric = Cij / (LOCs[i_1] + LOCs[i_2])
            RESULT[i_1, i_2] = metric
            print("Calculated metric: %3.6f" % metric)

