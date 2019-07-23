import cv2
import numpy as np
from statistics import mode
import sys
import matplotlib.pyplot as plt 
import os
import time
import pandas as pd

def contornosGabarito(im):	

	#im = cv2.imread(im)
	im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
	im = cv2.GaussianBlur(im,(1,1),0)
	im = cv2.threshold(im,im.min(),255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
	edges =  cv2.Canny(im,75,200,apertureSize = 3)




	return 