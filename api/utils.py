import ast
from PIL import Image
from io import BytesIO
import numpy as np
import face_recognition

def extract_face_vector(data):
    # Assuming data is a list of OrderedDict objects
    face_vector_list = [entry['face_vector'] for entry in data]
    # Extracting the first face vector (assuming there is only one in the list)
    face_vector = face_vector_list[0]
    return face_vector

def clean_face_vector(vector_str):
    return ast.literal_eval(vector_str.replace('\r\n', ''))