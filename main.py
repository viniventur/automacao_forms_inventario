from dotenv import load_dotenv, dotenv_values
env = dotenv_values('.env')
import pandas as pd
import time
import streamlit as st
from utils.chrome import chrome
from utils.xpaths import relacao_xpath_cadastro, relacao_xpath_registro

from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedTagNameException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from utils.funcoes import *


def main():
    st.title("Preenchedor de Formulário de Invetário de Dados")

    # Carrega dados
    df_cadastro = pd.read_excel("base_dados/relacao_dados.xlsx", sheet_name="cadastro")
    df_perguntas = pd.read_excel("base_dados/relacao_dados.xlsx", sheet_name="perguntas")
    st.subheader("Planilha: perguntas")
    st.dataframe(df_perguntas, use_container_width=True)
    st.subheader("Planilha: cadastro")
    st.dataframe(df_cadastro, use_container_width=True)

    # Iniciar navegador e abrir form
    if st.button("iniciar"):
        st.cache_data.clear()
        st.cache_resource.clear()
        driver = get_driver()
        open_form(driver)
        st.success("Navegador iniciado e formulário aberto.")

    if st.button("Página de Cadastro"):
        try:
            driver = st.session_state.driver
            wait = WebDriverWait(driver, 20)
            for pergunta in df_cadastro.columns:

                try:

                    if pergunta == 'Secretaria:':
                        escolher_opcao('Secretaria:', df_cadastro[pergunta].iloc[0])               
                        continue

                    inserir_input(pergunta, df_cadastro[pergunta].iloc[0])
                except Exception as e:
                    st.error(f'Erro na pergunta {pergunta}: {e}')

            avancar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]')))
            avancar.click()
        except Exception as e:
            st.error(f'Erro ao registra pagina de cadastro: {e}')


    if st.button('registrar inventario'):
        driver = st.session_state.driver
        wait = WebDriverWait(driver, 20)

        n_rows = len(df_perguntas)

        for i in range(n_rows):
            row = df_perguntas.iloc[i]
            ultima_resposta = ''

            for pergunta in df_perguntas.columns:
                try:
                    valor = row[pergunta]

                    if 'Não' in str(ultima_resposta) and 'Se sim' in pergunta:
                        st.text(ultima_resposta)
                        ultima_resposta = ''
                        continue

                    st.warning(pergunta)

                    if 'radio' in pergunta:
                        st.warning(pergunta.replace('radio-', ''))
                        responder_radio(pergunta.replace('radio-', ''), valor)
                        ultima_resposta = valor
                        continue

                    if 'checkbox' in pergunta:
                        st.warning(pergunta.replace('checkbox-', ''))
                        valores = str(valor or '')
                        itens = [p.strip().rstrip(':') for p in valores.split(',') if p.strip()]
                        for item in itens:
                            st.success(item)
                            clicar_checkbox(pergunta.replace('checkbox-', ''), item)
                        continue

                    if ('Se outro for marcado, descreva:' in pergunta) and ('' not in str(ultima_resposta)) and (valor != None):
                            responder_outros(valor)
                            continue
                    elif ('Se outro for marcado, descreva:' in pergunta) and ('' in str(ultima_resposta)):
                        responder_outros(' ')
                        continue

                    inserir_input(pergunta, valor)
                    ultima_resposta = valor

                    avancar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]')))
                    avancar.click()

                    if valor == 'Não':
                        st.success('fim')


                except Exception as e:
                    st.error(f"Erro na linha {i+1}, pergunta {pergunta}: {e}")

            # # ---- AO FINAL DA LINHA: checa se é a última ----
            # if i == n_rows - 1:

            #     avancar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]')))
            #     avancar.click()
                
            # (se não for a última, o loop simplesmente continua para a próxima linha)

    if st.button('clicar_radio'):
        responder_radio("Há informações disponíveis em formato de Dados Abertos?", 'Não, mas há necessidade')


    if st.button('clicar-check'):
        clicar_checkbox('Se sim, como é feito o envio para a alta gestão?', 'Relatório')

    if st.button('teste_forms_input'):
        inserir_input('Se sim, como é feito o envio para a alta gestão?', "Programa XYZ")


    if st.button('responder outros'):
        responder_outros('Se sim, como é feito o envio para a alta gestão?', 'teste outro')

        
if __name__ == "__main__":
    main()
