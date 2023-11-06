import json
import time
import os
import cv2
from imutils import resize
import numpy as np
import tensorflow as tf
import math
from utils_func import iou_width_height as iou

'''
dir_img='/Users/mariolamas/Downloads/train2017'
json_labels='/Users/mariolamas/Downloads/annotations/instances_train2017.json'
with open(json_labels,'r') as labels_info:
    data=json.load(labels_info)
    annotations=data['annotations']
    images=data['images']
labels_info.close()
def prep_bbox(lista,elem,im_info):
    ancho_im=im_info['width']
    alto_im=im_info['height']
    lista[0]=str(lista[0]/ancho_im)
    lista[1]=str(lista[1]/alto_im)
    lista[2]=str(lista[2]/ancho_im)
    lista[3]=str(lista[3]/alto_im)
    lista.insert(0,str(elem['category_id']))
    return ' '.join(lista)+'\n'
'''
ruta_images='/Users/mariolamas/Desktop/sOFTWARE/SCRIPTS-TFG/Dataset/prueba_data/images'
ruta_labels='/Users/mariolamas/Desktop/sOFTWARE/SCRIPTS-TFG/Dataset/prueba_data/labels'

class YOLO_Dataset(tf.keras.utils.Sequence):
    def __init__(self,ruta_imagenes,ruta_labels,tam, batch,grid_sizes,anchors,anchor_mask):
        self.ruta_im=ruta_imagenes
        self.ruta_labels=ruta_labels
        self.tam=tam
        self.batch=batch
        self.anchors=anchors
        self.anchor_mask=anchor_mask
        self.data=[]
        self.grid=grid_sizes


        self.comprobar_tam(self.ruta_im)
        self.leer_bbox(ruta_labels)
    
    def __len__(self):
        return len(os.listdir(self.ruta_labels))
        

    
    def comprobar_tam(self,ruta_ims):
        for im in os.listdir(ruta_ims):
            img=cv2.imread(f'{ruta_ims}/{im}')
            if (np.shape(img)[0]!=self.tam) or (np.shape(img)[0]!=self.tam):
                img=resize(img,width=self.tam,height=self.tam)
                cv2.imwrite(f'{ruta_ims}/{im}',img)

        print('\n ¡TODAS LAS IMAGENES TIENEN EL TAMAÑO ADECUADO!\n')
    
    def leer_bbox(self,ruta_label):
        for txt in os.listdir(ruta_label):
            elem=[]
            file_name=txt.split('.')[0]
            bbox=np.roll(np.loadtxt(fname=f'{ruta_label}/{txt}',delimiter=' '), 4,axis=1).tolist()
            elem=[f'{self.ruta_im}/{file_name}.jpg',bbox]
            self.data.append(elem)
    
            

    def append_index_using_best_iou(self,x, anchors):
        x1_true, y1_true, x2_true, y2_true = x
        w_true = x2_true - x1_true
        h_true = y2_true - y1_true
        index = -1
        max_iou = -1
        for ind, anchor in enumerate(anchors):
            h_anch, w_anch = anchor
            intersection = min(w_true, w_anch) * min(w_true, w_anch)
            union = (w_true * h_true) + (w_anch * h_anch) - intersection
            iou = intersection / union
            if iou > max_iou:
                max_iou = iou
                index = ind
        return index

    

    def __getitem__(self, index):
        outs=[np.zeros(shape=(self.batch,3,G,G,6)) for G in self.grid]
        X=np.zeros(shape=(self.batch,self.tam,self.tam,3),dtype='float32') # 3 son los canales RGB
        print(len(outs))
        for i in range(self.batch):
            info_item=self.data[(index*self.batch)+i]
            im=cv2.imread(info_item[0])
            im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
            im =np.array(im,dtype='float32')
            im=im/255.0
            X[i,:,:,:]=im
            items=[]
            for box in info_item[1]:
                #print(box[2:4]) # (w,h)
                xo, yo, w, h, clas =box
                x1=xo+w
                y1=yo+h
                x=xo + w/2
                y=yo + h/2

                indice=self.append_index_using_best_iou([xo,yo,x1,y1],self.anchors)

                if indice in self.anchor_mask[0]:
                    celda_x=int(self.grid[0]*x)
                    celda_y=int(self.grid[0]*y)

                    x_cel= self.grid[0]*x - celda_x
                    y_cel= self.grid[0]*y - celda_y
                    w_cel =w*self.grid[0]
                    h_cel=h*self.grid[0]
                    outs[0][i,indice %len(self.anchor_mask[0]),celda_y,celda_x,:]=[1.0,x_cel,y_cel,w_cel,h_cel,int(clas)]
                
                elif indice in self.anchor_mask[1]:
                    celda_x=int(self.grid[1]*x)
                    celda_y=int(self.grid[1]*y)

                    x_cel= self.grid[1]*x - celda_x
                    y_cel= self.grid[1]*y - celda_y
                    w_cel =w*self.grid[1]
                    h_cel=h*self.grid[1]
                    outs[1][i,indice %len(self.anchor_mask[1]),celda_y,celda_x,:]=[1.0,x_cel,y_cel,w_cel,h_cel,int(clas)]
                
                elif indice in self.anchor_mask[2]:
                    celda_x=int(self.grid[2]*x)
                    celda_y=int(self.grid[2]*y)
                    x_cel= self.grid[2]*x - celda_x
                    y_cel= self.grid[2]*y - celda_y
                    w_cel =w*self.grid[2]
                    h_cel=h*self.grid[2]
                    outs[2][i,indice %len(self.anchor_mask[2]),celda_y,celda_x,:]=[1.0,x_cel,y_cel,w_cel,h_cel,int(clas)]

            

            
        return tf.convert_to_tensor(X,dtype='float32'),[tf.convert_to_tensor(outs[0],dtype='float32'),tf.convert_to_tensor(outs[1],dtype='float32'),tf.convert_to_tensor(outs[2],dtype='float32')]

def test():
    anchors= [
    [0.28, 0.22], [0.38, 0.48], [0.9, 0.78],
    [0.07, 0.15], [0.15, 0.11], [0.14, 0.29],
    [0.02, 0.03], [0.04, 0.07], [0.08, 0.06],
    ]
    anchors_mask=[[0, 1, 2], [3, 4, 5], [6, 7, 8]]   

    ruta_images='/Users/mariolamas/Desktop/sOFTWARE/SCRIPTS-TFG/Dataset/prueba_data/images'
    ruta_labels='/Users/mariolamas/Desktop/sOFTWARE/SCRIPTS-TFG/Dataset/prueba_data/labels'

    dataset=YOLO_Dataset(ruta_images,ruta_labels,416,1,[13,26,52],anchors,anchors_mask)

    print(dataset[0])


if __name__=='__main__':
    test()



    
