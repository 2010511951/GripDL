import os 
import csv
import numpy as np
from PIL import Image
import random

def read_image(img_url):

    #arr1 = np.zeros((128,320,1),dtype="float64")
    #img = Image.open(img_url).convert('L')
    img = Image.open(img_url)
    arr1 = np.asarray(img,"float64")
    '''arr_out[0, :, :] = arr1[:, :, 0]
    arr_out[1, :, :] = arr1[:, :, 1]
    arr_out[2, :, :] = arr1[:, :, 2]'''


    return arr1

def find_image_group(gene_images,gene):

    img_lateral = []
    img_dorsal = []
    img_ventral = []

    for row in gene_images:
        if row[6]=='6' and (row[0]==gene or row[1]==gene or row[2]==gene or row[3]==gene):
        	if row[7]=='lateral':
        		img_name = str(str(str(row[5]).split('/')[-1]).split('.')[0]).split('u')[-1]+'_s.bmp'
        		#print('lateral',img_name)
        		img_lateral.append(img_name)
        	if row[7]=='dorsal':
        		img_name = str(str(str(row[5]).split('/')[-1]).split('.')[0]).split('u')[-1]+'_s.bmp'
        		#print('dorsal',img_name)
        		img_dorsal.append(img_name)
        	if row[7]=='ventral':
        		img_name = str(str(str(row[5]).split('/')[-1]).split('.')[0]).split('u')[-1]+'_s.bmp'
        		#print('ventral',img_name)
        		img_ventral.append(img_name)

    return [img_lateral,img_dorsal,img_ventral]


def load_image(set):

	gene_images = []
	with open('gene_images.csv','r') as f:
		reader = csv.reader(f)
		for row in reader:
			gene_images.append(row)
	f.close()

	print('	Generating image pairs...')
	image_pairs = []
	database_path = '/data/flyexpress/DL_biomedicine_image/data/pic_data/'
	for row in set:
		label = row[2]
		gene1 = row[0]
		gene2 = row[1]
		g1_batch = find_image_group(gene_images,gene1)
		g2_batch = find_image_group(gene_images,gene2)
		for i in range(3):
			for p in range(len(g1_batch[i])):
				for q in range(len(g2_batch[i])):
					try:
						Image.open(database_path + g1_batch[i][p])
						Image.open(database_path + g2_batch[i][q])
						image_pair = [g1_batch[i][p],g2_batch[i][q],label]
						image_pairs.append(image_pair)
						#print(image_pair)
					except Exception,e:
						continue
					#print([g1_batch[i][p],g2_batch[i][q],label])
	random.shuffle(image_pairs)
	print('	Image pair list is ready: '+str(len(image_pairs)))
	print('	Read images...')
	
	data = np.empty((len(image_pairs),256,320,3),dtype="float64")
	label = np.empty((len(image_pairs),1),dtype="float64")
	for i,row in enumerate(image_pairs):
		label[i,0] = row[2]
		data[i,0:128,:,:] = read_image(database_path + row[0])
		data[i,128:256,:,:] = read_image(database_path + row[1])
		#print('image pair ' + str(i+1) + ' has been read.   Progress: ' + str(((i + 1) * 100) / len(image_pairs)) + '%')
	
	return data,label
		
def load_image_for_test_set(set):

	gene_images = []
	with open('gene_images.csv','r') as f:
		reader = csv.reader(f)
		for row in reader:
			gene_images.append(row)
	f.close()

	print('	Generating image pairs...')
	image_pairs = []
	database_path = '/data/flyexpress/DL_biomedicine_image/data/pic_data/'
	for row in set:
		label = [row[0],row[1],row[2]]
		gene1 = row[0]
		gene2 = row[1]
		g1_batch = find_image_group(gene_images,gene1)
		g2_batch = find_image_group(gene_images,gene2)
		for i in range(3):
			for p in range(len(g1_batch[i])):
				for q in range(len(g2_batch[i])):
					try:
						Image.open(database_path + g1_batch[i][p])
						Image.open(database_path + g2_batch[i][q])
						image_pair = [g1_batch[i][p],g2_batch[i][q],label]
						#print(image_pair)
						image_pairs.append(image_pair)
					except Exception,e:
						continue
					
					#print([g1_batch[i][p],g2_batch[i][q],label])
	random.shuffle(image_pairs)
	print('	Image pair list is ready: '+str(len(image_pairs)))
	print('	Read images...')
	
	data = np.empty((len(image_pairs),256,320,3),dtype="float64")
	label = []
	for i,row in enumerate(image_pairs):
		new_label = row[2]
		label.append(new_label)
		data[i,0:128,:,:] = read_image(database_path + row[0])
		data[i,128:256,:,:] = read_image(database_path + row[1])
		#print('image pair ' + str(i+1) + ' has been read.   Progress: ' + str(  (i + 1)*100/len(image_pairs) ) + '%')
	
	return data,label

def load_data(train_set,valid_set,test_set):

	train_data, train_label = load_image(train_set)
	print('train-set has beed loaded!')
	valid_data, valid_label = load_image(valid_set)
	print('valid-set has been loaded!')
	test_data, test_label = load_image_for_test_set(test_set)
	print('test-set has been loaded!')
	'''GTS_data, GTS_label = load_image_for_test_set(GTS_set)
	print('GTS_set has been loaded!')'''

	'''train_data /= 255.0
	valid_data /= 255.0
	test_data /= 255.0
	GTS_data /= 255.0'''

	return train_data, train_label, valid_data, valid_label, test_data, test_label#, GTS_data, GTS_label

