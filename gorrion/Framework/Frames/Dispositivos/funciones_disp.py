
from typing import Optional, Tuple, Union
import customtkinter as ctk
import Framework.Frames.Dispositivos.dispositivo as db

def validar_ip(valor,disp):
    if len(valor)>3:
        return False
    else:
        return True

class Vent_ana(ctk.CTk):
    def __init__(self,self2):
        super().__init__()
        self.self2=self2
        self.geometry('300x500')
        self.resizable(width=False,height=False)

        #Nombre
        texto_name=ctk.CTkLabel(self,text='Nombre',font=ctk.CTkFont(size=14,weight='bold'))
        texto_name.place(x=120,y=10)
        self.text_nombre=ctk.CTkEntry(self,width=200,height=20)
        self.text_nombre.place(x=50,y=50)

        #Activo
        self.activo=ctk.CTkCheckBox(self,text='Activo',font=ctk.CTkFont(size=14,weight='bold'))
        self.activo.place(x=100,y=80)

        #Usuario
        texto_user=ctk.CTkLabel(self,text='Usuario',font=ctk.CTkFont(size=12,weight='bold'))
        texto_user.place(x=120,y=105)
        self.text_usuario=ctk.CTkEntry(self,width=200,height=20)
        self.text_usuario.place(x=50,y=130)

        #Password
        texto_pass=ctk.CTkLabel(self,text='Password',font=ctk.CTkFont(size=14,weight='bold'))
        texto_pass.place(x=120,y=160)
        self.text_password=ctk.CTkEntry(self,width=200,height=20,show='*')
        self.text_password.place(x=50,y=200)

        texto_id=ctk.CTkLabel(self,text='Identificador',font=ctk.CTkFont(size=14,weight='bold'))
        texto_id.place(x=120,y=230)
        self.text_identificador=ctk.CTkEntry(self,width=200,height=20)
        self.text_identificador.place(x=50,y=270)

        #Campo IP
        texto_ip=ctk.CTkLabel(self,text='IP',font=ctk.CTkFont(size=14,weight='bold'))
        texto_ip.place(x=150,y=300)

        self.text_ip_1=ctk.CTkEntry(self,width=60,height=20,validate='key',validatecommand=(self.register(lambda text:text.isdecimal()),'%S'))
        self.text_ip_1.place(x=10,y=330)
        self.text_ip_1.bind('<KeyRelease>',lambda event: self.validar(event,0))
        punto_1=ctk.CTkLabel(self,text='.',font=ctk.CTkFont(size=14,weight='bold'))
        punto_1.place(x=80,y=330)

        self.text_ip_2=ctk.CTkEntry(self,width=60,height=20,validate='key',validatecommand=(self.register(lambda text:text.isdecimal()),'%S'))
        self.text_ip_2.place(x=90,y=330)
        self.text_ip_2.bind('<KeyRelease>',lambda event: self.validar(event,0))
        punto_2=ctk.CTkLabel(self,text='.',font=ctk.CTkFont(size=14,weight='bold'))
        punto_2.place(x=160,y=330)

        self.text_ip_3=ctk.CTkEntry(self,width=60,height=20,validate='key',validatecommand=(self.register(lambda text:text.isdecimal()),'%S'))
        self.text_ip_3.place(x=170,y=330)
        self.text_ip_3.bind('<KeyRelease>',lambda event: self.validar(event,0))
        punto_3=ctk.CTkLabel(self,text='.',font=ctk.CTkFont(size=14,weight='bold'))
        punto_3.place(x=240,y=330)

        self.text_ip_4=ctk.CTkEntry(self,width=60,height=20,validate='key',validatecommand=(self.register(lambda text:text.isdecimal()),'%S'))
        self.text_ip_4.place(x=250,y=330)
        self.text_ip_4.bind('<KeyRelease>',lambda event: self.validar(event,0))
        


        boton_salir=ctk.CTkButton(self,text='SALIR',command=self.salir)
        boton_salir.place(x=90,y=400,)
        boton_enviar=ctk.CTkButton(self,text='ENVIAR',command=self.enviar)
        boton_enviar.place(x=90,y=450)
    
    def validar(self,event,num):
        valor=event.widget.get()
        if num==0:
            valido=validar_ip(valor,db.Dispositivos.lista)
            if valido:
                event.widget.configure({'bg':'white'})
            else:
                event.widget.configure({'bg':'Red'})

    def enviar(self):
        ip=f'{self.text_ip_1.get()}.{self.text_ip_2.get()}.{self.text_ip_3.get()}.{self.text_ip_4.get()}'
        if self.activo.get()==1:
            activo='SI'
        else:
            activo='NO'
        disp=db.Dispositivos.crear(self.text_nombre.get(),self.text_usuario.get(),self.text_password.get(),
                                   self.text_identificador.get(),ip,activo)
        
        self.self2.treeview.insert(
            parent='',
            index='end',
            iid=disp.nombre,
            values=(disp.nombre,disp.activo,disp.ip),
        )
        print(db.Dispositivos.lista)
        self.salir()

    def salir(self):
        self.self2.deiconify()
        self.destroy()




class Ver_info(ctk.CTk):
    def __init__(self,self2,disp):
        super().__init__()
        self.self2=self2
        
        self.campos=self.self2.treeview.item(disp,'values')
        self.geometry('300x500')
        self.resizable(width=False,height=False)

    



        boton_salir=ctk.CTkButton(self,text='SALIR',command=self.salir)
        boton_salir.place(x=90,y=450)


        print(self.campos)
        

        
        


    def salir(self):
        self.self2.deiconify()
        self.destroy()

    
