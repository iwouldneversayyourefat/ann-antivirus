#coding=utf-8
import os


def force_del(filename) :
	print("是否删除可疑文件\n")
	try :
		fsize = os.path.getsize(filename)
		with open(filename, 'rb+') as f :
			for _ in range(3) :
				f.seek(0,0)
				f.write(os.urandom(fsize))
		os.remove(filename)
	except Exception as err :
		print(filename, str(err))
