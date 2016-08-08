from os import *


#create folder
def create_folder(root, name):
	directory = root +"/"+ name
	print directory
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
		except Exception, e:
			return False
		else:
			return True
		