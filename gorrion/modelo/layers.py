##############################################3
        #IMPORTACION DE PAQUETES
##############################################
import tensorflow as tf
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import random as rn

#### DEFINICION DE LOS TIPOS DE CAPAS ###
#-------------------------------------------- 

#CAPA DE CONVOLUCION
class CONV(tf.keras.layers.Layer):
  '''
  -------------------------------------------------------------------------------
  La capa de convolución se encarga de aprender las características más cruciales del modelo, realiza la operación de convolución sobre unos datos de entrada,
  esta es la capa que produce un mayor consumo de recursos:

  Este bloque de convolución esta compuesto por tres capas:

    1. Convolucion 2D
    2. Normalizacion
    3. Leaky Relu

  -------------------------------------------------------------------------------
  '''
  def __init__(self,kernel_size,strides,filters):
    '''
    -------------------------------------------------------------------------------
    En el método __init__ definimos los parámetros necesarios así como las capas necesarias para el adecuado
    funcionamiento del bloque.

    Los parámetros requeridos son los siguientes:

    Kernel_size --> Indica el tamaño de los filtros con los que se va a aplicar la convolución.

    Strides --> Hacen que el kernel se desplace un numeor concreto de pixeles a la derecha.

    Filters --> Indica el número de filtros que se van a aplicar

    -------------------------------------------------------------------------------
    '''
    super(CONV,self).__init__()
    self.kernel_size=kernel_size
    self.strides=strides
    self.filters=filters
    self.conv=tf.keras.layers.Conv2D(filters=self.filters,kernel_size=self.kernel_size,strides=self.strides,padding='same',use_bias=False,kernel_regularizer=tf.keras.regularizers.L2(l2=53-4))
    self.norm=tf.keras.layers.BatchNormalization()
    self.leaky=tf.keras.layers.LeakyReLU()
  
  def call(self,inputs,training):
    return self.leaky(self.norm(self.conv(inputs)))
  
  def get_config(self):
    '''
    -------------------------------------------------------------------------------
    El método get_config se encarga de actualizar los valores de los parámetros del bloque.

    -------------------------------------------------------------------------------
    '''
    config = super(CONV, self).get_config()
    config.update({'filters': self.filters, 'kernel_size': self.kernel_size})
    return config

#CAPA C2F
class C2f(tf.keras.layers.Layer):
    def __init__(self,filtros_out,kernel_size,strides,shorcut,number_bottles):
        super(C2f,self).__init__(trainable=True,dynamic=False,dtype='float32')
        self.filtros_out=filtros_out
        self.kernel_size=kernel_size
        self.strides=strides
        self.n=number_bottles
        self.shortcut=shorcut
        self.conv=CONV(self.kernel_size,self.strides,self.filtros_out)
        self.btllnck=Bottleneck(self.filtros_out/2,self.shortcut)
        self.conc=tf.keras.layers.Concatenate(axis=-1)
        self.conv_end=CONV(self.kernel_size,self.strides,self.filtros_out)
    
    def call(self,inputs):
        x=self.conv(inputs)
        x1,x=tf.split(x,2,axis=-1)
        conc=[x1,x]
        for i in range(self.n):
            x=self.btllnck(x)
            conc.append(x)
        x=self.conc(conc)
        return self.conv_end(x)



class SPPF(tf.keras.layers.Layer):

    def __init__(self,filtros,kernel_size,strides,pool_size,strides_pooling):
        super(SPPF,self).__init__(trainable=True,dynamic=False,dtype='float32')
        self.filtros=filtros
        self.pool_size=pool_size
        self.strides_pooling=strides_pooling
        self.strides=strides
        self.kernel_size=kernel_size
        self.conv=CONV(self.kernel_size,self.strides,self.filtros)
        self.max_pool=tf.keras.layers.MaxPooling2D(self.pool_size,self.strides_pooling,padding='same')
        self.concat=tf.keras.layers.Concatenate(axis=-1)
        self.conv_end=CONV(self.kernel_size,self.strides,self.filtros)
    
    def call(self,inputs):
        x=self.conv(inputs)
        x1=x
        x=self.max_pool(x)
        x2=x
        x=self.max_pool(x)
        x3=x
        x=self.max_pool(x)
        x=self.concat([x,x3,x2,x1])
        x=self.conv_end(x)
        return x



#CAPA BOTTLENECK
class Bottleneck(tf.keras.layers.Layer):
    '''
    -------------------------------------------------------------------------------
    La capa Bottleneck consiste en una concatenación de capas de Convolución, 
    este bloque tiene los siguientes tipos de capas:

        1. Bloques Conv
    
    ------------------------------------------------------------------------------
    '''
    def __init__(self,filtros,shorcut):
        '''
        -------------------------------------------------------------------------------
        En el método __init__ definimos los parámetros necesarios así como las capas necesarias para el adecuado
        funcionamiento del bloque.

        Los parámetros requeridos son los siguientes:

        Kernel_size --> Indica el tamaño de los filtros con los que se va a aplicar la convolución.

        Strides --> Hacen que el kernel se desplace un numeor concreto de pixeles a la derecha.

        Filters --> Indica el número de filtros que se van a aplicar

        Shortcut --> En caso de ser True guarda información de los inputs y se lo suma a la salida.

        -------------------------------------------------------------------------------
        '''
        super(Bottleneck,self).__init__(trainable=True,dynamic=False,dtype='float32')
        self.filtros=filtros
        self.shortcut=shorcut
        self.conv=CONV((3,3),(1,1),self.filtros)
    
    def call(self,inputs):
        if self.shortcut==True:
            x=self.conv(inputs)
            x=self.conv(x)
            
            return x + inputs
        else:
            return self.conv(self.conv(inputs))

#Capa de deteccion
class DETECT(tf.keras.layers.Layer):
    def __init__(self,filtros,kernel_size,strides,number_clases,grid_size):
        super(DETECT,self).__init__(trainable=True,dynamic=False,dtype='float32')
        self.filtros=filtros
        self.kernel_size=kernel_size
        self.strides=strides
        self.num=number_clases
        self.grid_size=grid_size

        #Superior
        self.conv=CONV((3,3),(1,1),(self.filtros))
        self.concat=tf.keras.layers.Concatenate(axis=-1)
        self.conv2D_1=tf.keras.layers.Conv2D(3*5,(3,3),1,'same')
        self.conv2D_2=tf.keras.layers.Conv2D(3*self.num,(3,3),1,'same')

        self.reshape_1=tf.keras.layers.Reshape(target_shape=(3,self.grid_size,self.grid_size,5))
        self.reshape_2=tf.keras.layers.Reshape(target_shape=(3,self.grid_size,self.grid_size,self.num))

    def call(self,inputs,training):
        x=self.conv(inputs)
        x=self.conv(x)
        x1=self.conv2D_1(x)
        x1=self.reshape_1(x1)   #(3,GRID,GRID,5(p,xo,yo,w,h))

        x=self.conv(inputs)
        x=self.conv(x)
        x2=self.conv2D_2(x)
        x2=self.reshape_2(x2)   #(3,GRID,GRID,NUM_CLASES)

        return self.concat([x1,x2])     #(3,GRID,GRID,(p,xo,yo,w,h,num_clases))






#Capa nms
class NMS(tf.keras.layers.Layer):
    '''
    -------------------------------------------------------------------------------
    La capa NMS (Non-Max Suppression) se encarga de combinar las predicciones de todos los grids mostrando las predicciones que cumplen con los umbrales
    de IOU (Intersection over Union) y de confianza, evitando asi que un mismo objeto no se detecte en varias ocasiones y que los objetos mostrados 
    cuenten con la confianza suficiente.
    Emplea los siguientes tipos de capas:

        1. Capas de Reshape
        2. Capas de Concatenación

    -------------------------------------------------------------------------------
    '''
    def __init__(self, num_classes, iou_threshold, score_threshold, max_bboxes):
        '''
        -------------------------------------------------------------------------------
        En el método __init__ definimos los parámetros necesarios así como las capas necesarias para el adecuado
        funcionamiento del bloque.

        Los parámetros requeridos son los siguientes:

        Num_clases --> Indica el número de clases con que esta entrenado o esta siendo entrenado el modelo.

        IOU_threshold --> Valor límite para la intersección sobre unión

        Score_threshold --> Valor mínimo para la confianza en la predicción

        Max_bboxes --> Numero máximo de predicciones por imagen.

        -------------------------------------------------------------------------------
        '''
        super(NMS, self).__init__(trainable=False, dynamic=False, dtype='float32')
        self.num_classes = num_classes
        self.iou_threshold = iou_threshold
        self.score_threshold = score_threshold
        self.max_bboxes = max_bboxes
        self.reshape_b13 = tf.keras.layers.Reshape(target_shape=(-1, 4))
        self.reshape_p13 = tf.keras.layers.Reshape(target_shape=(-1, 1))
        self.reshape_c13 = tf.keras.layers.Reshape(target_shape=(-1, self.num_classes))
        self.reshape_b26 = tf.keras.layers.Reshape(target_shape=(-1, 4))
        self.reshape_p26 = tf.keras.layers.Reshape(target_shape=(-1, 1))
        self.reshape_c26 = tf.keras.layers.Reshape(target_shape=(-1, self.num_classes))
        self.reshape_b52 = tf.keras.layers.Reshape(target_shape=(-1, 4))
        self.reshape_p52 = tf.keras.layers.Reshape(target_shape=(-1, 1))
        self.reshape_c52 = tf.keras.layers.Reshape(target_shape=(-1, self.num_classes))
        self.bbox_concat = tf.keras.layers.Concatenate(axis=1)
        self.p_concat = tf.keras.layers.Concatenate(axis=1)
        self.c_concat = tf.keras.layers.Concatenate(axis=1)
        self.reshape = tf.keras.layers.Reshape(target_shape=(-1, 1, 4))

    def call(self, inputs, training): # [[(B, 13, 13, 3, 4), (B, 13, 13, 3, 1), (B, 13, 13, 3, N)], [(B, 26, 26, 3, 4), (B, 26, 26, 3, 1), (B, 26, 26, 3, N)], [(B, 52, 52, 3, 4), (B, 52, 52, 3, 1), (B, 52, 52, 3, N)]]
        [bbox13, p13, c13], [bbox26, p26, c26], [bbox52, p52, c52] = inputs # [(B, 13, 13, 3, 4), (B, 13, 13, 3, 1), (B, 13, 13, 3, N)], [(B, 26, 26, 3, 4), (B, 26, 26, 3, 1), (B, 26, 26, 3, N)], [(B, 52, 52, 3, 4), (B, 52, 52, 3, 1), (B, 52, 52, 3, N)]
        bbox13 = self.reshape_b13(bbox13) # (B, 13 * 13 * 3, 4)
        p13 = self.reshape_p13(p13) # (B, 13 * 13 * 3, 1)
        c13 = self.reshape_c13(c13) # (B, 13 * 13 * 3, N)
        bbox26 = self.reshape_b26(bbox26) # (B, 26 * 26 * 3, 4)
        p26 = self.reshape_p26(p26) # (B, 26 * 26 * 3, 1)
        c26 = self.reshape_c26(c26) # (B, 26 * 26 * 3, N)
        bbox52 = self.reshape_b52(bbox52) # (B, 52 * 52 * 3, 4)
        p52 = self.reshape_p52(p52) # (B, 52 * 52 * 3, 1)
        c52 = self.reshape_c52(c52) # (B, 52 * 52 * 3, N)
        bbox = self.bbox_concat([bbox13, bbox26, bbox52]) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3), 4)
        p = self.p_concat([p13, p26, p52]) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3), 1)
        c = self.c_concat([c13, c26, c52]) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3), N)
        c = tf.argmax(c, axis=-1) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3))
        c = tf.cast(c, dtype=tf.float32) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3))
        c = tf.expand_dims(c, axis=-1) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3), 1)
        score = p * c # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3), 1)
        bbox = self.reshape(bbox) # (B, (13 * 13 * 3) + (26 * 26 * 3) + (52 * 52 * 3), 1, 4)
        bbox, score, c, valid = tf.image.combined_non_max_suppression(boxes=bbox, scores=score, max_output_size_per_class=self.max_bboxes, max_total_size=self.max_bboxes, iou_threshold=self.iou_threshold, score_threshold=self.score_threshold) # (B, M, 4), (B, M), (B, M), (B,)
        score = tf.expand_dims(score, axis=-1) # (B, M, 1)
        c = tf.expand_dims(c, axis=-1) # (B, M, 1)
        pred = tf.concat([bbox, score, c], axis=-1) # (B, M, 4 + 1 + 1)
        return pred, valid # (B, M, 4 + 1 + 1), (B,)

    def get_config(self):
        '''
        -------------------------------------------------------------------------------
        El método get_config se encarga de actualizar los valores de los parámetros del bloque.

        -------------------------------------------------------------------------------
        '''
        config = super(NMS, self).get_config()
        config.update({'num_classes': self.num_classes, 'iou_threshold': self.iou_threshold, 'score_threshold': self.score_threshold, 'max_bboxes': self.max_bboxes})
        return config


#DEFINICION DEL BLOQUE UPSAMPPLE
class upsamp(tf.keras.layers.Layer):
  def __init__(self):
    super(upsamp,self).__init__()
    self.up=tf.keras.layers.UpSampling2D(size=(2,2))
  
  def call(self,inputs):
    x=self.up(inputs)
    
    return x
