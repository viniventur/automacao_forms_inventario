from dotenv import load_dotenv, dotenv_values
env = dotenv_values('.env')
import pandas as pd
import time
import streamlit as st
from utils.chrome import chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select

def get_driver():
    """Garante um driver único na sessão do Streamlit."""

    if "driver" in st.session_state:
        st.session_state.driver.quit()
        st.session_state.driver = chrome()

    if "driver" not in st.session_state or st.session_state.driver is None:
        st.session_state.driver = chrome()
    return st.session_state.driver


def open_form(driver):
    driver.get(env['FORM_URL'])
    wait = WebDriverWait(driver, 20)
    # clica no primeiro "Próxima"/"Começar" se existir
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        ))
        btn.click()
    except TimeoutException:
        pass  # alguns forms já abrem direto na primeira página

def escolher_opcao(pergunta, escolha):
    driver = st.session_state.driver
    wait = WebDriverWait(driver, 20)

    texto = escolha           # valor a selecionar

    base = f'//div[contains(@data-params, "{pergunta}")]'
    opcao_xpath = (
        base
    )

    try:
        el = wait.until(EC.element_to_be_clickable((By.XPATH, opcao_xpath)))
        el.click()
    except Exception as e:
        st.error(f'Erro ao clicar na caixa de escolha: {e}')

    try:
        option_xpath = (f"//div[@role='option'][.//span[normalize-space(.)='{texto}']]")
        opt = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        opt.click()
        time.sleep(1.5)
    except Exception as e:
        st.error(f'Erro ao clicar na escolha: {e}')


def clicar_checkbox(pergunta, escolha):
    driver = st.session_state.driver
    wait = WebDriverWait(driver, 20)

    xpath = (
        f'//div[contains(@data-params, "{pergunta}")]'
        f'//div[@role="checkbox" and @data-answer-value="{escolha}"]'
    )

    el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    el.click()


def responder_outros(resposta):
    driver = st.session_state.driver
    wait = WebDriverWait(driver, 20)

    pergunta = 'Se sim, como é feito o envio para a alta gestão?'

    base = f'//div[contains(@data-params, "{pergunta}")]'

    field_xpath = (
        base + '//input[@aria-label="Outra resposta"] | '
        + base + '//textarea[@aria-label="Outra resposta"] | '
        + base + '//*[normalize-space()="Outra resposta" and @aria-hidden="true"]/preceding-sibling::input | '
        + base + '//*[normalize-space()="Outra resposta" and @aria-hidden="true"]/preceding-sibling::textarea'
    )

    campo = wait.until(EC.visibility_of_element_located((By.XPATH, field_xpath)))

    # foco e preenchimento (sem JS)
    ActionChains(driver).move_to_element(campo).click().perform()
    try:
        campo.clear()  # funciona para input/textarea
    except Exception:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACK_SPACE).perform()

    campo.send_keys(resposta)




def inserir_input(pergunta, resposta):
    driver = st.session_state.driver
    wait = WebDriverWait(driver, 20)

    base = f'//div[contains(@data-params, "{pergunta}")]'

    field_xpath = (
        base + '//input[@aria-label="Sua resposta"] | '
        + base + '//textarea[@aria-label="Sua resposta"] | '
        + base + '//*[normalize-space()="Sua resposta" and @aria-hidden="true"]/preceding-sibling::input | '
        + base + '//*[normalize-space()="Sua resposta" and @aria-hidden="true"]/preceding-sibling::textarea'
    )

    campo = wait.until(EC.visibility_of_element_located((By.XPATH, field_xpath)))

    # foco e preenchimento (sem JS)
    ActionChains(driver).move_to_element(campo).click().perform()
    try:
        campo.clear()  # funciona para input/textarea
    except Exception:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACK_SPACE).perform()

    campo.send_keys(resposta)


def responder_radio(pergunta, resposta):
    driver = st.session_state.driver
    wait = WebDriverWait(driver, 20)

    xpath = (
        f'//div[contains(@data-params, "{pergunta}")]'
        f'//div[@role="radio" and @data-value="{resposta}"]'
    )

    el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    el.click()
