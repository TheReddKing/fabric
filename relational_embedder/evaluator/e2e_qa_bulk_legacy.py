import os,glob
sys.
dir_path = "/data/kevin21/testing/mitb_spaces"
f = open("accuracy.sh","w")

if len(sys.argv) < 2:
    print("NEED MORE ARGS")
    sys.exit(2)

parser = argparse.ArgumentParser()
parser.add_argument('dirpath', metavar='foldername',
                help='folder')
parser.add_argument('--spaces', default='True', help='should I have spaces? Default Yes')


args = parser.parse_args()
dir_path = args.dirpath
spaces = args.spaces
app = ""
if spaces:
    app = " space"

files = glob.glob(dir_path + "/vectors/*.txt")

for file in files:
    f.write("python e2e_qa_evaluator_legacy.py " + dir_path + " " + file + app + "\n")
