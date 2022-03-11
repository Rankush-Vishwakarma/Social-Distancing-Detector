# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 16:07:33 2022

@author: rvishwakar23
"""


# import the necessary packages
from detection import Detection
from scipy.spatial import distance as dist
import numpy as np
import argparse
import pyautogui
import imutils
import cv2
import os
import csv
#from tkinter import *
from tkinter import messagebox
from loggingModule import makeLog
from time import time 

class Detector:
    def __init__(self):
        self.__weightsPath = 'yolov3.weights'
        self.__configPath = 'yolov3.cfg'
        self.__coco_names = 'coco.names'
        self.__title = ['confidence','bounding box','centroid']
        self.__title2 = ['Total number of Peoples','Violated People','Non-infected People']
        self.__FrameData = []
        self.__PeopleData = []
        self.__log = makeLog()
        try:
            self.__detection = Detection()
            self.__log.info('Detection module working fine.')
        except Exception as e:
            self.__log.error(str(e))
        
    def __load_Yolo(self) -> tuple:
        try:
            self.__log.info("loading YOLO from disk")
            net = cv2.dnn.readNetFromDarknet(self.__configPath, self.__weightsPath)
            try:
                # check if we are going to use GPU
                if self.__detection.USE_GPU:
                	# set CUDA as the preferable backend and target
                	#print("[INFO] setting preferable backend and target to CUDA...")
                    self.__log.info('setting preferable backend and target to CUDA.')
                    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) 
                    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                # determine only the *output* layer names that we need from YOLO
                ln = net.getLayerNames()
                ln =  [layerName for layerName in net.getUnconnectedOutLayersNames()]
                self.__log.info('Model and Corresponding layers have been sucessfully loaded.')
                return net, ln
            except Exception as e:
                self.__log.debug(e)
        except Exception as e:
            self.__log.error(e)
    
    def __SaveDate(self, __title,__dataset,fileName):
      try:
          self.__log.info('SaveDate Saving data into dataset.csv file')
          with open(f'dataset/{fileName}.csv','w') as f:
              write = csv.writer(f) 
              write.writerow(__title) 
              write.writerows(__dataset)
              self.__log.info('SaveDate Data saved successfully.')
      except Exception as e:
          self.__log.debug('SaveDate Something went wrong '+str(e))
          pass
            
    def __writeFrame(self,frame, outputVideoFile , writer = None  ):
        try:
            if outputVideoFile != "" and writer is None:
        		# initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG") 
                writer = cv2.VideoWriter(outputVideoFile, fourcc, 25,
        			(frame.shape[1], frame.shape[0]), True)
        	# if the video writer is not None, write the frame to the output
        	# video file
            if writer is not None:
                writer.write(frame)
            self.__log.info(f'Writing frame in {outputVideoFile}')
        except Exception as e:
            self.__log.error(e)
            
    
            
    def social_distance_detector(self,inputVideo:str, outputVideoFileName:str, display = True):
        #inputVideo = 'video.mp4'
        #output = 'testing.avi'
        #display = 1
        # load the COCO class labels our YOLO model was trained on
        #labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
        startTime = time()
        outputVideoFile = 'output/'+outputVideoFileName+'.avi'
        #LABELS = open('coco.names').read().strip().split("\n")
        LABELS = open(self.__coco_names).read().strip().split("\n")
       
        # load our YOLO object detector trained on COCO dataset (80 classes)
        
        circles = 0
        net , ln = self.__load_Yolo()
        
        # initialize the video stream and pointer to output video file
        self.__log.info("accessing video stream")
        try:
            vs = cv2.VideoCapture(inputVideo)
            writer = None
            self.__log.info('video frame capturing started sucesssfully')
        except Exception as e:
            self.__log.debug(e)
            # loop over the frames from the video stream
        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()
            # if the frame was not grabbed, then we have reached the end
            # of the stream
            if not grabbed:
                self.__log.debug('capturing the frame return nothing')
                break
            # resize the frame and then detect people (and only people) in it
            frame = imutils.resize(frame, width=700)
            try:
                results = self.__detection.detect_people(frame, net, ln,
                                                  personIdx=LABELS.index("person"))
                self.__log.info('Detected person in the frame successfully')
            except Exception as e:
                self.__log.error(e)
            #dataset.append(results)
            # initialize the set of indexes that violate the minimum social
        	# distance
            violate = set()
            
            self.__FrameData.append(results[0])
            self.__FrameData.append(results[1])
            self.__FrameData.append(results[2])
            self.__SaveDate(self.__title,self.__FrameData,'FrameData')
        
        	# ensure there are *at least* two people detections (required in
        	# order to compute our pairwise distance maps)
            if len(results) >= 2:
                # extract all centroids from the results and compute the
        		# Euclidean distances between all pairs of the centroids
                centroids = np.array([r[2] for r in results])
                D = dist.cdist(centroids, centroids, metric="euclidean")
        		# loop over the upper triangular of the distance matrix
                for i in range(0, D.shape[0]):
                    for j in range(i + 1, D.shape[1]):
        				# check to see if the distance between any two
        				# centroid pairs is less than the configured number
        				# of pixels
                        if D[i, j] < self.__detection.MIN_DISTANCE:
        					# update our violation set with the indexes of
        					# the centroid pairs
                            violate.add(i)
                            violate.add(j)
            # loop over the results
            for (i, (prob, bbox, centroid)) in enumerate(results):
        		# extract the bounding box and centroid coordinates, then
        		# initialize the color of the annotation
                (startX, startY, endX, endY) = bbox
                (cX, cY) = centroid
                color = (0, 255, 0)
        
        		# if the index pair exists within the violation set, then
        		# update the color
                if i in violate: 
                    color = (0, 0, 255)
        
        		# draw (1) a bounding box around the person and (2) the
        		# centroid coordinates of the person,
                #cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                cv2.circle(frame, (cX, cY), 3, color, -1)
                circles += 1
                
            #oldPeople = circles
        	# draw the total number of social distancing violations on the
        	# output frame
            people = f'Total number of Peoples: {circles}' 
            cv2.putText(frame, people, (10, frame.shape[0] - 5),
        		cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
            text = f"Social Distancing Violations: {len(violate)}" 
            cv2.putText(frame, text, (10, frame.shape[0] - 30),
        		cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            safePeople = f"Non-infected brave peoples: {abs(len(violate) - circles)}"
            cv2.putText(frame, safePeople, (10, frame.shape[0] - 55),
        		cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255,0), 2)
            
            self.__PeopleData.append([circles,len(violate),abs(len(violate) - circles)])
            
        
        	# check to see if the output frame should be displayed to our
        	# screen
            if display > 0:
                cv2.imshow("Social Distance Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    vs.release() 
                    cv2.destroyAllWindows()
                    self.__log.info('user quit live stream successfully')
                    break
            circles = 0    
        	# if an output video file path has been supplied and the video
        	# writer has not been initialized, do so now
            self.__writeFrame(frame, outputVideoFile , writer = None  )
            self.__SaveDate(self.__title2,self.__PeopleData,'PeopleData')
        endTime = time()
        if len(violate) > 0:
            pyautogui.alert(f"{len(violate)} poeples are in infected place")
        