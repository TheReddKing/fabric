from relational_embedder import relation_textification
import os
import sys
import errno
import glob
import shutil

dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("NEED MORE ARGS")
        print("python setup_folders.py foldername databasename")
        print("OR")
        print("python setup_folders.py foldername databasename outputparsedfolder")
        # NEW python setup_f.py data_fold databasename outputparsedfol
        sys.exit(0)

    filepath = sys.argv[1]
    filename = sys.argv[2]
    parseddirc = filepath
    if len(sys.argv) == 3:
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
