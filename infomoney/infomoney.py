from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_maiores_altas():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar em modo headless
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navegar até a página
        url = "https://www.infomoney.com.br/ferramentas/altas-e-baixas/"
        driver.get(url)
        time.sleep(5)  # Aguarde o carregamento da página

        # Esperar até que a tabela esteja presente
        wait = WebDriverWait(driver, 20)
        table = wait.until(EC.presence_of_element_located((By.ID, 'altas_e_baixas')))

        # Selecionar todas as linhas da tabela dentro do tbody
        rows = table.find_elements(By.XPATH, ".//tbody/tr")

        # Listas para armazenar resultados
        symbols = []
        variations = []

        # Iterar pelas linhas e extrair dados
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 3:
                symbol = cols[0].text.strip()
                variation = cols[2].text.strip().replace('%', '').replace(',', '.')

                # Filtrar ações com alta superior a 3%
                if float(variation) > 3:
                    symbols.append(symbol)
                    variations.append(f"{variation}%")

        # Converter os resultados em DataFrame
        df = pd.DataFrame({'Ação': symbols, 'Variação (%)': variations})
        return df

    finally:
        driver.quit()

# Execução do script
df_resultado = get_maiores_altas()
if not df_resultado.empty:
    print(df_resultado)
else:
    print("Nenhuma ação com alta superior a 3% encontrada.")