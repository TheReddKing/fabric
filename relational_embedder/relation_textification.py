import argparse
import pandas as pd
from data_prep import data_prep_utils as dpu
import os
from os import listdir
from os.path import isfile, join


def _read_rows_from_dataframe(df, columns,format="TXT"):
    for index, el in df.iterrows():
        row = []
        for c in columns:
            cell_value = el[c]
            # clean cell_value
            cell_value = dpu.encode_cell(cell_value)
            if cell_value == 'nan':  # probably more efficient to avoid nan upstream
                row.append("")
            else:
                row.append(cell_value)
                if format == "TXT":
                    yield cell_value
        if format == "CSV":
            yield row

def _read_columns_from_dataframe(df, columns,format="TXT"):
    for c in columns:
        data_values = df[c]
        for el in data_values:
            el = dpu.encode_cell(el)
            if cell_value == 'nan':  # probably more efficient to avoid nan upstream
                continue
            yield el

# METHOD = "ROW","COL","ROWCOL" and "TXT" or "CSV" for FORMAT
def serialize(paths, output_file, method="ROWCOL", format="TXT", debug=False):
    try:
        os.remove(output_file)
    except FileNotFoundError:
        print("Creating new file for writing data")

    total = len(paths)
    current = 0
    if format == "TXT":
        f = open(output_file, 'a')
    elif format = "CSV":
        f = csv.writer(open(output_file, 'a'), delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    for path in paths:
        if debug:
            print(str(current) + "/" + str(total))
            current += 1
        df = pd.read_csv(path, encoding='latin1')
        columns = df.columns
        if format == "TXT":
            # Rows
            if "ROW" in method:
                for cell_value in _read_rows_from_dataframe(df, columns):
                    f.write(" " + cell_value)
            # Columns
            if "COL" in method:
                for cell_value in _read_columns_from_dataframe(df, columns):
                            f.write(" " + cell_value)
        elif format == "CSV":
            for row in _read_rows_from_dataframe(df,columns,format="CSV"):
                f.writerow(row)
            f.writerow(["~R!RR*~"])

def all_files_in_path(path):
    fs = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return fs

if __name__ == "__main__":
    print("Textify relation")

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', help='path to we model')
    parser.add_argument('--method', default='row_and_col', help='path to relational_embedding model')
    parser.add_argument('--output', default='textified.txt', help='path to relational_embedding model')
    parser.add_argument('--debug', default=False, help='whether to run progrm in debug mode or not')

    args = parser.parse_args()

    path = args.dataset
    method = args.method
    output = args.output
    debug = args.debug

    fs = all_files_in_path(path)
    if method == "row":
        serialize(fs, output,method="ROW",debug=debug)
    elif method == "col":
        serialize(fs, output,method="COL", debug=debug)
    elif method == "row_and_col":
        serialize(fs, output,method="ROWCOL", debug=debug)

    print("Done!")
