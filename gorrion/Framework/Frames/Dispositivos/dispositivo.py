import csv

class Dispositivo():
    def __init__(self,nombre,usuario,password,identificador,ip,activo='No'):
        self.nombre=nombre
        self.activo=activo
        self.usuario=usuario
        self.password=password
        self.id=identificador
        self.ip=ip
        pass

    def __str__(self):
        return f'El dispositivo {self.nombre} , esta {self.activo} activo\nSu identificador es {self.id} y su IP es {self.ip}.\n Su usuario es {self.usuario} y para ver su contraseña comprobar la base de datos.'
    




class Dispositivos():

    lista=[]
    with open('./info/dispositivos.csv',newline='\n') as data:
        reader=csv.reader(data,delimiter=';')
        for nombre,usuario,password,identificador,ip,activo in reader:
            disp=Dispositivo(nombre,usuario,password,identificador,ip,activo)
            lista.append(disp)

    @staticmethod
    def buscar(nombre):
        for dispositivo in Dispositivos.lista:
            if dispositivo.nombre== nombre:
                return dispositivo
    
    @staticmethod
    def crear(nombre,usuario,password,identificador,ip,activo='No'):
        disp=Dispositivo(nombre,usuario,password,identificador,ip,activo)
        Dispositivos.lista.append(disp)
        Dispositivos.guardar()
        return disp
    
    @staticmethod
    def modificar(nombre,usuario,password,identificador,ip,activo):
        for index,dispositivo in enumerate(Dispositivos.lista):
            if dispositivo.nombre==nombre:
                    Dispositivo.lista[index].usuario=usuario
                    Dispositivo.lista[index].password=password
                    Dispositivo.lista[index].identificador=identificador
                    Dispositivo.lista[index].ip=ip
                    Dispositivo.lista[index].activo=activo
                    Dispositivos.guardar()
                    return Dispositivos.lista[index]
    
    @staticmethod
    def eliminar(nombre):
        for index,disp in enumerate(Dispositivos.lista):
            if disp.nombre == nombre:
                disp=Dispositivos.lista.pop(index)
                Dispositivos.guardar()
                return disp
    
    @staticmethod
    def guardar():
        print('Guardando...')
        with open('./info/dispositivos.csv','w',newline='\n') as data:
            writer=csv.writer(data,delimiter=';')
        
            for disp in Dispositivos.lista:
                writer.writerow((disp.nombre,disp.usuario,disp.password,disp.id,disp.ip,disp.activo))
        data.close()
