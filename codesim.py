#!/usr/bin/env python3
"""
codesim: tool for calculating similarity between two c++ programs.
"""
import os
import sys
import argparse
import tempfile
import subprocess
import re


def check_file(file_path):
    """
    check file path is invalid. (not satisfied c++ file path)
    """
    if os.path.isfile(file_path) and file_path.endswith(".cpp"):
        return False
    return True

def get_hex_list_from_compile_file(file_path):
    """
    compile code and return hexadecimal list
    """
    temp_file_path = tempfile.mkstemp(suffix='.o', dir='./')[1]
    # print("Temp File Path: {}".format(temp_file_path))
    subprocess.call(['gcc', '-c', '-o', temp_file_path, file_path])
    p = subprocess.Popen(['objdump', '-s', '-j', '.text', temp_file_path], stdout=subprocess.PIPE)
    output = p.communicate()[0].decode("utf-8")
    # remove temp file
    subprocess.call(['rm', temp_file_path])
    hex_pattern =  r'[0-9a-f]{8}'
    return re.findall(hex_pattern, output)

def check_similarity(source_hex_list, target_hex_list):
    """
    calculate similarity between source_hex_list and target_hex_list
    """
    # print(source_hex_list)
    # print(target_hex_list)
    match_hex_list = [hex for hex in source_hex_list if hex in target_hex_list]
    similarity = float(len(match_hex_list)) / min(len(source_hex_list), len(target_hex_list))
    return similarity


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="codesim")
    # add optional arguments
    parser.add_argument("-v", "--verbose", help="print debugging messages", action="store_true")
    # add positional arguments
    parser.add_argument("code1", help="source c++ code file path")
    parser.add_argument("code2", help="target c++ code file path")

    args = parser.parse_args()
    source_file_path = args.code1
    target_file_path = args.code2

    # check files path
    if check_file(source_file_path) or check_file(target_file_path):
        sys.stderr.write("ERROR: INVALID FILE PATH, CHECK PATH SPELLING AND FILE SUFFIX.\n")
        exit(-1)

    # compile file and get hex tuple
    source_hex_list = get_hex_list_from_compile_file(source_file_path)
    target_hex_list = get_hex_list_from_compile_file(target_file_path)
    
    similarity = check_similarity(source_hex_list, target_hex_list)
    print("{:.1f}".format(similarity*100))
    # calculate similarity
    # if args.verbose:
    #     # debug mode
    #     pass
    # else:
    #     # normal mode
    #     pass
    # print("End.")