# this program aims to calculate the prediction accuracy based on gene-pair, using max method
# namely, the highest score will be accepted as the final prediction score for the gene pair

import os
import csv
import string

# to define a class named 'edge' and a daughter class 'edge_set'


def weight_f(x):
	#print(2*abs(x-0.5))
	return 2-4*abs(x-0.5)


class one_edge:

	
	def __init__(self,A,B,truth):
		self.geneA = A
		self.geneB = B
		self.groundTruth = truth
		self.predictions = []
		self.final_pred = 0
		self.TP = 0
		self.TN = 0
		self.FP = 0
		self.FN = 0


	def is_prediction_right(self):

		self.final_pred = 0.0
		#for ele in self.predictions:
			#self.final_pred += ele*weight_f(ele)
		self.final_pred = sum(self.predictions)/len(self.predictions)
		#self.final_pred = max(self.predictions)
		if ( self.final_pred > 0.5 and self.groundTruth == 1) or ( self.final_pred < 0.5 and self.groundTruth == 0):
			return 1
		else:
			return 0


	def f1_preparing(self):

		self.final_pred = 0.0
		#for ele in self.predictions:
			#self.final_pred += ele*weight_f(ele)
		self.final_pred = sum(self.predictions)/len(self.predictions)
		#self.final_pred = max(self.predictions)
		if self.final_pred >0.5 and self.groundTruth == 1:
			self.TP = 1
		if self.final_pred >0.5 and self.groundTruth == 0:
			self.FP = 1
		if self.final_pred <0.5 and self.groundTruth == 1:
			self.FN = 1
		if self.final_pred <0.5 and self.groundTruth == 0:
			self.TN = 1

		return self.TP,self.FP,self.FN,self.TN

 	def display(self):
 		print(self.geneA,self.geneB,self.groundTruth,self.final_pred)


class edges_set:

	def __init__(self):
		self.edges = []

	def add(self,edge):
		for ele in self.edges:
			if edge.geneA == ele.geneA and edge.geneB == ele.geneB:
				ele.predictions.append(edge.predictions[0])
				return
		self.edges.append(edge)
		return 

	def total_accuracy(self):
		suc = 0.0
		for ele in self.edges:
			suc += ele.is_prediction_right()
		return suc/len(self.edges)


	def F1_calculating(self):
		tp_total = 0
		fp_total = 0
		fn_total = 0
		tn_total = 0
		for edge in self.edges:
			TP,FP,FN,TN = edge.f1_preparing()
			tp_total += TP
			fp_total += FP
			fn_total += FN
			tn_total += TN
		#print('sum',tp_total+fp_total+fn_total+tn_total)
		print('FP',fp_total)
		print('TP',tp_total)
		print('FN',fn_total)
		print('TN',tn_total)
		return 2*float(tp_total)/float(2*tp_total+fp_total+fn_total)

	def display(self):
		for ele in self.edges:
			ele.display()

# to import the csv file of the predictions


def acc_and_f1(predict_list):

	
	gene_pairs = edges_set()

	'''with open(file_path,'r') as f:
		reader = csv.reader(f)
		for row in reader:
			A = str(row[0])
			B = str(row[1])
			truth = string.atof(row[2])
			prediction = string.atof( str(row[3][1:-1]) )
			new_edge = one_edge(A,B,truth)
			new_edge.predictions.append(prediction)
			#new_edge.display()
			gene_pairs.add(new_edge)

	f.close()'''
	for row in predict_list:
		A = str(row[0])
		B = str(row[1])
		truth = row[2]
		#prediction = string.atof( str(row[3][1:-1]) )
		prediction = row[3]
		new_edge = one_edge(A,B,truth)
		new_edge.predictions.append(prediction)
		#new_edge.display()
		gene_pairs.add(new_edge)

	# to calculate the overall accuracy of predictions based on max method
	#gene_pairs.display()
	#print('edges: '+str(len(gene_pairs.edges)))
	acc = gene_pairs.total_accuracy()
	#print('accuracy: ',acc)
	f1= gene_pairs.F1_calculating()
	#print('f1: ',f1)

	return acc,f1,gene_pairs