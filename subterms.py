#!/usr/bin/python
# --coding: utf-8 --

# import sys, pysrt, yomichan
import pickle

def save_data(stLineNumber, stTermStart, stTermEnd):
    file = open("state_zxc", 'w')
    data = {'stLineNumber': stLineNumber, 'stTermStart': stTermStart, 'stTermEnd': stTermEnd}
    pickle.dump(data, file)
    file.close()

def restore_data():
    file = open("state_zxc", 'r')
    data = pickle.load(file)
    file.close()
    #print "file closed"
    stLineNumber = data['stLineNumber']
    stTermStart = data['stTermStart']
    stTermEnd = data['stTermEnd']
    return stLineNumber, stTermStart, stTermEnd



