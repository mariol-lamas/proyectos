import customtkinter as ctk

#--------
#Funcion para comprobar si el video existe y su formato es correcto
#--------
def comprobacion_video(ruta):
    valor = ruta.rsplit(sep='.',maxsplit=1)
    if valor[1].lower()==('mp4'or'mov'):
        return True
    else:
        print('\n El formato de video introducido no es válido\n'
                'Los formatos permitidos son .mp4 .mov\n ')
        return False
    
#------------
#Funcion para comprobar si la imagen existe y su formato es correcto
#------------
def comprobacion_img(ruta):
    valor = ruta.rsplit(sep='.', maxsplit=1)
    if valor[1] == ('jpg' or 'png'or 'jpeg'):
        return True
    else:
        print('\n El formato de la imagen introducido no es válido\n '
                'Los formatos permitidos son .jpg .png .jpeg\n')
        return False

#----------
#Funcion para la venta de confirmacion d einfo enviada
#-----------------
def info_env():

    #Definicion de la ventana
    vent=ctk.CTk()
    vent.geometry(f'{330}x{100}')
    vent.resizable(width=False,height=False)
    titulo=ctk.CTkLabel(vent,text='INFORMACION ENVIADA CORRECTAMENTE',font=ctk.CTkFont(size=14,weight='bold'))
    titulo.place(x=10,y=30)

    #Funcion para cerrar la ventana una vez pulsado ok
    def cerrar_vent():
        vent.destroy()

    #Definicion del boton de ok
    boton_ok=ctk.CTkButton(vent,text='Ok',command=cerrar_vent)
    boton_ok.place(x=100,y=65)
