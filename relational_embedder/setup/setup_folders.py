from relational_embedder import relation_textification
import os
import sys
import errno
import glob
import shutil
from globals import *
import argparse

dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("NEED MORE ARGS")
        print("python setup_folders.py foldername databasename")
        # NEW python setup_f.py data_fold databasename outputparsedfol
        sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('foldername', metavar='foldername',
                    help='folder')
    parser.add_argument('databasename', metavar='dbname',
        help='db name')
    parser.add_argument('--spaces', default='True', help='should I split on spaces? Default Yes')
    parser.add_argument('--output', default="", help='output folder')


    args = parser.parse_args()

    outputparsedfolder = args.output
    spaces = args.spaces

    # print(spaces)
    Globals.set(GlobalC.RELATIONAL_EMBEDDER,"replaceSpace",spaces)

    filepath = args.foldername
    filename = args.databasename
    parseddirc = filepath
    if len(outputparsedfolder) == 0:
        # filepath
        try:
            if(not os.path.isdir(f"{filepath}/data/")):
                files = glob.glob(f"{filepath}/*.csv")
                os.makedirs(f"{filepath}/data/")
                for file in files:
                    shutil.move(file, f"{filepath}/data/")
            if(not os.path.isdir(f"{filepath}/dataparsed/")):
                os.makedirs(f"{filepath}/dataparsed/")
            os.makedirs(filepath+"/vectors/")
            # os.makedirs(filepath+"/vectors_combined/")
            os.makedirs(filepath+"/results/")
            # os.makedirs(filepath+"/vocabulary/") #TODO: Add vocabulary option so that the accuracy API works better.
        except OSError as e:
            pass
        fs = relation_textification.all_files_in_path(f"{filepath}/data/")
        parseddirc = f"{filepath}/dataparsed"
    else:
        fs = relation_textification.all_files_in_path(f"{filepath}/")

    relation_textification.serialize(fs,f"{parseddirc}/{filename}.csv",method="ROWCOL",format="CSV",debug=True)
    relation_textification.serialize(fs, f"{parseddirc}/{filename}.txt",method="ROWCOL",format="TXT",debug=True)
