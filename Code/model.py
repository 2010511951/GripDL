from __future__ import absolute_import
from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import MaxPooling2D,Conv2D
from keras.optimizers import adam, Adadelta,adagrad,SGD
from keras.utils import np_utils, generic_utils
from six.moves import range
from integration import acc_and_f1
import os
import csv
from keras import applications
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.metrics import binary_accuracy
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint



def Resnet50_model(round, train_data, train_label, valid_data, valid_label, test_data, test_label):

	base_model = applications.ResNet50(weights= 'imagenet',include_top=False,input_shape = train_data.shape[1:])

	add_model = Sequential()
	add_model.add(Flatten(input_shape=base_model.output_shape[1:]))
	add_model.add(Dense(128,activation='tanh'))
	add_model.add(BatchNormalization())
	add_model.add(Dropout(0.1))
	add_model.add(Dense(1,activation='sigmoid'))

	model = Model(inputs=base_model.input,outputs=add_model(base_model.output))
	

	sgd = SGD(lr = 1e-3, decay = 1e-5,momentum = 0.8,nesterov=True)
	model.compile(loss = 'binary_crossentropy', optimizer= sgd ,metrics = ['accuracy'])
	#model.summary()
	nb_epochs = 60
	hist = model.fit(train_data,train_label,batch_size=16,epochs = nb_epochs,shuffle=True,verbose=1,validation_data=(valid_data, valid_label),
                 	callbacks=[ModelCheckpoint('weight&outcome/ResNet-transferlearning2-mesoderm.model', monitor='val_acc', save_best_only=True)])


	test_predic = model.predict(test_data)
	with open("weight&outcome/prediction_mesoderm-round"+str(round)+".csv",'w') as f:
	    for i,row in enumerate(test_label):
	        f.write(str(row[0])+','+str(row[1])+','+str(row[2])+','+str(test_predic[i][0])+'\n')
	f.close()

	predict_list = []
	for i,row in enumerate(test_label):
		new_row = [row[0],row[1],row[2],test_predic[i][0]]
		predict_list.append(new_row)
	acc1, f1,gene_pairs = acc_and_f1(predict_list)
	print('test acc: ',acc1,'test f1: ',f1)

	with open("weight&outcome/Resnet50_mesoderm_prediction_integration-round"+str(round)+".csv",'w') as f:
		for edge in gene_pairs.edges:
			f.write(str(edge.geneA)+','+str(edge.geneB)+','+str(edge.groundTruth)+','+str(edge.final_pred)+'\n')
	f.close()

	# to calculate acc and f1 on the Generalization Test Set
	'''GTS_predic = model.predict(GTS_data)
	with open('GTS_predic.csv','w') as f:
		for i,row in enumerate(GTS_label):
			f.write(str(row[0])+','+str(row[1])+','+str(row[2])+','+str(GTS_predic[i])+'\n')
	f.close()

	GTS_predic_list = []
	for i,row in enumerate(GTS_label):
		new_row = [row[0],row[1],row[2],GTS_predic[i][0]]
		GTS_predic_list.append(new_row)
	acc2,f2 = acc_and_f1(GTS_predic_list)
	print('GTS acc: ',acc2,'GTS f1: ',f2)'''
	
	return acc1,f1#, acc2
