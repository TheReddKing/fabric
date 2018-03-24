from relational_embedder import relation_to_csv, relation_to_text
import os
import sys
import errno
import glob
import shutil

dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("NEED MORE ARGS")
        print("python setupFolders.py foldername databasename")
        sys.exit(0)

    filepath = sys.argv[1]
    filename = sys.argv[2]

    try:
        if(not os.path.isdir(f"{filepath}/data/")):
            files = glob.glob(f"{filepath}/*.csv")
            os.makedirs(f"{filepath}/data/")
            for file in files:
                shutil.move(file, f"{filepath}/data/")
        if(not os.path.isdir(f"{filepath}/dataparsed/")):
            os.makedirs(f"{filepath}/dataparsed/")
        os.makedirs(filepath+"/vectors/")
        os.makedirs(filepath+"/vectors_combined/")
        os.makedirs(filepath+"/results/")
    except OSError as e:
        pass
    fs = relation_to_csv.all_files_in_path(f"{filepath}/data/")
    relation_to_csv.serialize_row_and_column_csv(fs,f"{filepath}/dataparsed/{filename}.csv",debug=True)
    relation_to_text.serialize_row_and_column(fs, f"{filepath}/dataparsed/{filename}.txt", debug=True)
