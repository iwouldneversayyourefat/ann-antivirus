import os
import gc
import sys
import time
import os.path
import threading
from dir_walk import *
from predict_file import *
from delete_file import *
from output import Ui_Dialog
from process_data import PE_DATASET
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication,QMessageBox
from PyQt5.QtWidgets import QFileDialog
#from watchdog.observers import Observer
#from watchdog.events import *
import string

def predict_it(files,resultlist) :
	for file in files :
		pe_dataset = PE_DATASET(file)
		X = [pe_dataset.get_num_of_suspicious_import_func(), pe_dataset.has_embeded_pefile(),pe_dataset.get_entropy()]
		X = np.matrix(X)
		rows = X.shape[0]
		X = np.insert(X, 0, values = np.ones(rows), axis = 1)
		prediction = predict(theta,X)[0]
		del(pe_dataset)
		gc.collect()
		resultlist.addItem(file + " | " + str("可能存在风险" if prediction else "无风险"))



# class FileEventHandler(FileSystemEventHandler):
# 	def __init__(self):
# 		FileSystemEventHandler.__init__(self)

# 	def on_moved(self, event):
# 		if event.is_directory:
# 			print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
# 		else:
# 			print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

# 	def on_created(self, event):
# 		if event.is_directory:
# 			print("directory created:{0}".format(event.src_path))
# 		else:
# 			print("file created:{0}".format(event.src_path))

# 	def on_deleted(self, event):
# 		if event.is_directory:
# 			print("directory deleted:{0}".format(event.src_path))
# 		else:
# 			print("file deleted:{0}".format(event.src_path))

# 	def on_modified(self, event):
# 		if event.is_directory:
# 			print("directory modified:{0}".format(event.src_path))
# 		else:
# 			gc.collect()
# 			pe_dataset = PE_DATASET(event.src_path)
# 			X = [pe_dataset.get_num_of_suspicious_import_func(), pe_dataset.has_embeded_pefile(),pe_dataset.get_entropy()]
# 			X = np.matrix(X)
# 			rows = X.shape[0]
# 			X = np.insert(X, 0, values=np.ones(rows), axis=1)
# 			prediction = predict(theta, X)[0]
# 			del(pe_dataset)
# 			gc.collect()
# 			if(prediction):
# 				force_del(event.src_path)
# 				print("发现恶意程序，已删除")

class AppWindow(QDialog) :

	def __init__(self) :	
		super().__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.show()
		self.ui.select_file.clicked.connect(self.select_file_Click)
		self.show()
		self.ui.select_folder.clicked.connect(self.select_folder_Click)
		self.show()
		self.ui.delete_selected.clicked.connect(self.remove_selected_file)
		self.show()

	def select_file_Click(self) :
		fileName1, filetype = QFileDialog.getOpenFileName(self,"选取文件","./")
		fileName1="D:\\桌面备份\\4464.exe"
		if (not fileName1) :
			return
		tn = threading.Thread(target=predict_it, args=(fileName1,self.ui.resultlist)).start()
		self.ui.resultlist.itemClicked.connect(self.toggle_state)
		gc.collect()

	def select_folder_Click(self) :
		self.ui.resultlist.clear()
		files = []
		directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
		if (not directory1) :
			return
		for parent, dirnames, filenames in os.walk(directory1) :
			for filename in filenames :
				files.append(os.path.join(parent, filename))
		print(files)
		tn = threading.Thread(target=predict_it, args=(files,self.ui.resultlist)).start()
		self.ui.resultlist.itemClicked.connect(self.toggle_state)

	def delete_selected_Click(self) :
		print([i.text() for i in self.ui.resultlist.selectedItems()])

	def remove_item(self,item) :
		self.ui.resultlist.takeItem(self.ui.resultlist.row(item))

	def remove_selected_file(self) :
		items = []
		for x in range(0,self.ui.resultlist.count()) :
			items.append(self.ui.resultlist.item(x))
		if(not items) :
			return
		print(items)
		for item in items :
			if(item.background()==QtGui.QColor("red")) :
				self.ui.resultlist.takeItem(self.ui.resultlist.row(item))
				file = item.text()
				file = file[:(file.index("|")-1)]
				print(file)
				force_del(file)
				
	def toggle_state(self,item) :
		item.setBackground(QtGui.QColor('red') if (item.background() != QtGui.QColor('red')) else QtGui.QColor('white'))



		


if __name__ == "__main__":
	#observer = Observer()
	#event_handler = FileEventHandler()
	#observer.schedule(event_handler,"./",True)
	#observer.start()
	
	app = QApplication(sys.argv)
	w = AppWindow()
	w.show()
	sys.exit(app.exec_())
	