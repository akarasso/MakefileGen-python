import os
import re
import math
from functools import reduce

def write_var(fd, key, value):
	fd.write("{}	= {}\n\n".format(key, value))

def write_rule(fd, key, dep="", value=[]):
	fd.write("{}	: {}\n".format(key, dep))
	for v in value:
		fd.write("\t{}\n".format(v))
	fd.write("\n")
		

def list_columns(objs, cols=3):
	res = [objs[n:n+cols] for n in range(0, len(objs), cols)]
	res = list(map(lambda x: "\t" + "\t".join(x), res))
	res = "\t\\\n".join(res)
	return res

srcs = []
header = []
for root, directories, filenames in os.walk('.'):
	for filename in filenames:
		if filename.endswith('.c'):
			srcs.append(filename)
		if filename.endswith('.h'):
			header.append(filename)

projectname = input("Nom du projet: ")
projectname = projectname or "undefined"
srcdir = input("Source dir:(srcs by default) ./")
srcdir = srcdir or "srcs"
incdir = input("Header dir:(includes by default) ./")
incdir = incdir or "includes"

mf = open("Makefile", "w")
write_var(mf, "NAME", projectname)
write_var(mf, "SRCDIR", "./" + srcdir + "/")
write_var(mf, "INCDIR", "./" + incdir + "/")
write_var(mf, "CC", "gcc")
write_var(mf, "CFLAGS", "-Wall -Werror -Wextra")
write_var(mf, "SRC", "$(addprefix $(SRCDIR),$(SOURCES))")
write_var(mf, "OBJ", "$(SRC:.c=.o)")
write_var(mf, "SOURCES", list_columns(srcs))

write_rule(mf, "all", "$(NAME)", [""])
write_rule(mf, "%.o", "%.c", ["$(CC) $(CFLAGS) -I$(INCDIR) -c -o $@ $<"])
write_rule(mf, "$(NAME)", "$(OBJ)")
write_rule(mf, "clean", "", ["rm -f $(OBJ)"])
write_rule(mf, "fclean", "clean" , ["rm -f $(NAME)"])
write_rule(mf, "re", "fclean all")
