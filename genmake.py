#!/usr/bin/python

import os
from retrieve import *
from init import *

def write_var(fd, key, value):
	fd.write("{}	= {}\n\n".format(key, value))

def write_rule(fd, key, dep="", value=[]):
	fd.write("{}	: {}\n".format(key, dep))
	for v in value:
		fd.write("\t{}\n".format(v))
	fd.write("\n")

def get_option(msg, opt1 = "", opt2 = "", default = ""):
    r = ""
    if opt1 == "" and opt2 == "":
        r = raw_input("{}:".format(msg, opt1.upper()))
        r = r or default
    else:
        while not(r == opt1 or r == opt2):
            r = raw_input("{}:({}/{})".format(msg, opt1.upper(), opt2))
            r = r or default
    return r

def write_prog_makefile():
    pro_name = get_option("Nom du projet", "", "", "noname")
    mf = open("Makefile", "w")
    list_src = tr_str(retrieve_filelist(".", ".c"))
    list_headers = tr_str(retrieve_filelist(".", ".h"))
    l = get_dirlist("./includes")
    l.append("./includes ")
    list_h = tr_str(l)
    write_var(mf, "CC", "gcc")
    write_var(mf, "CFLAGS", "-Wall -Werror -Wextra")
    write_var(mf, "NAME", pro_name)
    write_var(mf, "HEADERS", list_h + "./libft/includes")
    write_var(mf, "SOURCES", list_src)
    write_var(mf, "OBJ", "$(SOURCES:.c=.o)")
    write_var(mf, "HEADER_LIST", "$(addprefix -I,$(HEADERS))")
    write_rule(mf, "all", "$(NAME)")
    if os.path.exists("./libft"):
        write_rule(mf, "makelib", "", ["make -C libft/"])
        write_rule(mf, "cleanlib", "", ["make clean -C libft/"])
        write_rule(mf, "fcleanlib", "", ["make fclean -C libft/"])
        write_rule(mf, "%.o", "%.c $(HEADERS)", ["$(CC) $(CFLAGS) $(HEADER_LIST) -c -o $@ $<"])
        write_rule(mf, "$(NAME)", "$(OBJ)", [
            "make -C libft/",
            "$(CC) $(CFLAGS) $(HEADER_LIST) -o $(NAME) $(OBJ) ./libft/libft.a"])
        write_rule(mf, "clean", "cleanlib", ["rm -f $(OBJ)"])
        write_rule(mf, "re", "fcleanlib fclean all")
        write_rule(mf, "fclean", "cleanlib clean" , ["rm -f $(NAME)"])
    else:
        write_rule(mf, "%.o", "%.c $(HEADERS)", ["$(CC) $(CFLAGS) $(HEADER_LIST) -c -o $@ $<"])
        write_rule(mf, "$(NAME)", "$(OBJ)", ["$(CC) $(CFLAGS) $(HEADER_LIST) -o $(NAME) $(OBJ)"])
        write_rule(mf, "clean", "", ["rm -f $(OBJ)"])
        write_rule(mf, "re", "fclean all")
        write_rule(mf, "fclean", "clean" , ["rm -f $(NAME)"])

def write_lib_makefile():
    pro_name = get_option("Nom de la lib", "", "", "noname")
    mf = open("Makefile", "w")
    list_src = tr_str(retrieve_filelist(".", ".c"))
    write_var(mf, "CC", "gcc")
    write_var(mf, "CFLAGS", "-Wall -Werror -Wextra")
    write_var(mf, "NAME", pro_name)
    write_var(mf, "HEADERS", "./includes")
    write_var(mf, "SOURCES", list_src)
    write_var(mf, "OBJ", "$(SOURCES:.c=.o)")
    write_rule(mf, "all", "$(NAME)")
    write_rule(mf, "%.o", "%.c $(HEADERS)", ["$(CC) $(CFLAGS) -I$(HEADERS) -c -o $@ $<"])
    write_rule(mf, "$(NAME)", "$(OBJ)", ["ar rcs $(NAME) $(OBJ)"])
    write_rule(mf, "so", "$(OBJ)", ["$(CC) -fPIC $(CFLAGS) $(SOURCES) -shared -I$(HEADERS)"])
    write_rule(mf, "clean", "", ["rm -f $(OBJ)"])
    write_rule(mf, "fclean", "clean" , ["rm -f $(NAME)"])
    write_rule(mf, "re", "fclean all")

def request():
    t = get_option("Type de contenu", "prog", "lib", "prog")
    if t == "prog":
        write_prog_makefile()
    else:
        write_lib_makefile()

if __name__ == "__main__":
    request()
