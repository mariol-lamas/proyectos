#CONTENIDO DEL ARCHIVO .PY (ADAPTACION DEL IPYNB PARA EL FLUJO AUTOMATIZADO)
#!/usr/bin/env python3
#IMPORTACION DE PAQUETES
import requests
import pandas as pd
import datetime
import numpy as np
import json
import eurostat

#CONSTANTES
URL_INE='https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/26061'
URL_POWER_BI='https://api.powerbi.com/beta/78954451-ce2d-4c90-ae61-68906e409956/datasets/1f36bc2c-4539-4f74-a5e7-ff1d7898ee51/rows?experience=power-bi&key=WyBo5NOrT%2FzlgJCPXglBxozLxm%2FMwLNKOMqY%2BLNxEuyIMGxtYysHpnIhTkEi%2FDW42TEVzd772kk68Bl6xQ2NmA%3D%3D'
URL_DATA='/Users/mariolamas/Desktop'


class Scrap():
    def __init__(self,url_ine,url_pw_bi,url_data):
        """
        INIT
        -----
        Se encarga de definir algunas constantes básicas que va a requerir la clase

        Args:
            url_ine (string): Url a la tabla del Ine
            url_pw_bi (string): Url del flujo de datos de POWERBI
            url_data (string): Url del equipo donde ubicar el archivo con los datos mergeados
        """
        self.url_ine=url_ine
        self.url_power_bi=url_pw_bi
        self.url_data=url_data
        self.code='prc_ipc_g20'
        self.headers={'Content-Type': 'application/json'}
        self.paises=['ESP','FR','EU27_2020','DE']
    
    def datos_ine_preprocess(self):
        """
        Data Ine Processed
        ------------------
        Esta funcion se encarga de recolectar los datos del INE y procesarlos

        Returns:
            pd.DataFrame: Datos del INE procesados.
        """
        r = requests.get(self.url_ine)
        data = r.json()
        #prettify
        df=pd.DataFrame(data)
        data=pd.DataFrame(df.iloc[0,-1])
        data['date']=data[['Anyo','FK_Periodo']].apply(lambda x: f'{x.Anyo}-{x.FK_Periodo}',axis=1)
        data=data.drop(['Fecha','FK_TipoDato','FK_Periodo','Anyo','Secreto'],axis=1)
        data.rename(columns={'Valor':'ESP'},inplace=True)
        return data

    def data_eur_processed(self):
        """
        Data Eurostat Processed
        -----------------------
        Esta funcion se encarga de recolectar los datos de eurostat y procesarlos

        Returns:
            pd.DataFrame: Datos de EUROSTAT procesados.
        """
        data_euro = eurostat.get_data_df(self.code)
        data_euro=data_euro.transpose().iloc[-1:1:-1]
        data_euro.columns=data_euro.iloc[-1,:]
        data_euro=data_euro.iloc[:-1,0:20].copy()
        data_euro.reset_index(inplace=True)
        data_euro.rename(columns={'index':'date'},inplace=True)
        return data_euro

    def data_merge(self,data_ine,data_eur):
        """
        Data Merge
        -----------
        Funcion encargada de mergear los datos de los Dataframes preprocesados del INE y EUROSTAT

        Args:
            data_ine (pd.DataFrame): Datos preprocesados del INE
            data_eur (pd.DataFrame): Datos preprocesados de EUROSTAT

        Returns:
            pd.DataFrame: Datos unidos del INE con EUROSTAT
        """
        data_merged=pd.merge(data_ine, data_eur, on='date', how='inner')
        data_merged['pred_place_holder']=1
        return data_merged
    
    def push_pw_bi(self,data_merged):
        """
        Push to POWERBI
        -----------------
        Este metodo se encarga de enviar los datos procesados a un streaming de datos de powerbi a traves de la url proporcionada

        Args:
            data_merged (pd.DataFrame): DataFrame con los datos limpios y procesados del INE y EUROSTAT
        """
        #Convertimos el dataframe al formato de diccionario requerido por el data streaming
        dict_list = []
        # Iteramos sobre cada fila del DataFrame
        for _, row in data_merged.iterrows():
            item_dict={}
            item_dict['Fecha']=str(datetime.datetime(day=1,month=int(row['date'].split('-')[1]),year=int(row['date'].split('-')[0])))
            for pais in self.paises:
                # Creamos un diccionario con los valores de cada fila
                item_dict[pais]=row[pais]
                # Agregamos este diccionario a la lista
            dict_list.append(item_dict)
        
        #HACEMOS EL POST REQUEST
        response = requests.request(
            method="POST",
            url=self.url_power_bi,
            headers=self.headers,
            data=json.dumps(dict_list))
    

    def guardar_info(self,data):
        """
        Guardar info
        -------------

        Esta funcion de encarga de guardar la informacion de los datos procesados en un archivo datos_scrap.json
        Args:
            data (pd.DataFrame): Datos mergeados y procesados del INE y EUROSTAT
        """
        with open(f'{self.url_data}/data_scrap.json','w') as archivo:
            json.dump(data.to_dict(),archivo)
        archivo.close()
    
    def run(self):
        """
        Run
        ----
        Este método se encarga de definir el flujo de ejecucion de las diferentes funcionalidades del scraper de datos del INE y EUROSTAT
        """
        data_ine=self.datos_ine_preprocess()
        data_eur=self.data_eur_processed()
        data_merged=self.data_merge(data_ine=data_ine,
                                    data_eur=data_eur)
        try:   
            self.push_pw_bi(self.url_power_bi,data_merged=data_merged)
        except:
            print('La URL de POWERBI introducida no es correcta')
        self.guardar_info(data_merged)


if __name__=='__main__':
    #Creamos una instancia de la clase y llamamos al método run
    scraper=Scrap(URL_INE,URL_POWER_BI,URL_DATA)
    scraper.run()
