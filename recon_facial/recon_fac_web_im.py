### CON ESTE PROGRAMA, PODREMOS A PARTIR DE UN DIRECTORIO CON IMAGENES, APLICAR RECONOCIMIENTO FACIAL SOBRE LA WEBCAM O UNA IMAGEN ###
### IMPORTACION DE PAQUETES ###
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
import torch
import warnings
import typing
import logging
import os
import platform
import glob
import PIL
import facenet_pytorch
from typing import Union, Dict
from PIL import Image
from facenet_pytorch import MTCNN
from facenet_pytorch import InceptionResnetV1
from urllib.request import urlretrieve
from tqdm import tqdm
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine

warnings.filterwarnings('ignore')

###Detector MCNN###
# --------------------#
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

mtcnn = MTCNN(
    select_largest=True,
    min_face_size=20,
    thresholds=[0.6, 0.7, 0.7],
    post_process=False,
    image_size=160,
    device=device
)
### ENCODER ###
# ----------------#
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
encoder = InceptionResnetV1(
    pretrained='vggface2',
    classify=False,
    device=device
).eval()


### DICCIONARIO DE REFERENCIA ###
# -------------------------------#
def dic_referencias(ruta, encoder):
    personas = os.listdir(ruta)
    dic = {}
    for pers in personas:
        embedd = []
        fotos = os.listdir(ruta + f'/{pers}')
        for pic in fotos:
            im = cv2.imread(ruta + f'/{pers}/{pic}')
            cara_im = mtcnn.forward(im)
            if cara_im is None:
                # print('la imagen ', pic, 'no reconoce cara')
                ...
            else:
                cara_im = np.moveaxis(np.expand_dims(cara_im.permute(1, 2, 0).int().numpy(), 0), -1, 1).astype(
                    np.float32) / 255
                cara_im = torch.tensor(cara_im)
                embeddings_im = encoder.forward(cara_im).detach().cpu().numpy()
                embeddings_im = list(tuple(embeddings_im[0]))
                embedd.append(embeddings_im)
        embedd = np.mean(embedd, axis=0)
        dic[pers] = embedd

    return dic


### FUNCIONES A EMPLEAR ###
# -------------------------#
def calcular_embedding(imagen, encoder):
    cara = imagen.permute(1, 2, 0).int().numpy()
    cara = np.expand_dims(cara, 0)
    caras = np.moveaxis(cara, -1, 1)
    caras = caras.astype(np.float32) / 255
    caras = torch.tensor(caras)
    embeddings = encoder.forward(caras).detach().cpu().numpy()
    embeddings_1 = list(tuple(embeddings[0]))
    return embeddings_1


def dib_cuad_name(imagen, boxes, name):
    i = 0
    while i < len(boxes):
        cv2.rectangle(imagen, (int(round(boxes[i, 0])), int(round(boxes[i, 1]))),
                      (int(round(boxes[i, 2])), int(round(boxes[i, 3]))), (0, 0, 255), 2)
        diferencia = int(round(boxes[i, 2])) - int(round(boxes[i, 0]))
        ini_x = int(round(boxes[i, 0]))
        valor_x = int(ini_x + diferencia / 2)
        cv2.putText(imagen, name, (valor_x, int(round(boxes[i, 3]))), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1)
        i += 1


def webcam_detect(encoder, mtcnn, diccionar):
    imagen = cv2.VideoCapture(0)
    frame_exist = True
    while (frame_exist):
        frame_exist, frame = imagen.read()
        frame1 = frame.copy()
        if not frame_exist:
            imagen.release()
            cv2.destroyAllWindows()
            break
        boxes, probs, landmarks = mtcnn.detect(frame, landmarks=True)
        # Extraccion caras
        cara = mtcnn.forward(frame1)
        if cara is None:
            pass
        else:
            embeddings_1 = calcular_embedding(cara, encoder)
            for key, value in diccionar.items():
                similitud = 1 - cosine(value, embeddings_1)
                if similitud >= 0.5:
                    dib_cuad_name(frame, boxes, key)
                else:
                    pass

        cv2.imshow('webcam', frame)

        if (cv2.waitKey(1) == ord('q')):
            ...


def imag_detect(encoder, mtcnn, diccionar):
    ruta_imagen = str(input('Introduce la ruta absoluta de la imagen: '))
    imagen = cv2.imread(ruta_imagen)
    boxes, probs, landmarks = mtcnn.detect(imagen, landmarks=True)
    cara = mtcnn.forward(imagen)
    if cara is None:
        pass
    else:
        embeddings_1 = calcular_embedding(cara, encoder)
        # print('CALCULANDO SIMILITUDES\n ------------------------------\n')
        for key, value in diccionar.items():
            similitud = 1 - cosine(value, embeddings_1)
            if similitud >= 0.6:
                dib_cuad_name(imagen, boxes, key)
                # print(f'SE HA DETECTADO A {key}')
            else:
                pass
    while (cv2.waitKey(1) != ord('q')):
        cv2.imshow('deteccion', imagen)  # Al presionar q se cierra la imagen mostrada
        time.sleep(1)


def ruta_dir():
    ruta_dir_imagenes = ''
    while ruta_dir_imagenes == '':
        try:
            ruta_dir_imagenes = str(input('Introduce la ruta de las imagenes de referencia'))
            if os.path.exists(ruta_dir_imagenes) == True:
                lista = os.listdir(ruta_dir_imagenes)
                for elem in lista:
                    if elem == '.DS_Store':
                        os.remove(ruta_dir_imagenes + '/.DS_Store')
                    else:
                        pass
                try:
                    diccionar = dic_referencias(ruta_dir_imagenes, encoder)
                except AttributeError:
                    print('\n #----------------------------------#'
                          '\nel directorio introducido no es correcto o no tiene imagenes'
                          '\n #----------------------------------#\n')
                    ruta_dir_imagenes = ''
            else:
                ruta_dir_imagenes = ''
                print('\n #----------------------------------#'
                      '\nEl directorio introducido no existe'
                      '\n #----------------------------------#\n')
        except ValueError:
            print('El valor introducido no es una ruta')
    return ruta_dir_imagenes, diccionar
    
    
    ruta_dir_imagenes, diccionar = ruta_dir()
i = 1
while i == 1:
    print('## RECONOCEDOR FACIAL ###\n'
          '#------------------------------#\n'
          'Pulse:\n'
          '1--> Reconocimiento mediante webcam\n'
          '2--> Reconocimiento con imagen\n'
          '3--> Salir')
    try:
        valor = int(input('Introduce el valor deseado: '))
        if valor == 1:
            webcam_detect(encoder, mtcnn, diccionar)
        elif valor == 2:
            imag_detect(encoder, mtcnn, diccionar)
        elif valor == 3:
            i = 0
        else:
            print('\n#------------------------#\n'
                  'EL VALOR INTRODUCIDO NO ES VALIDO\n'
                  '#------------------------#\n')
    except ValueError:
        print('\n#------------------------#\n'
              'EL VALOR INTRODUCIDO NO ES NUMÉRICO'
              '\n#------------------------#\n')
