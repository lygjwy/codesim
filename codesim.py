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

def get_hex_list_from_compile_file(file_path, verbose=False):
    """
    compile code and return hexadecimal list
    """
    temp_file_path = tempfile.mkstemp(suffix='.o', dir='./')[1]
    # print("Temp File Path: {}".format(temp_file_path))
    subprocess.call(['gcc', '-c', '-o', temp_file_path, file_path])
    p = subprocess.Popen(['objdump', '-d', temp_file_path], stdout=subprocess.PIPE)
    output = p.communicate()[0].decode("utf-8")
    # remove temp file
    subprocess.call(['rm', temp_file_path])
    # match assembly command related hex-code
    hex_pattern =  r':\t(([0-9a-f]{2}\s){1,7})'
    hex_list = []
    for match in re.findall(hex_pattern, output):
        hex_list.append(match[0].replace(' ', ''))
    if verbose:
        print("Compiled Code Assembly Commands Hex List: %r" % hex_list)
    return hex_list


def check_similarity(source_hex_list, target_hex_list, verbose=False):
    """
    calculate similarity between source_hex_list and target_hex_list
    """
    # Longest Common Substring
    dp = [ [0 for i in range(len(target_hex_list)+1)] for j in range(len(source_hex_list)+1)]
    
    for i in range(len(source_hex_list)):
        for j in range(len(target_hex_list)):
            if source_hex_list[i] == target_hex_list[j]:
                dp[i+1][j+1] = dp[i][j] + 1
    
    max_value_list = [max(line) for line in dp]
    lcs_len = max(max_value_list)
    # construct consistent-match statistic info
    common_substring_dic = {}
    for i in range(1, lcs_len+1):
        common_substring_dic[i] = 0
    
    # get common substrings statistic dic
    i = len(max_value_list) -1
    while i >= 0:
        max_value = max_value_list[i]
        if max_value > 0:
            common_substring_dic[max_value] += 1
            # jump over max_value - 1 lines
            i -= max_value - 1
        i -= 1
    
    if verbose:
        print("Len source hexs: {}".format(len(source_hex_list)))
        print("Len target hexs: {}".format(len(target_hex_list)))
        print("Consistent match statistic dictionary: %r" % common_substring_dic)
    # calculate similarity
    sum = 0.0
    for span, num in common_substring_dic.items():
        sum += span**2  * num
    return sum*2 / (len(source_hex_list)**2 + len(target_hex_list)**2)


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

    verbose = args.verbose

    # check files
    if check_file(source_file_path) or check_file(target_file_path):
        sys.stderr.write("ERROR: INVALID FILE PATH, CHECK PATH SPELLING AND FILE SUFFIX.\n")
        exit(-1)

    # compile file and get hex tuple
    source_hex_list = get_hex_list_from_compile_file(source_file_path, verbose)
    target_hex_list = get_hex_list_from_compile_file(target_file_path, verbose)
    
    similarity = check_similarity(source_hex_list, target_hex_list, verbose)
    print("{:.1f}".format(similarity*100))