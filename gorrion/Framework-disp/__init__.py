from Framework.dispositivo_framework import App
import pyautogui
import os
import uuid
import json


if __name__=='__main__':
    if os.path.exists('./res/info_disp.json'):
        app=App(pyautogui.size().width,pyautogui.size().height)
        app.mainloop()
    else:
        inf={'identificador':str(uuid.uuid4())}
        nombre_disp=str(input('Introduce un nombre para el dispositivo: '))
        inf['nombre']=nombre_disp
        with open('./res/info_disp.json','w') as jsonfile:
            json.dump(inf,jsonfile)
        jsonfile.close()
        app=App(pyautogui.size().width,pyautogui.size().height)
        app.mainloop()
