import customtkinter as ctk
from tkinter import ttk
import Framework.Frames.Dispositivos.dispositivo as db
from tkinter.messagebox import askokcancel,WARNING
from Framework.Frames.Dispositivos.funciones_disp import Vent_ana, Ver_info

def frame_disp(self):
        #Funciones del frame
        def borrar():
                disp=self.treeview.focus()
                if disp:
                        campos=self.treeview.item(disp,'values')
                        confirmar=askokcancel(
                                title='Confirmar borrado',
                                message=f'¿Borrar {campos[0]}?',
                                icon=WARNING)

                        if confirmar:
                                self.treeview.delete(disp)
                                db.Dispositivos.eliminar(campos[0])
        
        def anadir():
                self.iconify()
                app_anadir=Vent_ana(self)
                app_anadir.mainloop()

        def info():
                disp=self.treeview.focus()
                if disp!='':
                        self.iconify()
                        app_info= Ver_info(self,disp)
                        app_info.mainloop()
                

        self.ancho_disp=round(0.43*self.ancho_pant)
        self.alto_disp= self.alto_pant

        #Creacion del frame
        frame_disp = ctk.CTkFrame(self,width=self.ancho_disp,height=self.alto_disp,corner_radius=10)
        frame_disp.grid(row=0,column=1,pady=12,sticky='nsew')

        titulo_dete=ctk.CTkLabel(frame_disp,text='Control de dispositivos',font=ctk.CTkFont(size=24,weight='bold'))
        titulo_dete.place(x=round(0.75*self.ancho_disp),y=round(0.013*self.alto_pant))

        frame_tabla=ctk.CTkFrame(frame_disp,width=round(self.ancho_disp),height=self.alto_disp*2)
        frame_tabla.place(x=50,y=70)
        
        treeview=ttk.Treeview(frame_tabla)
        treeview['columns']=('Nombre','Activo','IP')
        
        treeview.column('#0',width=0,stretch='NO')
        treeview.column('Nombre',anchor='center')
        treeview.column('Activo',anchor='center')
        treeview.column('IP',anchor='center')

        treeview.heading('Nombre',text='Nombre',anchor='center')
        treeview.heading('Activo',text='Activo',anchor='center')
        treeview.heading('IP',text='IP',anchor='center')

        barra_desl=ttk.Scrollbar(frame_tabla)
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

        #Definicion de los botones
        boton_anadir=ctk.CTkButton(frame_disp,text='AÑADIR',command=anadir)
        boton_mod=ctk.CTkButton(frame_disp,text='MODIFICAR',command=None)
        boton_borrar=ctk.CTkButton(frame_disp,text='BORRAR',command=borrar)
        boton_info=ctk.CTkButton(frame_disp,text='OBTENER INFO',command=info)
        boton_borrar.place(x=round(self.ancho_disp*1.2),y=70)
        boton_anadir.place(x=round(self.ancho_disp*1.2),y=120)
        boton_mod.place(x=round(self.ancho_disp*1.2), y=170)
        boton_info.place(x=round(self.ancho_disp*1.2),y=220)


        self.treeview=treeview

        #Frame analisis
        frame_analisis=ctk.CTkFrame(frame_disp,width=1.9*self.ancho_disp,height=round(self.alto_disp/1.8))
        frame_analisis.place(x=50, y=300)

        title_her=ctk.CTkLabel(frame_analisis,text='Herramienta de análisis',font=ctk.CTkFont(size=14,weight='bold'))
        title_her.place(x=round(0.9*self.ancho_disp),y=10)




        frame_disp.tkraise()

        
