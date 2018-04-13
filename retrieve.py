#!/usr/bin/python

import os

def get_root_folder(path):
    list_dir = path.split("/")
    if len(list_dir) == 1:
        return list_dir[0]
    else:
        return list_dir[1]

def tr_column(objs, l):
	ret = ""
	larg = 0
	for obj in objs:
		larg = len(obj) - len(obj) % 8
		ret = ret + obj
		while larg != l:
			ret = ret + "\t"
			larg += 8
	return ret

def tr_str(objs):
	return "\t\\\n\t".join(objs)

def list_columns(objs, largeur, cols=3):
	ret = ""
	res = [objs[n:n+cols] for n in range(0, len(objs), cols)]
	res = list(map(lambda x : tr_column(x, largeur),res))
	return res

def get_max_length(objs):
	m = 0
	for obj in objs:
		if len(obj) > m:
			m = len(obj)
	m = m + 8 - m % 8
	return m

def retrieve_filelist(path, extension):
	ret = []
	larg = 0
	for root, directories, filenames in os.walk(path):
		for filename in filenames:
			if filename.endswith(extension) and not get_root_folder(root) == "libft":
				ret.append(root + "/" + filename)
	larg = get_max_length(ret)
	return list_columns(ret, larg)


if __name__ == "__main__":
	print(retrieve_filelist(".", ".c"))
