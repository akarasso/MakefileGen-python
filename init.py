#!/usr/bin/python

import os

def create_folders():
    if not os.path.exists("./srcs"):
        os.makedirs("./srcs")
    if not os.path.exists("./includes"):
        os.makedirs("./includes")

def import_libft():
    imp = ""
    while not (imp == "y" or imp == "n"):
        imp = raw_input("Import libft (Y/n)? :")
        imp = imp or "y"
    if imp == "y":
        os.system("git clone https://github.com/minipopov/libft.git libft")

if __name__ == "__main__":
    create_folders()
    import_libft()
