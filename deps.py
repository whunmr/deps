import sys
import os
from os import path
import re

#TODO: 1. ignore comments
#TODO: 2. ignore .obj,pdb,res,manifest... files

PROJECT_FILE = "C:/Projects/test/test/test.vcproj"
SRC_DIR = "C:/Projects/test/test/"
ROOT_FILE = "C:/Projects/test/test/src/test.cpp"

def cpp_files_under(src_dir):
    file_list = []
    cpp_file_pattern = re.compile(".*\.(h|hpp|cpp|cxx|tcc)$", re.IGNORECASE)    
    for root, sub_folders, files in os.walk(SRC_DIR):
        for file in files:
            file_list.append(os.path.join(root,file))
    file_list = [path.abspath(f) for f in file_list if cpp_file_pattern.match(f)]
    return set(file_list)

PRODUCT_FILES = cpp_files_under(SRC_DIR)
print PRODUCT_FILES

def deps_of(f):    
    ret = []
    dir = path.dirname(f)
    file_obj = file(f)
    lines = file_obj.readlines()
    file_obj.close()
    for line in lines:
        p = re.compile(r'#include *("|<)(.+?)("|>).*')        
        m = p.search(line)
        if m != None:
            include_file = path.abspath(path.join(dir, m.group(2)))
            if include_file in PRODUCT_FILES:
                ret.append(include_file)
                ret.extend(deps_of(include_file))
            else:
                print "==" + include_file
    return ret

def find_deps(files):
    ret = []
    for f in files:
        ret.extend(deps_of(path.abspath(f)))        
    return ret

if __name__ == "__main__":
    print find_deps([ROOT_FILE])
