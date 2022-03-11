# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 11:18:24 2022

@author: rvishwakar23
"""

from social_distance_detector import Detector
import sys


if __name__ == '__main__':
    detector = Detector()
    #print(sys.argv[1],sys.argv[2])
    #detector.social_distance_detector(sys.argv[1],sys.argv[2])
    filename = input('Please enter input file name - ')
    outputName = input('Please enter input file name - ')
    detector.social_distance_detector(filename,outputName)
