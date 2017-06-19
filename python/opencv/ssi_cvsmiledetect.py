'''
ssi_cvsmiledetect.py
author: Johannes Wagner <wagner@hcm-lab.de>
created: 2016/04/15
Copyright (C) University of Augsburg, Lab for Human Centered Multimedia

Smile detection.
'''

import cv2
import numpy as np


def getOptions(opts,vars):
    
    opts['model:dir'] = 'data/haarcascades/'
    opts['model:ext'] = '.xml'
    opts['model:face'] = 'haarcascade_frontalface_default'
    opts['model:smile'] = 'haarcascade_smile'


def getImageFormatOut(format, opts, vars): 
  
    vars['gray'] = np.zeros((format.height,format.width,1), np.uint8)

    return format
    

def transform_enter(ssrc, sdst, sxtra, board, opts, vars):

    vars['face_cascade'] = 	cv2.CascadeClassifier(opts['model:dir'] + opts['model:face'] + opts['model:ext'])
    vars['smile_cascade'] = cv2.CascadeClassifier(opts['model:dir'] + opts['model:smile'] + opts['model:ext'])


def transform(info, ssrc, sdst, sxtra, board, opts, vars):   

    img_src = np.asarray(ssrc)
    img_dst = np.asarray(sdst)
    np.copyto(img_dst, img_src)

    img_gray = vars['gray']
    face_cascade = vars['face_cascade']
    smile_cascade = vars['smile_cascade']

    cv2.cvtColor(img_src, cv2.COLOR_RGB2GRAY, img_gray)	
    faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img_dst, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = img_gray[y:y+h, x:x+w]
        roi_dst = img_dst[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 
                                                scaleFactor = 1.3,
                                                minNeighbors = 22,
                                                minSize = (25, 25),
                                                flags=cv2.CASCADE_SCALE_IMAGE)        
        for (sx,sy,sw,sh) in smiles:            
            cv2.rectangle(roi_dst, (sx,sy), (sx+sw, sy+sh), (0,255,0), 2)
