#!/usr/bin/python3

import os
import re
import sys
import os.path
import subprocess

import pprint
pp = pprint.PrettyPrinter(indent=4)

def unifdef(program_path, args, file_path):
    full_args = [program_path] + args + [file_path]
    #print(full_args)

    p = subprocess.Popen(full_args, shell=True, stdout=subprocess.PIPE)
    out,err = p.communicate()
    out = out.decode('utf-8')
    return out

class scanner2:
    def __init__(self, defines=()):
        self.defines = defines

        # attributions is a dict containing a tuple: filename, full path, code block, line no
        # key is the @attribution tag in C comment
        self.attributions = {}

    def do_scan(self, root_path):
        for root, dirs, files in os.walk(root_path):
            for file in files:

                if not self.__is_code(file): continue
                file_path = os.path.join(root, file)

                file_buf = ''
                with open(file_path, "r") as f:
                    file_buf = f.read()#.replace('\n','')

                self.__parse_ifdefs(file_buf, file, file_path)

                #print(file)

        return self.attributions


    def __is_code(self, filename):
        ext = os.path.splitext(filename)[1]
        return ext in ('.cpp', '.c', '.h', '.hh', '.cc', '.m', '.mm')


    def __parse_ifdefs(self, file_buf, filename, full_path):
        block_start_pattern = re.compile(r'\#if(?:n*def)*\s+?\(*([^\)]*)\)*')
        block_end_pattern   = re.compile(r'\#endif')
        attribution_pattern = re.compile(r'//(@.+)', re.M)
        inside = 0        # count of how many ifdefs inside
        inside_marked = 0 # depth that we entered a define we care about
        marked_lineno = 0 # line number marked buffer started at

        file_lines = file_buf.splitlines()
        code_buf = ""
        for i in range(0, len(file_lines)):
            if inside > 0:
                code_buf += file_lines[i] + "\n"

            match = block_start_pattern.search(file_lines[i])
            if match == None: 
                match = block_end_pattern.search(file_lines[i])
                if match == None: continue
                inside -= 1
                if inside < inside_marked:
                    # end of parse -- code_buf contains block
                    attribution = self.__parse_attribution(attribution_pattern, code_buf)
                    self.attributions.setdefault(attribution, []).append((filename, full_path, code_buf, marked_lineno))
                    code_buf = ""
                    inside_marked = 0

                if inside < 0:
                    print("error in parse: negative ifdef count reached")
                    print(filename)
                    print(file_lines[i])
                    print(i)
                    sys.exit(1)

                
                continue

            macro_name = match.group(1).rstrip()
            inside += 1

            if macro_name in self.defines:
                code_buf = ""
                code_buf += file_lines[i] + "\n"
                marked_lineno = i+1

                inside_marked = inside



    def __parse_attribution(self, attribution_pattern, code_buf):
        match = attribution_pattern.search(code_buf)
        if match == None:
            return "@unknown"
        else:
            return match.group(1).rstrip()
            
            
