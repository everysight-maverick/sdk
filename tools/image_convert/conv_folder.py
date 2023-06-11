#!/usr/bin/env python3

#########################################
import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x or newer")
    exit(-1)

#########################################
import os
import argparse
#########################################

def main():
    parser = argparse.ArgumentParser('Batch folder convert')
    parser.add_argument('-f', '--folder', type=str, default=".", help='Folder to convert')
    parser.add_argument('-o', '--out', type=str, default="out", help='Output Folder')
    args = parser.parse_args()
    path = args.folder
    out = args.out
    os.makedirs(out, exist_ok=True)
    sep = "----------------------------"
    print(sep)
    print("Searching files in "+path)
    print(sep)

    count=0
    for root, dirs, files in os.walk(path):
        for i in files:
            if i.lower().endswith("png") or i.lower().endswith("jpg") or i.lower().endswith("jpeg"):
                count = count+1
                relRoot = os.path.join(out,root.lstrip(path).strip('/').strip('\\'))
                os.makedirs(relRoot, exist_ok=True)
                o = f'{os.path.splitext(i)[0]}.png'
                print(f'{os.path.join(root, i)} -> {os.path.join(relRoot,o)}')
                os.system(f'python3 {os.path.join(os.path.dirname(os.path.realpath(__file__)),"evsimgconvert.py")} -c {os.path.join(root, i)} -o {os.path.join(relRoot,o)}')


    print(sep)
    print("DONE ("+ str(count) + " files processed)")
    print(sep)

if __name__ == '__main__':
    main()
