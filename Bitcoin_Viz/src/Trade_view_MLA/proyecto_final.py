import subprocess
archivo_requirements = "Bitcoin_Viz/requirements.txt"
# Ejecuta el comando pip para instalar los paquetes del archivo requirements.txt
subprocess.call(['pip', 'install', '-r', archivo_requirements])



class Test(unittest.TestCase):
    def setUp(self):
        self.divisas=('BTC/EUR','BTC/USD','ETH/EUR','ETH/USD','ETH/BTC')
        self.intervalos=(1,15,30,60,60*24)
        self.columnas=['timestamp', 'open', 'high','low','close','_','volume','conteo']
        self.app=App()
    
    def test_obtencion_datos(self):
        for divisa in self.divisas:
            for interval in self.intervalos:
                df=self.app.obt_datos(divisa,interval,[])
                self.assertEqual(df.empty,False,f'No se han recibido datos para la divisa {divisa} ')
                for col in self.columnas:
                    self.assertIn(col,df.columns,f'La columna {col} no existe en el DataFrame')
        
class App():
    
    def __init__(self):
        self.kraken=krakenex.API()
        self.intervalos={'1m':1,'15m':15,'30m':30,'1h':60,'24h':60*24}
    
    def barra_lat(self):
        '''
        Funcion encargada de la definición de los elementos de 
        la barra lateral.

        Devuelve:
        Divisa --> Se corresponde con el nombre del par divisa en formato wsname
        Intervalo --> 
        Indicadores --> Devuelve los indicadores a mostrar en el gráfico
        '''
        with st.sidebar:
            st.write('Opciones del gráfico')
            divisa=st.selectbox(
                'Par de divisas',
                ('BTC/EUR','BTC/USD','ETH/EUR','ETH/USD')
            )
            intervalo = st.selectbox(
                    'Intervalo',
                    ('1m', '15m', '30m','1h','24h'),
                    index=1)
            indicadores = st.multiselect(
                    'Indicadores',
                    ['VWAP', 'STOCH', 'BANDS'],
                    [],)
            
            vol=st.checkbox('Mostrar volumen')
            self.test=st.checkbox('Realizar test')
        return divisa,intervalo,indicadores, vol
    
    def calc_stoch(self,df,n,smooth_k,smooth_d):
        # Calcular el %K
        low_min = df['low'].rolling(n).min()
        high_max = df['high'].rolling(n).max()
        df['%K'] = ((df['close'] - low_min) / (high_max - low_min)) * 100

        # Aplicar un suavizado a %K
        df['%K_Smooth'] = df['%K'].rolling(smooth_k).mean()

        # Calcular %D
        df['%D'] = df['%K_Smooth'].rolling(smooth_d).mean()
        return df
    
    def calc_bbands(self,df, window=20, num_std_dev=2):
        # Calcular la media móvil simple (banda central)
        df['SMA'] = df['close'].rolling(window=window).mean()
        
        # Calcular la desviación estándar (volatilidad)
        df['STD'] = df['close'].rolling(window=window).std()
        
        # Calcular las bandas de Bollinger
        df['banda_sup'] = df['SMA'] + (df['STD'] * num_std_dev)
        df['banda_inf'] = df['SMA'] - (df['STD'] * num_std_dev)
        
        return df
    
    def obt_datos(self,par,intervalo,ind):
        '''
        Se encarga de realizar la query a la API de kraken para obtener los datos a partir del par de divisas
        y del intervalo de datos ya que estas queries devuelven un máximo de 720 valores.
        Devuelve -> Dataframe con columnas ['timestamp','open','high','low','close','volume','conteo']
        '''
        ohlc_data =requests.get(f'https://api.kraken.com/0/public/OHLC?pair={par}&interval={intervalo}')

        try:
            ohlc_data=ohlc_data.json() 
            ohlc_list = ohlc_data['result']
            print(ohlc_list)
            df=pd.DataFrame(ohlc_list[par],columns=['timestamp', 'open', 'high','low','close','_','volume','conteo'])
            #df['Date']=df['timestamp'].map(lambda x: datetime.datetime.fromtimestamp(x))
            df['Date']=pd.to_datetime(df['timestamp'],unit='s')
            df['Date_str']=df['Date'].astype(str)
            df['color']=df[['close','open']].apply(lambda x: 'red' if x.open>x.close else 'green',axis=1 )
            df['open']=df['open'].astype(float)
            df['close']=df['close'].astype(float)
            df['high']=df['high'].astype(float)
            df['low']=df['low'].astype(float)
            df['volume']=df['volume'].astype(float)

            if 'VWAP' in ind:
                df['Cum_Vol'] = df.iloc[::-1]['volume'].cumsum()
                df['m']=(df['close'])*df['volume']
                df['m_cum']=df.iloc[::-1]['m'].cumsum()
                df['VWAP'] = df['m_cum'] / df['Cum_Vol']

            if 'STOCH' in ind:
                df = self.calc_stoch(df,14,3,3)
            if 'BANDS' in ind:
                df = self.calc_bbands(df)
            return df
        
        except KeyError:
            st.write('No se dispone de información del par de divisas escogido')
            return pd.DataFrame([])

    def crear_graf(self,df,ind,vol,div):
        df=df[::-1]
        df_reduce=df[:46].copy()
        start=df_reduce['Date'].values.min()
        end=df_reduce['Date'].values.max()
        start_y= int(df_reduce['low'].values.min())*0.999
        end_y=int(df_reduce['high'].values.max())*1.001
        
        candle=figure(x_axis_type='datetime',height=300,x_range=(df['Date'].values[-1],df['Date'].values[0]),
                      tooltips=[('Date','@Date_str'),('open','@open'),('close','@close'),('high','@high'),('low','@low'),
                                ('color','@color')],y_axis_label='Precio',toolbar_location=None,
                                title=f'{div}')
    
        candle.segment('Date','low','Date','high',color='black',line_width=.5,source=df)
        candle.segment('Date','open','Date','close',color='color',line_width=6,source=df)
        candle.title.align='center'
        candle.title.text_font_size='16pt'
        candle.x_range.start= start
        candle.x_range.end= end
        candle.y_range.start=start_y
        candle.y_range.end = end_y
        children=[candle]

        if 'VWAP' in ind:
            candle.line('Date', 'VWAP', line_color="blue", line_width=.5, legend_label="VWAP-",source=df)
        
        
        if vol:
            volumen=figure(x_axis_type='datetime',height=120,x_range=(df['Date'].values[-1],df['Date'].values[0]),y_axis_label='Volumen',
                           toolbar_location=None)
            volumen.segment('Date',0,'Date','volume',color='color',line_width=6,source=df)
            volumen.yaxis.formatter = NumeralTickFormatter(format="0")
            volumen.x_range=candle.x_range
            children.append(volumen)
        
        if 'STOCH' in ind:
            estocast=figure(x_axis_type='datetime',height=100,x_range=(df['Date'].values[-1],df['Date'].values[0]),y_axis_label='STOCH',
                            toolbar_location=None)
            estocast.line('Date','%K_Smooth',line_color='blue',line_width=.5,legend_label='slowk',source=df)
            estocast.line('Date','%D',line_color='orange',line_width=.5,legend_label='slowd',source=df)
            estocast.x_range=candle.x_range
            children.append(estocast)
        if 'BANDS' in ind:
            candle.line('Date','banda_sup',line_color='green',line_width=.5,source=df)
            candle.line('Date','banda_inf',line_color='red',line_width=.5,source=df)
            candle.varea('Date', 'banda_sup', 'banda_inf', fill_color="gray", alpha=0.5,source=df)
            
        return column(children=children,sizing_mode='scale_width')

    def centro(self,fig):
        st.header("INTERACTIVE TRADING VIEW     BTC & ETH", divider='rainbow')
        st.bokeh_chart(fig,use_container_width=True)
    
    def run(self):
        st.set_page_config(page_title='INTERACTIVE TRADING VIEW') 
        divisa, intervalo, indicadores, vol=self.barra_lat()
        dataframe=self.obt_datos(divisa,self.intervalos[intervalo],indicadores)   #'XXBTZEUR'
        if not dataframe.empty:
            fig=self.crear_graf(dataframe,indicadores,vol,divisa)
            self.centro(fig)
        if self.test:
            try:
                test=Test()
                test.setUp()
                test.test_obtencion_datos()
                st.write('Todo ha ido correcto')
            except AssertionError:
                st.write('\n Han ocurrido errores durante el testeo')



if __name__=='__main__':
    archivo_requirements = "Bitcoin_Viz/requirements.txt"
    # Ejecuta el comando pip para instalar los paquetes del archivo requirements.txt
    subprocess.call(['pip', 'install', '-r', archivo_requirements])
    import pandas as pd
    import streamlit as st
    from bokeh.plotting import figure, column
    from bokeh.models import NumeralTickFormatter
    import unittest
    import requests
    app=App()
    app.run()
    
    

