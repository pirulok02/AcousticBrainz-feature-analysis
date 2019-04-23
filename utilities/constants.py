import os

ROOT_DIR = os.path.abspath("")
IMAGE_FOLDER = os.path.join(ROOT_DIR,"Output Plots")
DATA_FOLDER = os.path.join(ROOT_DIR, "Data Files")

if not os.path.isdir(IMAGE_FOLDER): os.makedirs(IMAGE_FOLDER)
if not os.path.isdir(DATA_FOLDER): os.makedirs(DATA_FOLDER)