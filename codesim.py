#!/usr/bin/env python3
"""
codesim: tool for calculating similarity between two c++ programs.
"""
import os
import sys
import argparse

def check_file(file_path):
    """
    check file path is invalid. (not satisfied c++ file path)
    """
    if os.path.isfile(file_path) and file_path.endswith(".cpp"):
        return False
    return True

def compile_file(file_path):
    """
    compile code
    """
    pass
    binary_file_path = ''
    return binary_file_path

def check_similarity(binary_code1, binary_code2):
    """
    calculate similarity between binary_code1 and binary_code2
    """
    similarity = 0
    pass
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

    # compile file
    source_binary_file_path = compile_file(source_file_path)
    target_binary_file_path = compile_file(target_file_path)

    # calculate similarity
    if args.verbose:
        # debug mode
        pass
    else:
        # normal mode
        pass
    similarity = check_similarity(source_binary_file_path, target_binary_file_path)
    print(similarity)
    