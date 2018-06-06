import matconvnet_hr101_to_pickle
import os
import requests

DEFAULT_MODEL_NAME = "hr_res101_pickle3.p"
DEFAULT_PICKLE_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models',DEFAULT_MODEL_NAME)
MAT_MODEL_URL = """https://www.cs.cmu.edu/%7Epeiyunh/tiny/hr_res101.mat"""
DEFAULT_MAT_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"hr_res101.mat")

import builtins
from tqdm import tqdm

def download_mat_model(mat_model_path=DEFAULT_MAT_FILE_PATH,verbose=True):
    def print(*args,**kwargs):
        if verbose:
            builtins.print(*args,**kwargs)
    print("Downloading model...")
    with requests.get(MAT_MODEL_URL, stream=True) as request:
        chunk_size = 1024
        length = int(request.headers['content-length'])
        try:
            file_size = os.path.getsize(mat_model_path)
        except FileNotFoundError:
            file_size = 0
        if file_size == length:
            print("File already exists")
        else:
            with open(mat_model_path, 'wb') as fp:
                for chunk in tqdm(request.iter_content(chunk_size=chunk_size), disable=not verbose, total=length/chunk_size,unit_scale=True,unit='MB'):
                    fp.write(chunk)
    print("Done!")
    return mat_model_path

def download_and_save_model():
    mat_model_path = download_mat_model()
    matconvnet_hr101_to_pickle.convert_and_save_pickle_model(mat_model_path,DEFAULT_PICKLE_FILE_PATH)

if __name__ == '__main__':
    download_and_save_model()
