from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import ScrapingUtilities as Su
import pandas as pd


complete_dataframe = pd.DataFrame()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.imobiliare.ro/vanzare-apartamente/cluj")
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "box-anunt")))
listings = driver.find_elements(By.CLASS_NAME, "box-anunt")
for listing in listings:
    apartment_dict = Su.decode_announcement_imobiliare(listing)
    if apartment_dict["data_integrity"]:
        df_dictionary = pd.DataFrame([apartment_dict])
        complete_dataframe = pd.concat([complete_dataframe, df_dictionary], ignore_index=True)
driver.close()

print(complete_dataframe)
