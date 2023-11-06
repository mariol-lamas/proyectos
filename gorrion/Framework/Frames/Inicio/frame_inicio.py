import customtkinter as ctk



def frame_inicio(self):
        self.ancho_ini=round(0.43*self.ancho_pant)
        self.alto_ini= self.alto_pant

        #Creacion del frame
        frame_ini = ctk.CTkFrame(self,width=self.ancho_ini,height=self.alto_ini,corner_radius=10)
        frame_ini.grid(row=0,column=1,pady=12,sticky='nsew')
        

        #Titulo del frame
        titulo_ini=ctk.CTkLabel(frame_ini,text='BIENVENIDO A GORRIÓN',font=ctk.CTkFont(size=28,weight='bold'))
        titulo_ini.place(x=round(0.7*self.ancho_ini),y=30)
        
        #imagen_fondo=ctk.CTkLabel()

        textbox = ctk.CTkTextbox(frame_ini, width=round(1.9*self.ancho_ini),height=round(0.8*self.alto_ini))
        textbox.place(x=30,y=80)
        textbox.insert('0.0',text='')

        frame_ini.tkraise()
