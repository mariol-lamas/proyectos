'''
IMPORTACION DE PAQUETES
'''
import customtkinter as ctk
import tkinter as tk
import os
from Framework.funciones import comprobar_switches, change_appearance_mode_event
from Framework.Frames.Inicio.frame_inicio import frame_inicio
from Framework.Frames.Dispositivos.frame_dispositivo import frame_disp
from ultralytics import YOLO
import supervision as sv
import json
import cv2
import time
import imutils
from PIL import Image, ImageTk
import numpy as np
import pyautogui
from Framework.Frames.Detect.frame_detect import frame_det

#Valor de apariencia por defecto de la ventana
class App(tk.Tk):
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('green')

    def __init__(self, ancho,alto):
        super().__init__()

        ##PROPIEDADES POR DEFECTO
        self.ancho_pant=ancho
        self.alto_pant=750
        self.modo='Webcam'
        # configure window
        self.ruta_prog = os.getcwd()
        self.title("Gorrión")
        self.geometry(f'{self.ancho_pant}x750')
        self.resizable(width=False,height=False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #Obtencion lables
        with open('info/labels.json','r') as jsonfile:
            self.dic=json.load(jsonfile)
        self.lista_labels=[values for key,values in self.dic.items()]
        jsonfile.close()
        # configuracion de la barra lateral
        self.sidebar_frame = ctk.CTkFrame(self, width=round(self.ancho_pant*0.1), corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        #Definicion de los botones de la barra lateral
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MENU",
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame,text='Inicio',command=self.frame_inicio)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame,text='Dispositivos',command=self.frame_disp)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame,text='Deteccion',command=self.frame_detect)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text='Salir', command=self.salir)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        #Definicion del cambio de apariencia
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appariencia:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Claro", "Oscuro"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        #Llamamos al frame inicio
        frame_inicio(self)
    

    def frame_inicio(self):
        frame_inicio(self)

################################################
    #-----------------------------------------------
    #FRAME DEL DETECTOR
    #--------------------------------------------
################################################
    def frame_detect(self):
        frame_det(self)


    def frame_disp(self):
        frame_disp(self)
    #-----------------------------------------------
    #FUNCIONES GENERALES DEL FRAME LATERAL (TIRAN DEL ARCHIVO FUNCIONES.PY)
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        change_appearance_mode_event(self,new_appearance_mode)

    def salir(self):
        self.destroy()
    
    def comprobar_switches(self):
        comprobar_switches(self)
