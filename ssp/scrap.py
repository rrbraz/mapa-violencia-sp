import os
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

downloads_path = os.path.join(os.getcwd(), 'planilhas')


def rename_last_download(new_name):
    filename = max([os.path.join(downloads_path, f) for f in os.listdir(downloads_path)], key=os.path.getctime)
    shutil.move(filename, os.path.join(downloads_path, new_name))

options = Options()
options.headless = True

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", downloads_path)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

driver = webdriver.Firefox(options=options, firefox_profile=profile)
driver.get('https://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx')

select_anos = Select(driver.find_element_by_id('conteudo_ddlAnos'))

anos = []
for option in select_anos.options:
    ano = option.get_attribute('value')
    if ano != '0':
        anos.append(ano)

for ano in anos:
    print(ano)
    select_anos = Select(driver.find_element_by_id('conteudo_ddlAnos'))
    select_anos.select_by_value(ano)
    btn_excel = driver.find_element_by_id('conteudo_btnExcel')
    btn_excel.click()
    rename_last_download(f'{ano}.csv')
