from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import random
import time
from scipy.misc import imread
from scipy.misc import imresize
import matplotlib.image as mpimg
import os
from scipy.ndimage import filters
import urllib
from PIL import Image




os.chdir('/Users/sajjad/School/ThirdYear/CSC320/a3')
gray()


act = ['Aaron Eckhart',  'Adam Sandler',   'Adrien Brody',  'Andrea Anders',    'Ashley Benson',    'Christina Applegate',    'Dianna Agron',  'Gillian Anderson']


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''From:
    http://code.activestate.com/recipes/473878-timeout-function-using-threading/'''
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = default

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return False
    else:
        return it.result

testfile = urllib.URLopener()            



#Note: you need to create the uncropped folder first in order 
#for this to work

for a in act:
    name = a.split()[1].lower()
    i = 0
    for line in open("faces_subset.txt"):
        if a in line:
            filename = name+str(i)+'.'+line.split()[4].split('.')[-1]
            
            coordinates = line.split()[5].split(',')
            x1, y1, x2, y2 = [int(j) for j in coordinates]
            
            
            #A version without timeout (uncomment in case you need to 
            #unsupress exceptions, which timeout() does)
            #testfile.retrieve(line.split()[4], "uncropped/"+filename)
            #timeout is used to stop downloading images which take too long to download

            timeout(testfile.retrieve, (line.split()[4], "uncropped/"+filename), {}, 30)
            
            if os.path.isfile("uncropped/"+filename):
                try: 
                    img = array(Image.open("uncropped/"+filename))
                    img = double(img) / 255.0
                    
    #               TODO: some pictures were 2 dimensional? wat? 
                    if(len(img.shape) == 3):  
                        cropped = img[y1:y2,x1:x2,:]
                    else:
                        cropped = img[y1:y2,x1:x2]
                    
                    grey = np.zeros((cropped.shape[0], cropped.shape[1])) # init 2D numpy array
                    for rownum in range(len(cropped)):
                        for colnum in range(len(cropped[rownum])):
                            grey[rownum][colnum] = np.average(cropped[rownum][colnum])            
                                    
                    grey2 = imresize(grey, [32, 32])                            
                    imsave("cropped/"+filename, grey2) 
                except IOError:  
                    pass
            if not os.path.isfile("uncropped/"+filename):
                continue
                            
            print filename
            i += 1
