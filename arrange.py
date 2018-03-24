#!/usr/bin/python

import os
import shutil

def get_root_folder(path):
	list_dir = path.split("/")
	if len(list_dir) == 1:
		return list_dir[0]
	else:
		return list_dir[1]

def create_prog_dir(dirs):
	miss = []
	cont = ""
	for directory in dirs:
		if not os.path.isdir(directory):
			miss.append(directory)
			os.mkdir(directory)
	if len(miss) > 0:
		print("Dir {} are missing..".format(", ".join(miss)))
		while not (cont == "y" or cont == "n"):
			cont = input("Continue(Y/n):")
			cont = cont or "y"
		if cont == "y":
			return 0
	return len(miss)

def is_good_arrange_file(path, filename):
	if filename.endswith('.c') and not get_root_folder(path) == "srcs":
		return False
	elif filename.endswith('.h') and not get_root_folder(path) == "includes":
		return False
	elif filename.endswith('.a') and not get_root_folder(path) == "libs":
		return False
	return True

def file_reorder(list_f):
	for f in list_f:
		if f.endswith('.c'):
			try:
				shutil.move(f, "./srcs")
			except Exception as e:
				print(e)
				return False
		if f.endswith('.h'):
			try:
				shutil.move(f, "./includes")
			except Exception as e:
				print(e)
				return False
		if f.endswith('.a'):
			try:
				shutil.move(f, "./libs")
			except Exception as e:
				print(e)
				return False
	return True

def is_good_arrange(path, dirs, exclude = []):
	badfiles = []
	cont = ""
	for root, directories, filenames in os.walk(path):
		for filename in filenames:
			if not is_good_arrange_file(root, filename) and not filename in exclude:
				badfiles.append(root + "/"  + filename)
	if len(badfiles) > 0:
		for f in badfiles:
			print("This file shouldn't be here :{}".format(f))
		while not (cont == "y" or cont == "n"):
			cont = input("Reorder files(Y/n):")
			cont = cont or "y"
		if cont == "y":
			if file_reorder(badfiles) == False:
				return False
			clean_empty_dir(path, dirs)
			return True
		return False
	clean_empty_dir(path, dirs)
	if len(badfiles) == 0:
		return True
	return False

def clean_empty_dir(path, dirs):
	n = 1
	while n > 0:
		n = 0 
		for root, directories, filenames in os.walk(path):
			for d in directories:
				if len(os.listdir(root + "/" + d)) == 0 and not d in dirs:
					os.rmdir(root + "/" + d)
					n += 1

if __name__ == "__main__":
	dirs = ["srcs", "libs", "includes"]
	if create_prog_dir(dirs) == 0:
		if is_good_arrange(".", dirs):
			print ("Folder good arrange")
		else:
			print ("Folder not good arrange")
