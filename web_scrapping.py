from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from time import sleep
import pandas as pd
from IPython.display import display
from datetime import date

class Scraper:
    
    def __init__(self) -> None:
        self.driver = None
    
    def open_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920, 1080)

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def get_produto_info(self, url):
        """Coleta as informações dos produtos de acordo com o link fornecido"""
        self.driver.get(url)
        sleep(5)

        nome_produto = self.driver.find_element(By.XPATH,
                                   '//*[@id="__next"]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div/h1').text
        valor_produto = self.driver.find_element(By.XPATH,
            '//*[@id="__next"]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/a/div/strong').text
        
        return nome_produto, valor_produto
    
    """def capture_graph(self):
        hist = self.driver.find_element(By.XPATH, By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[3]/a[1]')
        hist.click()
        sleep(5)

        grafico = self.driver.find_element(By.XPATH,
                              '//*[@id="__next"]/div[1]/div[3]/div[3]/div/div/section[2]/div/div/div[1]/div[1]/canvas')
        grafico_imagem = grafico.screenshot_as_png

        with open('grafico.png', 'wb') as arquivo:
            arquivo.write(grafico_imagem)"""
        
    def save_to_dataframe(self, df, nome_produto, valor_produto):
        nome_produto = ' '.join(nome_produto.split()[:4])

        nova_consulta = {'Produto': nome_produto, 'Valor': valor_produto, 'Dia de consulta': date.today()}
        df.loc[len(df)] = nova_consulta
        return df
    
    def raspagem(self, urls):
        df = pd.DataFrame(columns=['Produto', 'Valor', 'Dia de consulta'])

        print('Link dos produtos:\n')
        while True:
            resp = input('Digite o link do produto (Sair p/ encerrar):')
            if resp.lower() != 'sair':
                urls.append(resp)
            else:
                break
        
        self.open_browser()
        for url in urls:
            nome_produto, valor_produto = self.get_produto_info(url)
            #self.capture_graph()
            df = self.save_to_dataframe(df, nome_produto, valor_produto)
        
        df.to_excel('dados.xlsx')
        print('Dados salvos na planilha!')
        
        display(df)
        self.close_browser()

urls = []
scraper = Scraper()
scraper.raspagem(urls)
