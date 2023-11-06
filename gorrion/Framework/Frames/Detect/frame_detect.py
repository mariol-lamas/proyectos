from ultralytics import YOLO
import supervision as sv
import time
import numpy as np
import pyautogui
import imutils
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import Framework.Frames.Dispositivos.dispositivo as db
from Framework.Frames.funciones_aux import comprobacion_video, comprobacion_img, info_env
import os
from Framework.funciones import comprobar_switches


def frame_det(self):
    #Valores por defecto
    self.video = None
    self.ret = False
    modelo = YOLO('res/yolov8n.pt')
    anota_cubos = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.4
    )
    


#------------------------------------------- DEFINICION DE LAS FUNCIONES DEL FRAME DEL DETECTOR --------------------------------------#
    
    #-----------
    #Funcion para la deteccion en video y webcam
    #-----------
    def deteccion(clase):
        inicio =time.time()
        if self.video == None:
            ...
        else:
            self.ret, frame = self.video.read()
            if self.ret == True and len(clase)>0 and self.checkbox_1.get()==1:

                #Realizamos la deteccion
                resultaados = modelo(frame, conf=0.3, classes=clase, verbose=False)[0]
                detecciones = sv.Detections.from_yolov8(resultaados)
                try:
                    array = [
                        array
                        for array, _,_, class_od, _ in detecciones if class_od == 0
                    ][0]
                    if self.caras == True and array is not None:
                        persona = frame[round(array[1]):round(array[3]), round(array[0]):round(array[2])]
                        cv2.imwrite(f'{self.ruta_prog}/Imagenes/{self.imagenes_dir}.jpg', persona)
                        self.imagenes_dir += 1
                except IndexError:
                    print('Error en el indice durante el proceso')

                nombres = [
                    f'{self.lista_labels[class_id]}'  # {confidence:0.2f}'
                    for _,_, confidence, class_id, _
                    in detecciones
                ]

                #Mostramos la informacion en el entry
                num_per=len(nombres)
                if self.max<num_per:
                    self.max=num_per
                self.pers_vis_entr.delete(0,2)
                self.pers_vis_entr.insert(0,str(num_per))
                self.pers_vis_entr_max.delete(0,2)
                self.pers_vis_entr_max.insert(0,str(self.max))

                #Mostramos la imagen en el frame de deteccion
                if self.switch_mostrar_caja.get()==1:
                    frame = anota_cubos.annotate(scene=frame, detections=detecciones, labels=nombres)
                
                frame = imutils.resize(frame, width=640, height=480)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                etiq_video.configure(image=img)
                etiq_video.image = img
                etiq_video.after(2, main)
                
            else:
                detener()
                print('\nPara iniciar la deteccion debes elegir las clases y pulsar seleccion preparada\n')
        fin = time.time()
        print('TIEMPO: ', fin-inicio)

    #----------------
    #Funcion para realizar deteccion en funcion del modo de deteccion
    #------------------
    def main():
        etiq_video.place(x=round(0.017*self.ancho_detec), y=round(0.064*self.alto_detec))

        if (self.modo=='Video' or self.modo=='Webcam') and self.checkbox_1.get()==1:
            clase = clases_para_detect()
            deteccion(clase)
        elif self.modo=='Imagen'and self.checkbox_1.get()==1:
            clase = clases_para_detect()
            frame=cv2.imread(self.ruta)

            #Realizamos la deteccion sobre la imagen
            result=modelo(frame,conf=0.5, classes=clase,verbose=False)[0]
            detecciones = sv.Detections.from_yolov8(result)
            nombres = [
                f'{self.lista_labels[class_id]}'  # {confidence:0.2f}'
                for _,_, confidence, class_id, _
                in detecciones
            ]

            #Mostramos la info en el entry
            num_per=len(nombres)
            self.pers_vis_entr.delete(0)
            self.pers_vis_entr.insert(0,str(num_per))
            self.pers_vis_entr_max.delete(0)
            self.pers_vis_entr_max.insert(0,str(num_per))

            #Preprocesamos la imagen y la mostramos en el frame de deteccion
            if self.switch_mostrar_caja.get()==1:
                    frame = anota_cubos.annotate(scene=frame, detections=detecciones, labels=nombres)
            frame = imutils.resize(frame, width=640, height=480)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img=img.resize((640,300),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image=img)

            #Aplicamos la imagen sobre la etiqueta
            etiq_video.image = img
            etiq_video.configure(image=img)
            etiq_video.image = img

        else:
            print('\nEl modo de deteccion no es el correcto o el boton seleccion preparada no esta clicado\n')
    
    # clases_para_detect se encarga de comprobar os switches que estan activos es decir las clases seleccionadas
    # para la deteccion
    def clases_para_detect():
        self.list=[]
        dic = {'persona': 0, 'bicicleta': 1, 'coche': 2, 'motocicleta': 3, 'avion': 4, 'autobus': 5, 'tren': 6, 'camion': 7, 'barco': 8, 'semaforo': 9, 'hidrante': 10, 'señal de stop': 11, 'parquimetro': 12, 'banco': 13, 'pajaro': 14, 'gato': 15, 'perro': 16, 'caballo': 17, 'oveja': 18, 'vaca': 19, 'elefante': 20, 'oso': 21, 'cebra': 22, 'jirafa': 23, 'mochila': 24, 'paraguas': 25, 'bolso': 26, 'corbata': 27, 'maleta': 28, 'frisbee': 29, 'esquis': 30,
                'tabla de snowboard': 31, 'pelota de deportes': 32, 'cometa': 33, 'bate de beisbol': 34, 'guante de beisbol': 35, 'patineta': 36, 'tabla de surf': 37, 'raqueta de tenis': 38, 'botella': 39, 'copa de vino': 40, 'taza': 41, 'tenedor': 42, 'cuchillo': 43, 'cuchara': 44, 'cuenco': 45, 'platano': 46, 'manzana': 47, 'sandwich': 48, 'naranja': 49, 'brocoli': 50, 'zanahoria': 51, 'perro caliente': 52, 'pizza': 53, 'dona': 54, 'pastel': 55, 'silla': 56,
                'sofa': 57, 'planta en maceta': 58, 'cama': 59, 'mesa de comedor': 60, 'inodoro': 61, 'television': 62, 'portatil': 63, 'raton': 64, 'control remoto': 65, 'teclado': 66, 'telefono celular': 67, 'microondas': 68, 'horno': 69, 'tostadora': 70, 'fregadero': 71, 'refrigerador': 72, 'libro': 73, 'reloj': 74, 'jarron': 75, 'tijeras': 76, 'osito de peluche': 77, 'secador de pelo': 78, 'cepillo de dientes': 79}

        #Comprobacion de los switches seleccionados
        lista=comprobar_switches(self)
        print(lista)
        if len(lista)>=80:
            self.list=lista
        else:
            for eleme in lista:
                self.list.append(dic[eleme])
        return self.list
    
    #-------------
    #Funcion que define la fuente de informacion para video y webcam
    #-------------
    def iniciar_web():

        #Definimos el máximo inicial
        self.max=0
        self.pers_vis_entr_max.delete(0)

        #Definimos la fuente de informacion en funcion del modo de deteccion
        if self.modo=='Webcam':
            self.video = cv2.VideoCapture(0)
        elif self.modo=='Video':
            self.video = cv2.VideoCapture(self.ruta)
        elif self.modo=='Imagen':
            ...
        main()

    # detener, detiene la ejecucion de la deteccion
    def detener():
        self.video = None
        etiq_video.place_forget()
        etiq_video.image = ''
        self.ret = False

    # soltar_listo, al seleccionar un nuevo switch teniendo marcada la opcion de seleccion lista, la deselecciona
    # esto evita errores durante la ejecucion
    def soltar_listo():
        if self.checkbox_1.get()==1:
            self.checkbox_1.deselect()
            detener()
        else:
            ...

    #-------------------------------------------#
    #DEFINICION DE LOS COMANDO QUE SE PUEDEN EJECUTAR EN LA VENTANA DE DETECCION
    #-------------------------------------------#

    #------------
    #Funcion para el envio de comandos en el fram de deteccion
    #-----------------
    def comandos():
        text_lst=self.entrada_comandos.get().split(sep=' ')

        #Comprobamos si hay texto escrito en el text entry
        if len(text_lst)==0:
            print('No se ha introducido ningun comando')
        elif len(text_lst)==2:
            texto = text_lst[0]
            ruta = text_lst[1]
            if os.path.exists(ruta)==False:
                print('La ruta introducida no existe, introduce la ruta absoluta')
            else:

                #Actualizamos los parametros en caso de que se trate de una imagen
                if texto=='i':
                    self.modo='Imagen'
                    self.ruta = ruta
                    valor=comprobacion_img(self.ruta)
                    if valor==True:
                        textbox.delete('1.0','end')
                        textbox.insert('0.0', text=(f'Modo de deteccion: {self.modo}\n'
                                        f''))
                        info_env() 

                #Actualizamos los parametros en caso de que se trate de un video
                elif texto=='v':
                    self.modo = 'Video'
                    self.ruta=ruta
                    valor=comprobacion_video(self.ruta)
                    if valor==True:
                        textbox.delete('1.0', 'end')
                        textbox.insert('0.0', text=(f'Modo de deteccion: {self.modo}\n'
                                        f''))
                        info_env()
                    
                else:
                    print('\nEl comando introducido no existe revisa el manual de comandos\n')

        elif len(text_lst)==1:
            texto = text_lst[0]
            if texto=='w':
                self.modo = 'Webcam'
                textbox.delete('1.0', 'end')
                textbox.insert('0.0', text=(f'Modo de deteccion: {self.modo}\n'
                                        f''))
                info_env()
            else:
                print('\n El comando introducido no existe\n')
        elif len(text_lst)==5:
            self.database(text_lst)

    



    
    #------------------------
    #Funcion para la ventana de deteccion sobre pantalla
    #-------------------------
    def pantalla_detect():
        #Aseguramos que no se esta realizando deteccion en la ventana principal
        detener()

        #Minimizamos la ventana principal
        self.iconify()
        self.posicion=[]

        #Creacion de la ventana secundaria
        ventana_sec=ctk.CTk()
        ventana_sec.geometry(f'{300}x{300}')
        ventana_sec.resizable(width=False,height=False)
        ventana_sec.title('Deteccion sobre pantalla')

        #Frame general 
        frame_princ=ctk.CTkFrame(ventana_sec,width=250,height=235)
        frame_princ.place(x=25,y=0)

        #Personas vistas y cuadro de muestra
        pers_vis=ctk.CTkLabel(frame_princ,text='Personas vistas:')
        pers_vis.place(x=5,y=10)
        pers_vis_entr_2=ctk.CTkEntry(frame_princ,width=110)
        pers_vis_entr_2.place(x=120,y=10)

        #Modelo de deteccion para deteccion por pantalla
        modelo1=YOLO('res/yolov8m.pt')
        

        #--Funciones del frame
        def parar():
            #Para parar en caso de que se este ejecutanto por pantalla completa
            if pant_compl.get()==1:
                pant_compl.deselect()
            
            #Para parar en caso de que se este ejecutando por region
            self.validar=False

        def ini_detect():
            
            if pant_compl.get()==1 :

                #Toma de la captura y preprocesamiento de la imagen
                img=pyautogui.screenshot()
                print(img)
                img=np.array(img)
                img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

                #Ejecucion de la prediccion
                resultaados = modelo1(img, conf=0.5, classes=[0], verbose=False)[0]
                detecciones = sv.Detections.from_yolov8(resultaados)
                num_pers=len(detecciones)
                pers_vis_entr_2.delete(0,2)
                pers_vis_entr_2.insert(0,str(num_pers))
                print('ejecutando')

                pers_vis_entr_2.after(2,ini_detect)
            elif len(self.posicion)==4 and self.validar==True:
                img=pyautogui.screenshot(region=(self.posicion[0],self.posicion[1],self.posicion[2]-self.posicion[0],self.posicion[3]-self.posicion[1]))
                img=np.array(img)
                img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


                #Ejecucion de la prediccion
                resultaados = modelo1(img, conf=0.5, classes=[0], verbose=False)[0]
                detecciones = sv.Detections.from_yolov8(resultaados)
                num_pers=len(detecciones)
                pers_vis_entr_2.delete(0,2)
                pers_vis_entr_2.insert(0,str(num_pers))
                print('ejecutando')
                pers_vis_entr_2.after(2,ini_detect)
            else:
                print('Seleccione una region o marque pantalla completa')
            
        #Funcion para la eleccion del area de deteccion
        def eleccion1():
            if pant_compl.get()==1:
                pant_compl.deselect()
            self.validar=False

            #Crea una ventana transparente sobre la que haciendo drag con el raton se elige la zona
            vent_transp=tk.Tk()
            vent_transp.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')
            vent_transp.wait_visibility(self)
            vent_transp.wm_attributes('-alpha',0.3)
            
            vent_transp.title('Click Me')

            #Obtenemos las coordenadas al inicio del drag
            def ini_drag(event):
                self.x_1=event.x
                self.y_1=event.y

            #Obtenemos las coordenas del final del drag
            def fin_drag(event):
                self.x_2=event.x
                self.y_2=event.y

                #En caso de que el punto se haya seleccionado correctament
                if self.x_1==self.x_2 and self.y_1==self.y_2 or self.y_2<self.y_1 or self.x_2<self.x_1:
                    ...
                else:
                    self.posicion=[self.x_1,self.y_1,self.x_2,self.y_2]

                    #Introduccion de los valores de las coordenadas en la entradas correspondientes
                    x1_entry.delete(0,4)
                    x1_entry.insert(0,str(self.posicion[0]))
                    x2_entry.delete(0,4)
                    x2_entry.insert(0,str(self.posicion[2]))
                    y1_entry.delete(0,4)
                    y1_entry.insert(0,str(self.posicion[1]))
                    y2_entry.delete(0,4)
                    y2_entry.insert(0,str(self.posicion[3]))
                    
                    #Para permitir la deteccion ya que el punto elegido es correcto
                    self.validar=True

                    #Dibujo del recuadro elegido para la deteccion
                    #canvas=tk.Canvas(vent_transp,width=self.winfo_screenwidth(),height=self.winfo_screenheight(),bg='black')
                    #vent_transp.wait_visibility(canvas)
                    #vent_transp.wm_attributes('-alpha',0.6)
                    #canvas.create_rectangle(self.x_1,self.y_1,self.x_2,self.y_2,outline='white')
                    #canvas.pack()
                    vent_transp.destroy()

            #Indica que al realizar acciones con el click izquierdo del mouse conduza a su respectiva funcion
            vent_transp.bind('<ButtonPress-1>', ini_drag)  
            vent_transp.bind('<ButtonRelease-1>',fin_drag)

            vent_transp.mainloop()
        
        #Funcion para el boton de salir
        def exit():
            ventana_sec.destroy()
            self.deiconify()
            
        #Botones principales
        bot_inciar=ctk.CTkButton(ventana_sec,text='Iniciar',command=ini_detect,width=75)
        bot_inciar.place(x=15,y=250)
        bot_inciar=ctk.CTkButton(ventana_sec,text='Detener',command=parar,width=75)
        bot_inciar.place(x=100,y=250)
        bot_parar=ctk.CTkButton(ventana_sec,text='Salir',command=exit,width=75)
        bot_parar.place(x=190,y=250)
        bot_elec_area=ctk.CTkButton(ventana_sec,text='Elegir recuadro',command=eleccion1)
        bot_elec_area.place(x=90,y=200)
        pant_compl=ctk.CTkCheckBox(ventana_sec,text='Pantalla completa')
        pant_compl.place(x=90,y=170)

        #Definicion textos y entradas de los puntos
        x1=ctk.CTkLabel(frame_princ,text='X1')
        x1.place(x=5,y=40)
        x1_entry=ctk.CTkEntry(frame_princ,width=50)
        x1_entry.place(x=25,y=40)
        y1=ctk.CTkLabel(frame_princ,text='Y1')
        y1.place(x=110,y=40)
        y1_entry=ctk.CTkEntry(frame_princ,width=50)
        y1_entry.place(x=130,y=40)
        x2=ctk.CTkLabel(frame_princ,text='X2')
        x2.place(x=5,y=70)
        x2_entry=ctk.CTkEntry(frame_princ,width=50)
        x2_entry.place(x=25,y=70)
        y2=ctk.CTkLabel(frame_princ,text='Y2')
        y2.place(x=110,y=70)
        y2_entry=ctk.CTkEntry(frame_princ,width=50)
        y2_entry.place(x=130,y=70)


    #-----
    #Funcion para abrir el navegador de archivos
    #------
    def explorador():
        filename=()

        filetypes=(('Archivos de video',('*.mp4','*.mov')),
                    ('Archivos de imagen',('*.jpg','*jpeg','*.png')))
        
        filename = tk.filedialog.askopenfilename(initialdir = "/home/",
                                        title = "Elige un archivo",
                                        filetypes=filetypes)
        if filename !=() and filename!='':
            terminacion=filename.split(sep='.')[1]
            if terminacion=='mp4' or terminacion=='mov':
                self.modo='Video'
                self.ruta=filename
                textbox.delete('1.0', 'end')
                textbox.insert('0.0', text=(f'Modo de deteccion: {self.modo}\n'
                                            f''))
                info_env()
            elif terminacion=='jpeg' or terminacion=='jpg' or terminacion=='png':
                self.modo='Imagen'
                self.ruta=filename
                textbox.delete('1.0', 'end')
                textbox.insert('0.0', text=(f'Modo de deteccion: {self.modo}\n'
                                            f''))
            else:
                print('El archivo elegido no tiene el formato adecuado')



    ##########################################################################################
                #Definicion del resto de widgets del frame detector
    ##########################################################################################

    #Definicion del ancho y alto del frame de deteccion
    self.ancho_detec=round(0.43*self.ancho_pant)
    self.alto_detec= self.alto_pant

    #Creacion del frame
    frame_dete = ctk.CTkFrame(self,width=self.ancho_detec,height=self.alto_detec,corner_radius=0)
    frame_dete.grid(row=0,column=1,pady=12,sticky='nsew')
    self.titulo_dete=ctk.CTkLabel(frame_dete,text='Deteccion',font=ctk.CTkFont(size=24,weight='bold'))
    self.titulo_dete.place(x=round(0.75*self.ancho_detec),y=round(0.013*self.alto_pant))

    #Definicion etiqueta imagenes
    etiq_video = tk.Label(frame_dete)
    etiq_video.place(x=round(0.017*self.ancho_detec), y=round(0.064*self.alto_detec))
    self.boton_inciar_det=ctk.CTkButton(frame_dete,text='Iniciar',command=iniciar_web)
    self.boton_inciar_det.place(x=round(0.3*self.ancho_detec),y=round(0.55*self.alto_detec))
    self.boton_detener_det=ctk.CTkButton(frame_dete,text='Detener',command=detener)
    self.boton_detener_det.place(x=round(0.58*self.ancho_detec),y=round(0.55*self.alto_detec))

    #Frame para los switches
    scrollable_frame = ctk.CTkScrollableFrame(frame_dete, label_text="Opciones",label_font=ctk.CTkFont(size=16,weight='bold'))
    scrollable_frame.place(x=round(1.63*self.ancho_detec),y=round(0.013*self.alto_detec))
    scrollable_frame.grid_columnconfigure(0, weight=1)
    self.scrollable_frame_switches = []
    self.lista_objetos=self.lista_labels
    self.lista_objetos.insert(0,'Todos')
    i=0
    for elem in self.lista_objetos:
        self.switch = ctk.CTkSwitch(master=scrollable_frame, text=f"{elem}",command=soltar_listo)
        self.switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        i+=1
        self.scrollable_frame_switches.append(self.switch)
    self.checkbox_1 = ctk.CTkCheckBox(frame_dete,text='Seleccion preparada',command=self.comprobar_switches)
    self.checkbox_1.place(x=round(1.63*self.ancho_detec),y=round(0.35*self.alto_detec))

    self.lista_objetos.pop(0)
    #Barra introduccion de comandos
    self.entrada_comandos=ctk.CTkEntry(frame_dete,placeholder_text='Introduce un comando',width=round(0.92*self.ancho_detec))
    self.entrada_comandos.place(x=round(0.017*self.ancho_detec),y=round(0.9*self.alto_detec))
    img=Image.open('res/carpeta.png')
    img=ctk.CTkImage(light_image=img,dark_image=img)
    
    self.expl_arch=ctk.CTkButton(frame_dete,image=img,width=30,height=30,text='',command=explorador)
    self.expl_arch.place(x=round(0.94*self.ancho_detec),y=round(0.9*self.alto_detec))
    self.boton_comandos=ctk.CTkButton(frame_dete,text='Enviar',command=comandos)
    self.boton_comandos.place(x=self.ancho_detec,y=round(0.9*self.alto_detec))

    #Frame de informacion
    self.info_frame_ancho=round(0.45*self.ancho_detec)
    self.info_frame_alto=round(0.61*self.alto_detec)
    self.info_frame=ctk.CTkFrame(frame_dete,width=self.info_frame_ancho,height=self.info_frame_alto,corner_radius=5)
    self.info_frame.place(x=round(1.13*self.ancho_detec),y=round(0.064*self.alto_detec))
    self.titulo_info=ctk.CTkLabel(self.info_frame,text='Informacion', font=ctk.CTkFont(size=16,weight='bold'))
    self.titulo_info.place(x=round(0.16*self.info_frame_ancho),y=round(0.02*self.info_frame_alto))
    self.pers_vis=ctk.CTkLabel(self.info_frame,text='Personas vistas:')
    self.pers_vis.place(x=round(0.04*self.info_frame_ancho),y=round(0.104*self.info_frame_alto))
    self.pers_vis_entr=ctk.CTkEntry(self.info_frame)
    self.pers_vis_entr.place(x=round(0.47*self.info_frame_ancho),y=round(0.104*self.info_frame_alto))
    self.pers_vis_max=ctk.CTkLabel(self.info_frame,text='Personas máximo vistas:')
    self.pers_vis_max.place(x=round(0.04*self.info_frame_ancho),y=round(0.17*self.info_frame_alto))
    self.pers_vis_entr_max=ctk.CTkEntry(self.info_frame, width=round(0.37*self.info_frame_ancho))
    self.pers_vis_entr_max.place(x=round(0.62*self.info_frame_ancho),y=round(0.17*self.info_frame_alto))

    #Frame modos y rutas y botones
    textbox = ctk.CTkTextbox(frame_dete, width=round(0.41*self.ancho_detec),height=round(0.19*self.alto_detec))
    textbox.place(x=round(1.63*self.ancho_detec), y=round(0.4*self.alto_detec))
    textbox.insert('0.0', text=(f'Modo de deteccion: {self.modo}\n'
                                f''))
    self.switch_guardar = ctk.CTkSwitch(frame_dete, text='Guardar output')
    self.switch_guardar.place(x=round(1.63*self.ancho_detec), y= round(0.6*self.alto_detec) )
    self.switch_caras = ctk.CTkSwitch(frame_dete, text='Extraer personas')
    self.switch_caras.place(x=round(1.63*self.ancho_detec), y=round(0.64*self.alto_detec))
    self.switch_mostrar_caja = ctk.CTkSwitch(frame_dete, text='Dibujar recuadro')
    self.switch_mostrar_caja.place(x=round(1.63*self.ancho_detec), y=round(0.68*self.alto_detec))

    #Boton deteccion sobre pantalla
    self.detect_pant=ctk.CTkButton(frame_dete,text='Deteccion sobre pantalla'
                                    ,command=pantalla_detect)
    self.detect_pant.place(x=round(1.63*self.ancho_detec),y=round(0.74*self.alto_detec))

    #Frame Dispositivos
    self.frame_disp=ctk.CTkFrame(frame_dete,width=round(0.9*self.ancho_detec),height=round(0.28*self.alto_detec),corner_radius=5)
    self.frame_disp.place(x=round(0.017*self.ancho_detec),y=round(0.6*self.alto_detec))
    treeview=ttk.Treeview(self.frame_disp)
    treeview['columns']=('Nombre','Activo','IP')
    
    treeview.column('#0',width=0,stretch='NO')
    treeview.column('Nombre',anchor='center')
    treeview.column('Activo',anchor='center')
    treeview.column('IP',anchor='center')

    treeview.heading('Nombre',text='Nombre',anchor='center')
    treeview.heading('Activo',text='Activo',anchor='center')
    treeview.heading('IP',text='IP',anchor='center')

    barra_desl=ttk.Scrollbar(self.frame_disp)
    barra_desl.pack(side='right',fill='y')

    treeview['yscrollcommand']=barra_desl.set

    for disp in db.Dispositivos.lista:
            treeview.insert(
                    parent='',
                    index='end',
                    iid=disp.nombre,
                    values=(disp.nombre,disp.activo,disp.ip),

            )
    treeview.pack()

    frame_dete.tkraise()
