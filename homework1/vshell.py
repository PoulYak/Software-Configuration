#!/usr/bin/env python3

import os

def ls():
    try:
        print("\n".join(os.listdir()))
    except:
        pass

def pwd():
    try:
        print(os.getcwd())
    except:
        pass

def cd(args):
    if args:
        try:
            os.chdir(args[0])
        except:
            print("Error: No directory", args[0])

def cat(args):
    if args:
        try:
           filename = args[0]
           with open(filename) as fin:
               print(fin.read())
        except:
            print("Error: No file", args[0])


def get_dir():
    try:
        return os.getcwd().split("/")[-1]+"~"	
    except:
        return ""

isActive = True
while isActive:
    line = input(get_dir()+"$ ")
    line = line.split()
    if line:
        command, *args = line
        if command == "ls":
            ls()
        elif command == "pwd":
            pwd()
        elif command == "cd":
            cd(args)
        elif command == "cat":
            cat(args)

