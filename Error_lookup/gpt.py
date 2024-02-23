#IMPORTACION DE LOS PAQUETES REQUERIDOS
import undetected_chromedriver as uc    #Libreria para crear un driver que no es dectectado por el antibot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
import numpy as np
from bs4 import BeautifulSoup
import keyboard as kb
import os
from selenium.webdriver.common.keys import Keys


class GPT():
    def __init__(self,mail,password):
        self.mail=mail
        self.password=password
        self.p=0    #parrafos
        self.pre=0  #snipets de codigo
    
    #Funcion para arrancar el webdriver
    def iniciar_wd(self,headless=False,pos='maximize'):
        options=uc.ChromeOptions()
        options.add_argument('--password-store=basic')
        options.add_experimental_option(
            'prefs',
            {'credentials_enable_service':False,
            'profile.password_manager_enabled':False}
        )
        if headless:
            options.add_argument('--headless')

        #Iniciamos el driver
        self.driver=uc.Chrome(options=options,headless=headless,log_level=3)
        self.driver.maximize_window()
    
    def buscar_texto(self,texto):
        #Buscamos el area donde introducir el texto
        text=self.driver.find_element(By.XPATH,'//textarea[@tabindex=0]')
        text.send_keys(texto)
        text.send_keys(Keys.ENTER)

        time.sleep(10)
        #Obtenemos el texto de la respuesta
        parrafos = self.driver.find_elements(By.TAG_NAME,"p")
        textos=[parrafo.text for parrafo in parrafos]
        textos.remove('ChatGPT')
        textos_resp=textos[self.p:]
        self.p=len(textos)-self.p

        #Obtenemos el codigo de la respuesta(en caso de haberlo)
        soluciones=self.driver.find_elements(By.TAG_NAME,"pre")
        sols=[sol.text for sol in soluciones]
        sols_resp=sols[self.pre:]
        self.pre=len(sols)-self.pre
        sols_resp=[sol[sol.find('Copy code')+len('Copy code'):] for sol in sols_resp]

        return textos_resp,sols_resp
    
    def acceder_chat(self):

        #Accedemos a la pagina de chatgpt y creamos el wait
        self.driver.get('https://chat.openai.com/')
        self.wait=WebDriverWait(self.driver,30)
        time.sleep(np.random.randint(3,6))

        #Clicamos en el boton Log in
        log=self.wait.until(ec.element_to_be_clickable((By.XPATH,'//*[text()="Log in"]')))
        log.click()

        #Introducimos el mail y clicamos continuar
        mail=self.wait.until(ec.element_to_be_clickable((By.ID,'username')))
        mail.send_keys(self.mail)
        cont=self.wait.until(ec.element_to_be_clickable((By.XPATH,'//*[text()="Continuar"]')))
        cont.click()
        time.sleep(np.random.randint(1,3))

        #Introducimos la password y clicamos continuar
        passw=self.wait.until(ec.element_to_be_clickable((By.ID,'password')))
        passw.send_keys(self.password)
        cont=self.wait.until(ec.element_to_be_clickable((By.XPATH,'//*[text()="Continuar"]')))
        cont.click()
        time.sleep(np.random.randint(2,4))
    
    def cerrar_drv(self):
        self.driver.close()
        self.driver.quit()
    
    #Funcion para buscar solucion a errores con CHATGPT
    def buscar_errores(self,headless=False):
        print('-'*20,'\nIniciando el Driver\n','-'*20)
        self.iniciar_wd(headless=headless)
        print('-'*20,'\nAccediendo al chat\n','-'*20)
        self.acceder_chat()
        print('-'*20,'\nAcceso correcto!\n','-'*20)
        texto=''
        while texto.upper()!='Q':
            texto=str(input('\nPulsa Q para salir\nIntroduce el error a localizar: '))
            if texto.upper()!='Q':
                consulta=f'¿Que falla aqui?: {texto}'
                textos,codigo=self.buscar_texto(consulta)
                for text in textos:
                    print('El texto es: ',text)
                for cod in codigo:
                    print('El codigo es: ',cod)
        
        print('#'*20,'\nCERRANDO EL DRIVER\n','#'*20)
        self.cerrar_drv()


