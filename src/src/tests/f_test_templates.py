from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from src.tests.conftest import *

class TestCadastro:

    def setup_method(self, app):
        self.app = app
        global driver
        driver = webdriver.Chrome()

    def test_cadastroEscola(self, new_escolas, new_edificios):

        driver.get('http://127.0.0.1:5000/api/v1/send_frontend/cadastro-escolas')
        driver.maximize_window()
        time.sleep(1)

        # Execute suas ações no Selenium

        #Rolas pagina para baixo
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        #Selecinar formulário
        formulario_escolas = driver.find_element(By.ID, 'formulario-escolas')

        #Preencher formulário
        for keys, value in new_escolas.items():
            input_element = formulario_escolas.find_element(By.NAME, keys)
            input_element.send_keys(value)

        btn_proximo = driver.find_element(By.CLASS_NAME, 'botao')
        btn_proximo.click()

        driver.execute_script('console.log("alguma coisa")')

        time.sleep(1)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(0.2)

        btn_novo_cadastro = driver.find_element(By.CLASS_NAME, 'cadastroEdificacao')

        btn_novo_cadastro.click()
        time.sleep(0.1)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        formulario_edificios = driver.find_element(By.ID, 'formulario-edificacoes')

        formulario_edificios.find_element(By.ID, 'nome_do_edificio')

        for keys, value in new_edificios.items():
            if keys not in 'fk_escola reservatorio agua_de_reuso'.split(' '):
                elemento = formulario_edificios.find_element(By.NAME, keys)
                elemento.send_keys(value)

            elif keys in 'reservatorio agua_de_reuso'.split(' '):
                elemento = formulario_edificios.find_element(By.NAME, keys)
                elemento.click()
        btn_save_edificios = driver.find_element(By.ID, 'btn_save_edificio')
        btn_save_edificios.click()
        time.sleep(1)

    def teardown_class(self):
        driver.close()
