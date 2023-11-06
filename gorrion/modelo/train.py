import tensorflow as tf
from preprocessing_coco import YOLO_Dataset
from utils  import YOLOLoss, YOLOCallback

from yolo import YOLO


#DATOS INCIALES PARA EL MODELO
NUM_CLASES=80
GRID_SIZES=[13,26,52]
anchors= [
    [0.28, 0.22], [0.38, 0.48], [0.9, 0.78],
    [0.07, 0.15], [0.15, 0.11], [0.14, 0.29],
    [0.02, 0.03], [0.04, 0.07], [0.08, 0.06],
    ]
anchors_mask=[[0, 1, 2], [3, 4, 5], [6, 7, 8]] 
IOU,THRESHOLD=0.5,0.5
MAX_BBOXES=10
BATCH_SIZE=8
TAM_MOD=416
CANALES=3
EPOCHS=20

#DATASET PARA EL ENTRENAMIENTO

ruta_images='/Users/mariolamas/Desktop/sOFTWARE/SCRIPTS-TFG/Dataset/prueba_data/images'
ruta_labels='/Users/mariolamas/Desktop/sOFTWARE/SCRIPTS-TFG/Dataset/prueba_data/labels'

dir_entre_imgs='/home/zelenza/Desktop/pruebasia/yl_drn/dataset/train/images'
dir_entre_labels='/home/zelenza/Desktop/pruebasia/yl_drn/dataset/train/labels'
dir_val='/home/zelenza/Desktop/pruebasia/yl_drn/dataset/valid'

data_train= YOLO_Dataset(ruta_images,ruta_labels,416,2,GRID_SIZES,anchors,anchors_mask)

model=YOLO(NUM_CLASES,GRID_SIZES,IOU,THRESHOLD,MAX_BBOXES)

model.summary(416,416,3,2)

loss1=YOLOLoss(NUM_CLASES,GRID_SIZES[0],THRESHOLD)
loss2=YOLOLoss(NUM_CLASES,GRID_SIZES[1],THRESHOLD)
loss3=YOLOLoss(NUM_CLASES,GRID_SIZES[2],THRESHOLD)
loss=[loss1,loss2,loss3]

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-4),
              loss=loss,
              metrics=['accuracy'])

callbacks=YOLOCallback(TAM_MOD,NUM_CLASES,GRID_SIZES,anchors, anchors_mask)

model.fit(data_train,epochs=EPOCHS,callbacks=callbacks)





