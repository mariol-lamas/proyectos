import customtkinter as ctk


#Funcion para la comprobacion de switches
def comprobar_switches(self):
        lista=[]
        self.lista_objetos
        if self.switch_caras.get()==1:
            self.caras=True
        else:
            self.caras = False
        if self.switch_guardar.get()==1:
            self.guardar=True
        else:
            self.guardar = False

        i=0

        for elem in self.lista_objetos:
            if self.scrollable_frame_switches[i].get()==1 and self.scrollable_frame_switches[i]._text=='Todos':
                lista = [i for i in range(80)]
            elif self.scrollable_frame_switches[i].get()==1 and self.scrollable_frame_switches[i]._text!='Todos':
                lista.append(elem)
            i+=1
        return lista

def change_appearance_mode_event(self, new_appearance_mode: str):
        dic={'Claro':'Light','Oscuro':'Dark'}
        valor = dic[new_appearance_mode]
        ctk.set_appearance_mode(valor)
