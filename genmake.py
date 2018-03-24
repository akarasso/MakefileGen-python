#!/usr/bin/python

import os
from arrange import *
from retrive import *

def write_var(fd, key, value):
	fd.write("{}	= {}\n\n".format(key, value))

def write_rule(fd, key, dep="", value=[]):
	fd.write("{}	: {}\n".format(key, dep))
	for v in value:
		fd.write("\t{}\n".format(v))
	fd.write("\n")

pro_type = ""
pro_name = ""

while not(pro_type == "prog" or pro_type == "lib"):
	pro_type = input("Type de projet:(PROG/lib)")
	pro_type = pro_type or "prog"
while pro_name == "":
	pro_name = input("Nom du projet: ")
	pro_name = pro_name or ""

if pro_type == "prog":
	if create_prog_dir(["srcs", "libs", "includes"]) == 0:
		is_good_arrange(".", ["includes", "srcs", "libs"])
elif pro_type == "lib":
	if create_prog_dir(["srcs", "includes"]) == 0:
		is_good_arrange(".", ["includes", "srcs"], [pro_name])
mf = open("Makefile", "w")

list_h = retrive_list(".", ".h")
list_h = tr_str(list_h)
list_src = retrive_list(".", ".c")
list_src = tr_str(list_src)
list_libs = retrive_list(".", ".a")

write_var(mf, "CC", "gcc")
write_var(mf, "CFLAGS", "-Wall -Werror -Wextra")
write_var(mf, "NAME", pro_name)
if len(list_h) > 0:
	write_var(mf, "HEADERS", list_h)
	write_var(mf, "HEADERFLAGS", "$(addprefix -I, $(dir $(HEADERS)))")
if pro_type == "prog":
	write_var(mf, "LIBS", tr_str(list_libs))
else:
	if pro_name in list_libs:
		list_libs.remove(pro_name)
	write_var(mf, "LIBS", tr_str(list_libs))
write_var(mf, "SOURCES", list_src)
write_var(mf, "OBJ", "$(SOURCES:.c=.o)")
write_rule(mf, "all", "$(NAME)")
if len(list_h) > 0:
	write_rule(mf, "%.o", "%.c $(HEADERS)", ["$(CC) $(CFLAGS) $(HEADERFLAGS) -c -o $@ $<"])
else:
	write_rule(mf, "%.o", "%.c $(HEADERS)", ["$(CC) $(CFLAGS) -c -o $@ $<"])
if pro_type == "lib":
	write_rule(mf, "$(NAME)", "$(OBJ)", ["ar rcs $(NAME) $(OBJ)"])
elif pro_type == "prog":
	if len(list_h) > 0:
		write_rule(mf, "$(NAME)", "$(OBJ)", ["$(CC) $(CFLAGS) -o $(NAME) $(OBJ) $(LIBS)"])
	else:
		write_rule(mf, "$(NAME)", "$(OBJ)", ["$(CC) $(CFLAGS) $(HEADERFLAGS) -o $(NAME) $(OBJ) $(LIBS)"])
write_rule(mf, "clean", "", ["rm -f $(OBJ)"])
write_rule(mf, "fclean", "clean" , ["rm -f $(NAME)"])
write_rule(mf, "re", "fclean all")
