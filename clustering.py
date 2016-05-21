from skimage.io import imread, imsave
from skimage import img_as_float
from sklearn.cluster import KMeans
from math import log10
import numpy as np
from StringIO import StringIO
import logging


def PSNR(img_1, img_2):
	ssq = (img_1 - img_2)**2
	mse = np.mean(ssq)
	return 10*log10(1./mse)

def reduce_colors(image, n_clusters):

	image = img_as_float(image)
	height = len(image)
	width = len(image[0])
	image = image.reshape((height*width,3))

	image_mean = {}
	image_median = {}

	kmeans = KMeans(n_clusters = n_clusters, init='k-means++', random_state=241)
	classes = kmeans.fit_predict(image)

	means, medians = [], []
	for cl in range(n_clusters):
		means.append( np.mean(image[classes == cl], axis = 0))
		medians.append( np.median(image[classes == cl], axis = 0))
	
	image_mean = image.copy().astype(float)
	image_median = image.copy().astype(float)
	for cl in range(n_clusters):
		image_mean[classes == cl] = means[cl]
		image_median[classes == cl] = medians[cl]

	logging.info('Clusters: %s, PSNR(mean): %s, PSRN(median): %s'%(n_clusters, PSNR(image, image_mean), PSNR(image, image_median)))

	image_mean = image_mean.reshape(height,width,3)

	string_image = StringIO()
	plt.imsave(string_image, image_mean)

	return string_image
