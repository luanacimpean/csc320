from pylab import *
import numpy as np
import random
import matplotlib.cbook as cbook
import random
import time
from scipy.misc import imread
from scipy.misc import imsave
from scipy.misc import imresize
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import sys

os.chdir('/Users/luanacimpean/Documents/U of T/CSC 320/Project 3')

def pca(X):
    """    Principal Component Analysis
        input: X, matrix with training data stored as flattened arrays in rows
        return: projection matrix (with important dimensions first), variance and mean.
        From: Jan Erik Solem, Programming Computer Vision with Python
        #http://programmingcomputervision.com/
    """
    
    # get dimensions
    num_data,dim = X.shape
    
    # center data
    mean_X = X.mean(axis=0)
    X = X - mean_X
    
    if dim>num_data:
        # PCA - compact trick used
        M = dot(X,X.T) # covariance matrix
        e,EV = linalg.eigh(M) # eigenvalues and eigenvectors
        tmp = dot(X.T,EV).T # this is the compact trick
        V = tmp[::-1] # reverse since last eigenvectors are the ones we want
        S = sqrt(e)[::-1] # reverse since eigenvalues are in increasing order
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        # PCA - SVD used
        U,S,V = linalg.svd(X)
        V = V[:num_data] # only makes sense to return the first num_data
    
    # return the projection matrix, the variance and the mean
    return V,S,mean_X



    

def get_digit_matrix(img_dir):

    im_files = sorted([img_dir + filename for filename in os.listdir(img_dir) if filename[-4:] == ".jpg"])
    im_shape = array((imread(im_files[0])))[:,:,0].shape[:2] # open one image to get the size 
    im_matrix = array([(imread(im_file))[:,:,0].flatten() for im_file in im_files])
    im_matrix = array([im_matrix[i,:]/1.0 for i in range(im_matrix.shape[0])])
    return (im_matrix, im_shape)
    

def get_reconstruction(V, im, mean_im):
    # altered V[i,:] to V[i,:].reshape(im_shape)
    coefs = [np.dot(V[i,:], (im-mean_im)) for i in range(V.shape[0])]
    new_im = mean_im.copy()
    for i in range(len(coefs)):
        new_im = new_im + coefs[i]*(V[i, :])
    return new_im

def get_coefs(V, im, mean_im):
    coefs = [np.dot(V[i,:], (im-mean_im)) for i in range(V.shape[0])]
    return coefs

def display_25_rand_images(im_matrix,im_shape):
    '''Display 25 components in V'''
    #gray()
    fig = figure()
    for i in range(25):
        num = random.randint(1, 767)
        im = array(im_matrix[num,:]).reshape(im_shape)
        subplot(5, 5, i+1)
        imshow(im)
        axis('off')
    savefig('randim.jpg')  
    show()
 

def display_save_25_comps(V, im_shape):
    '''Display 25 components in V'''
    figure()
    for i in range(25):
        plt.subplot(5, 5, i+1)
        plt.axis('off')
        gray()
        imshow(V[i,:].reshape(im_shape))
    savefig('display_save_25_comps.jpg')  
    show()         

def salt_and_pepper_noise(flattened_im, noise_prop):
    im = flattened_im.copy()
    pix_inds = range(len(im))
    perm_inds = np.random.permutation(pix_inds)
    
    im[perm_inds[:int(0.5*noise_prop*len(im))]] = max(im)
    im[perm_inds[int(0.5*noise_prop*len(im)):int(noise_prop*len(im))]] = min(im)
    
    return array(im)


        
def occlusion_noise(flattened_im, num_blocks, size_blocks, im_shape):
    im = flattened_im.reshape(im_shape).copy()
    max_im = max(flattened_im)
    min_im = min(flattened_im)
    for i in range(num_blocks/2):
        r_x = np.random.randint(0, im_shape[0])
        r_y = np.random.randint(0, im_shape[1])
        im[r_x:r_x+size_blocks, r_y:r_y+size_blocks] = max_im

    for i in range(num_blocks/2):
        r_x = np.random.randint(0, im_shape[0])
        r_y = np.random.randint(0, im_shape[1])
        im[r_x:r_x+size_blocks, r_y:r_y+size_blocks] = min_im

    return im.flatten()


def auto_thresh(flattened_im):
    im = flattened_im.copy()
    thr = 0.07; sorted(flattened_im)[int(len(flattened_im)*.65)]
    print(thr)
    im[where(flattened_im>thr)] = 1
    im[where(flattened_im<=thr)] = 0
    return im

#a = auto_thresh(r)
#imshow(a.reshape(im_shape))

#Download and unpack digits from :
#http://programmingcomputervision.com/downloads/pcv_data.zip

#Change this:
training_dir = '/Users/luanacimpean/Documents/U of T/CSC 320/Project 3/cropped/training/'
validation_dir = '/Users/luanacimpean/Documents/U of T/CSC 320/Project 3/cropped/validation/'
test_dir = '/Users/luanacimpean/Documents/U of T/CSC 320/Project 3/cropped/test/'

im_matrix, im_shape = get_digit_matrix(training_dir)
for i in range(im_matrix.shape[0]):
    im_matrix[i,:] = im_matrix[i,:]/255.0

V,S,mean_im = pca(im_matrix)

#Using validation set:
v_im_matrix, v_im_shape = get_digit_matrix(validation_dir)
for i in range(v_im_matrix.shape[0]):
    v_im_matrix[i,:] = v_im_matrix[i,:]/255.0

gray()
#mean_im.resize(32,32)
#imshow(mean_im)
#
#display_save_25_comps(im_matrix,im_shape)

#imshow(get_reconstruction(V[:5,], array(im_matrix[0,:]).reshape(im_shape),  mean_im))

#r = get_reconstruction(V[:200,], im_matrix[0,:],  mean_im)
#r[where(r<0)] = 0
#imshow(r.reshape((32,32)))

#i = 0
#for i in range(80):
#    r = get_reconstruction(V[:2,], v_im_matrix[i,:],  mean_im)
#    r[where(r<0)] = 0
#    imshow(r.reshape((32,32)))
#    show()

#
#training_coeffs = get_coefs(V[:2,], im_matrix[0,:],  mean_im)

# ----- PART 3 ---------
#The k values were changed from 2 to 200 to fill in the table
#min_array = []
#
#y = 0
#for y in range(im_matrix.shape[0] - 1):
#    r = get_coefs(V[:2,], im_matrix[y,:],  mean_im)
#    #change x from 1 to 10 to get the first 10 faces in validation set
#    x = 0       
#    s = get_coefs(V[:2,], v_im_matrix[x,:],  mean_im)
#    min_array.append(np.sum((array(r)-array(s))**2))
#
#print min_array.index(min(min_array))

# ----------

f = open('output.txt', 'w')

x = 0
y = 0

for x in range(v_im_matrix.shape[0] - 1):
    for k in [2, 5, 10, 20, 50, 80, 100, 150, 200]:
        min_array = []
        for y in range(im_matrix.shape[0] - 1):
            r = get_coefs(V[:k,], im_matrix[y,:],  mean_im)      
            s = get_coefs(V[:k,], v_im_matrix[x,:],  mean_im)
            min_array.append(np.sum((array(r)-array(s))**2))
            
        print >> f, x , '\t' , k , '\t' , min(min_array) , '\t' , min_array.index(min(min_array)) , '\n'


f.close()



#Problem 1
#display_25_rand_images(im_matrix, im_shape)


#Part 2
#imsave('immean.jpg',mean_im)
#display_save_25_comps(V, im_shape)
