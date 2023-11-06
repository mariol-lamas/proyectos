import tensorflow as tf
import torch
from utils_func import intersection_over_union
import torch.nn as nn





class YOLOLoss(tf.keras.losses.Loss):
    def __init__(self, num_clases,grid_size, threshold):
        super(YOLOLoss, self).__init__()
        self.num_clas=num_clases
        self.grid=grid_size
        self.threshold=threshold
        

    def call(self, Y_true, Y_pred):
        p_true, x_true, y_true, w_true, h_true, clas=tf.split(Y_true,[1,1,1,1,1,1],axis=-1)
        p_pred, x_pred, y_pred, w_pred, h_pred, clas_pred=tf.split(Y_pred,[1,1,1,1,1,self.num_clas],axis=-1)

        bbox_scale = 2.0 - (w_true[..., 0] * h_true[..., 0])

        

        #print("__________________________________")
        #print(self.lambda_box * box_loss)
        #print(self.lambda_obj * object_loss)
        #print(self.lambda_noobj * no_object_loss)
        #print(self.lambda_class * class_loss)
        #print("\n")

        return 1





class YOLOCallback(tf.keras.callbacks.Callback):
    def __init__(self, tam, num_clases,grid_sizes, anchors,anchor_mask, ):
        ...

    def on_epoch_begin(self, epoch, logs=None):
        print(f'\n Comenzando epoch {epoch}')

    def on_train_begin(self, logs=None):
        print('#'*20,'\n COMENZANDO EL ENTRENAMIENTO\n','#'*20)
    
    def on_test_end(self, logs=None):
        return 
        
    def on_epoch_end(self, epoch, logs=None):
        print(f'\n Finalizando el epoch {epoch}')
