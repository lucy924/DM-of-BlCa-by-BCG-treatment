#!/usr/bin/env python
# -*- mode: python; python-indent: 4; tab-width: 4; indent-tabs-mode: nil -*-
################################################################################
# LUCY PICARD
# ----------------------------------
# https://pythonexamples.org/python-csv-to-json/
# Script for only adding things to git if they are small enough.
# Note that paths are hard-coded in.
# Run in virtual environment, eg. `mamba activate sns_py3.11.8_venv`
################################################################################

from __future__ import print_function
import argparse
import subprocess

import glob
import os
import sys
import pandas as pd
import numpy as np


def main(args):
    filepaths = args.filepaths
    truefalse = args.truefalse
    
    git_status = subprocess.run(['git', 'status'], capture_output=True)
    # print(git_status.stdout)
    
    start_now = False
    start_now_text = '  (use "git add <file>..." to include in what will be committed)'
    start_now2_text = '  (use "git restore --staged <file>..." to unstage)'
    stop_now_text = ''
    list_of_dirs_to_check = []
    list_of_files_to_check = []
    for line in git_status.stdout.splitlines():
        if start_now:
            line = line.decode()
            if line == stop_now_text:
                break
            if line.endswith('/'):
                list_of_dirs_to_check.append(line.strip('\t'))
            else:
                add_line = line.strip('\t')
                add_line = add_line.lstrip("new file:   ")
                list_of_files_to_check.append(add_line)
        else:
            if line.decode() == start_now_text:
                start_now = True
            elif line.decode() == start_now2_text:
                start_now = True
                
    for add_dir in list_of_dirs_to_check:
        os.path.join(os.getcwd(), add_dir)
        recursive_glob = glob.glob(os.path.join(os.getcwd(), add_dir, '**'), recursive=True)
        for i, fn in enumerate(recursive_glob):
            if i == 0:  # checks for the entry that is just the directory
                continue
            size = os.path.getsize(fn)
            if size < 100e6:
                # git add
                subprocess.run(['git', 'add', '--no-all', fn])
            else:
                # gitignore
                with open('.gitignore', 'a') as fgit:
                    fgit.write(fn.strip('/home/dejlu879/20240731-BEBIC_dmr/') + '\n')
                
    for fn in list_of_files_to_check:
        fn = fn.strip('modified:   ')
        # print(fn)
        size = os.path.getsize(os.path.join(os.getcwd(), fn))
        if size < 100e6:
            # git add
            subprocess.run(['git', 'add', '--no-all', fn])
        else:
            # gitignore
            with open('.gitignore', 'a') as fgit:
                fgit.write(fn + '\n')
                
    # sys.exit()


if __name__ == '__main__':
    desc = 'Description'
    parser = argparse.ArgumentParser(description=desc)
    #parser.add_argument('--dir', type=str, help='Dir Prefix')
    parser.add_argument('-fp', '--filepaths', type=str,
                        help='path to dir')
    parser.add_argument('-t', '--truefalse', action='store_true',
                        help='flag true if used, otherwise false')
    args = parser.parse_args()

    main(args)
