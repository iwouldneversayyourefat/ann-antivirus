#coding=utf-8
import os
import os.path
from predict_file import *
from process_data import PE_DATASET
from delete_file import *
import threading
import time
import gc

result = []

def predict_it(file) :
	pe_dataset = PE_DATASET(file)
	X = [pe_dataset.get_num_of_suspicious_import_func(), pe_dataset.has_embeded_pefile()]
	X = np.matrix(X)
	rows = X.shape[0]
	X = np.insert(X, 0, values = np.ones(rows), axis = 1)
	prediction = predict(theta,X)[0]
	del(pe_dataset)
	gc.collect()
	result.append([file,prediction])


def dir_walk(dir) :
	files = []
	threads = []

	for parent,dirnames,filenames in os.walk(dir) :
		for filename in filenames :   
			files.append(os.path.join(parent, filename))

	for file in files :
		tn = threading.Thread(target = predict_it, args = (file,))
		threads.append(tn)

	for t in threads :
		t.setDaemon(True)
		t.start()

	is_scanning = 1
	while (is_scanning) :
		r = 0
		for t in threads :
			r += int(t.is_alive())
		is_scanning = is_scanning and r

	return result

