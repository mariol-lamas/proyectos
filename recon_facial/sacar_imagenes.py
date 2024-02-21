### CON ESTE PROGRAMA A PARTIR DE LA WEBCAM, GUARDAREMOS UN NUMERO DE IMAGENES EN UN DIRECTORIO ###
def sacar_imagenes(mtcnn):
    print('\n#-----------------------------#'
          '\nEn caso de no tener un directorio con imagenes de referencia'
          '\n#-----------------------------------------------------------#'
          '\n 1--> Sacar imagenes'
          '\n 2--> Ya tengo un directorio de referencia\n')

    try:
        i = int(input('Introduce el numero de tu eleccion: '))
        if i == 1:
            try:
                numero_imagenes = int(input('Introduce el numero de imagenes que quieres sacar: '))
                directorio = str(
                    input('Introduce el directorio donde quieres que se cree la carpeta con las imagenes: '))
                if os.path.exists(directorio) == True:
                    pass
                else:
                    print('El directorio introducido no existe')
                    ...
                if os.path.exists(directorio + '/imagenes') == True:
                    print('Borrar la capeta imagenes del directorio'
                          f'\n {directorio}')
                    ...
                else:
                    os.mkdir(directorio + '/imagenes')
                    os.mkdir(directorio + '/imagenes/persona1')
                imagen = cv2.VideoCapture(0)
                frame_exist = True
                i = 0
                while (frame_exist) and i < numero_imagenes:
                    frame_exist, frame = imagen.read()
                    bboxes, probs = mtcnn.detect(frame, landmarks=False)
                    if bboxes is not None:

                        for bbox in bboxes:
                            x1, y1, x2, y2 = bbox
                            cara = frame[int(round(y1)):int(round(y2)), int(round(x1)):int(round(x2))]
                            # Redimensionamiento del recorte
                            cara = Image.fromarray(cara)
                            cara = cara.resize(tuple([160, 160]))
                            cara = np.array(cara)
                            cv2.imwrite(directorio + f'/imagenes/persona1/{i}.jpg', cara)
                            plt.imshow(cara)
                            plt.show()
                        i += 1
                    else:
                        pass
                print('\n#---------------------------------------------------#'
                      '\nLas imagenes se han guardado en el siguiente directorio'
                      f'\n{directorio}/imagenes'
                      '\n#------------------------------------------------#\n')
            except TypeError or ValueError or AttributeError:
                print('\n#-----------------------------------------------------------------#'
                      '\nLos datos introducido para el numero de imagenes y el directorio no son correctos'
                      '\n NºImagenes--> numero redondo'
                      '\n directorio --> texto'
                      '\n#-----------------------------------------------------------------#')
        elif i == 2:
            pass
        else:
            print('\n#----------------------------#'
                  '\nEl numero introducido no es correcto'
                  '\n#-----------------------------#\n')
    except ValueError or TypeError or AttributeError:
        print('\n#----------------------------------------------#'
              '\nEl valor introducido no tiene el formato adecuado #Numerico entero'
              '\n#----------------------------------------------#')
