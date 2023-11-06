import tensorflow as tf
from layers import CONV,C2f,SPPF,DETECT,upsamp
import torch 


#DEFINICION DE LOS DISTINTOS MODELOS

class YOLO(tf.keras.Model):
    def __init__(self, num_classes, grid_sizes, iou_threshold, score_threshold, max_bboxes):

        super(YOLO, self).__init__()
        self.num_classes = num_classes
        self.grid_sizes = grid_sizes
        self.iou_threshold = iou_threshold
        self.score_threshold = score_threshold
        self.max_bboxes = max_bboxes

        #Capas para el modelo
        #Bloque1 (Empezando desde arriba)
        self.conv1_b1=CONV((3,3),(2,2),32)  #(208,208,32)
        self.conv2_b1=CONV((3,3),(2,2),64)  #(104,104,64)
        self.c1_b1=C2f(64,(3,3),(1,1),True,2)   #(104,104,64)
        self.conv3_b1=CONV((3,3),(2,2),128) #(52,52,128)
        self.c2_b1=C2f(128,(3,3),(1,1),True,4)  #(52,52,128)
        self.conv4_b1=CONV((3,3),(2,2),256) #(26,25,256)
        self.c3_b1=C2f(256,(3,3),(1,1),True,4)  #(26,26,256)
        self.conv5_b1=CONV((3,3),(2,2),256) #(13,13,256)
        self.c4_b1=C2f(256,(3,3),(1,1),True,2)  #(13,13,256)
        self.sppf=SPPF(256,(3,3),(1,1),(2,2),(1,1)) #(13,13,256)

        #Bloque2 (Empezando desde arriba)
        self.c1_b2=C2f(256,(3,3),(1,1),False,2) #(52,52,256)
        self.c2_b2=C2f(512,(3,3),(1,1),False,2) #(26,26,512)

        #Bloque3 (Empezando desde arriba)
        self.conv1_b3=CONV((3,3),(2,2),256) #(26,26,256)
        self.c1_b3=C2f(512,(3,3),(1,1),False,2) #(26,26,512)
        self.conv2_b3=CONV((3,3),(2,2),512)    #(13,13,512)
        self.c2_b3=C2f(512,(3,3),(1,1),False,2) #(13,13,512)

        #CAPAS DE DETECT
        self.det_1=DETECT(256,(3,3),(1,1),self.num_classes,52)  #(52,52,5,5+num_clases)
        self.det_2=DETECT(512,(3,3),(1,1),self.num_classes,26)  #(26,26,5,5+num_clases)
        self.det_3=DETECT(512,(3,3),(1,1),self.num_classes,13)  #(13,13,5,5+num_clases)

        #Salida
        self.up=upsamp()
        self.concat=tf.keras.layers.Concatenate(axis=-1)

        '''
        #Layers de salida
        self.out80=Output(256,self.num_classes,self.grid_sizes[2],self.anchors[self.anchor_masks[2]])
        self.out40=Output(256,self.num_classes,self.grid_sizes[1],self.anchors[self.anchor_masks[1]])
        self.out20=Output(256,self.num_classes,self.grid_sizes[0],self.anchors[self.anchor_masks[0]])

        #Postprocesamiento
        self.post1 = PostProcessor(self.num_classes, self.grid_sizes[0], self.anchors, self.anchor_masks[0])
        self.post2 = PostProcessor(self.num_classes, self.grid_sizes[1], self.anchors, self.anchor_masks[1])
        self.post3 = PostProcessor(self.num_classes, self.grid_sizes[2], self.anchors, self.anchor_masks[2])

        #Capa nms para preparar preds
        self.nms = NMS(self.num_classes, self.iou_threshold, self.score_threshold, self.max_bboxes)
        '''

    
    def call(self, inputs, training=False):
        x=self.conv1_b1(inputs)
        
        x=self.conv2_b1(x)
        
        x=self.c1_b1(x)
        
        x=self.conv3_b1(x)
        
        x1=self.c2_b1(x)
        
        x=self.conv4_b1(x1)
        
        x2=self.c3_b1(x)
        
        x=self.conv5_b1(x2)
        
        x=self.c4_b1(x)
        
    
        x3=self.sppf(x)
        

        x=self.up(x3)
        
        x=self.concat([x,x2])
        
        x2_2=self.c2_b2(x)
        
        x=self.up(x2_2)
        
        x=self.concat([x,x1])
        
        x1_2=self.c1_b2(x)  #SALIDA PARA DETECCION (52,52,256)
        

        x=self.conv1_b3(x1_2)
        
        x=self.concat([x,x2_2])
        
        x2_3=self.c1_b3(x)  #SALIDA PARA DETECCION (26,26,512)
        
        x=self.conv2_b3(x2_3)
        
        x=self.concat([x,x3])
        
        x3_3=self.c2_b3(x)  #SALIDA PARA DETECCION (13,13,512)
        


        x1_out=self.det_1(x1_2) #(52,52,5,5+num_clases)
        
        x2_out=self.det_2(x2_3) #(26,26,5,5+num_clases)
        x3_out=self.det_3(x3_3) #(13,13,5,5+num_clases)

        '''
        x80_out=self.out80(x80)
        x40_out=self.out40(x40)
        x20_out=self.out20(x20)
        '''

        if training:
            return [x3_out,x2_out,x1_out]
        
        return [x3_out,x2_out,x1_out]

        '''
        bbox20, p20, c20, _ = self.post1(x20_out, False)
        bbox40, p40, c40, _ = self.post2(x40_out, False)
        bbox80, p80, c80, _ = self.post3(x80_out, False)
        pred, valid = self.nms([[bbox20, p20, c20], [bbox40, p40, c40], [bbox80, p80, c80]], False) 

        return pred, valid
        '''
    def summary(self, img_h, img_w, img_c, batch_size):
        X_inp = tf.keras.Input(shape=(img_h, img_w, img_c), batch_size=batch_size)
        x = self.call(X_inp)
        m = tf.keras.Model(inputs=X_inp, outputs=x)
        return m.summary()

if __name__=='__main__':
    num_clases=80
    grid_sizes=[13,26,52]
    iou,score=0.5,0.5
    max_box=10

    modelo=YOLO(num_clases,grid_sizes,iou,score,max_box)

    x=tf.random.normal(shape=(2,416,416,3))   

    salida=modelo(x,training=True)

    print(salida[0].shape)
    print(salida[1].shape)
    print(salida[2].shape)
