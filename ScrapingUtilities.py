from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests as re
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import time


def decode_announcement_imobiliare_selenium(dwelling_element: WebElement):  # Not updated
    dwelling = dict()
    dwelling["data_integrity"] = True
    if dwelling_element.get_attribute("class") == "box-anunt proiect standard":
        dwelling["data_integrity"] = False
        return dwelling

    dwelling["pret"] = dwelling_element.get_attribute("data-price")
    dwelling["judet"] = dwelling_element.get_attribute("data-judet")
    dwelling["zona"] = dwelling_element.get_attribute("data-zona")
    dwelling["NoCamere"] = dwelling_element.get_attribute("data-camere")
    dwelling["Type"] = dwelling_element.get_attribute("data-name")
    dwelling["InternalID"] = dwelling_element.get_attribute("id")

    temp = WebDriverWait(dwelling_element, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "titlu-anunt")))
    dwelling["anunt"] = temp.get_attribute("innerHTML").split("<")[1][5:]

    temp = WebDriverWait(dwelling_element, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "location_txt")))
    locatie = (" ".join(temp.get_attribute("innerHTML").split("<")[1][6:].split()))

    temp = WebDriverWait(dwelling_element, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "comision")))
    if len(temp.get_attribute("innerHTML").split("\n")) == 3:
        dwelling["comision"] = " ".join(temp.get_attribute("innerHTML").split("\n")[2].split())
    else:
        dwelling["comision"] = "Not mentioned"

    temp = WebDriverWait(dwelling_element, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "tva-luna")))
    if temp.get_attribute("innerHTML") == "€":
        dwelling["TVA"] = "No"
    else:
        dwelling["TVA"] = "Yes"

    if "," in locatie:
        dwelling["oras"] = locatie.split(",")[0]
        dwelling["zona"] = locatie.split(",")[1]
    else:
        dwelling["oras"] = locatie
        dwelling["zona"] = "Nan"

    temp = WebDriverWait(dwelling_element, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "swiper-wrapper")))
    characteristics = temp.find_elements(By.CLASS_NAME, "caracteristica")
    for element in characteristics:
        split_element = element.get_attribute("innerHTML").split()
        if "etaj" in split_element[2]:
            if len(split_element) == 6:
                dwelling["Etaj"] = split_element[5][:split_element[5].find("</strong")]
            if len(split_element) == 5:
                dwelling["Etaj"] = split_element[4][split_element[4].find("strong>") +
                                                    7:split_element[4].find("</strong")]
        elif "camere" in split_element[2]:
            dwelling["Partajare"] = split_element[3][split_element[3].find("<strong>")
                                                     + 8:split_element[3].find("</strong>")]
        elif "suprafata" in split_element[2]:
            if len(split_element) == 6:
                dwelling["Suprafata"] = split_element[4][split_element[4].find("<strong>")+8:split_element[4].find("</strong")]
            if len(split_element) == 5:
                dwelling["data_integrity"] = False
    return dwelling


def decode_announcement_imobiliare_beautiful(dwelling_element: bs4.element.Tag):
    dwelling = dict()
    element_attribute_dictionary = dwelling_element.attrs

    if len(element_attribute_dictionary["class"]) != 1:
        dwelling["data_integrity"] = False
        return dwelling

    if "data-price" in element_attribute_dictionary.keys():
        dwelling["pret"] = element_attribute_dictionary["data-price"]
    else:
        dwelling["data_integrity"] = False
        return dwelling

    caracteristici = dwelling_element.find(class_="swiper-wrapper").find_all(class_="caracteristica")
    if len(caracteristici) < 3:
        dwelling["data_integrity"] = False
        return dwelling

    if "mp" in " ".join(caracteristici[1].find('span').text.split()):
        dwelling["suprafata"] = " ".join(caracteristici[1].find('span').text.split()).split()[0]
    else:
        dwelling["data_integrity"] = False
        return dwelling

    dwelling["etaj"] = " ".join(caracteristici[2].find('span').text.split())
    if len(caracteristici) > 3:
        dwelling["partajare"] = " ".join(caracteristici[3].find('span').text.split())
    else:
        dwelling["partajare"] = "Not specified"
    dwelling["noCamere"] = element_attribute_dictionary["data-camere"]
    dwelling["type"] = element_attribute_dictionary["data-name"]

    dwelling["judet"] = element_attribute_dictionary["data-judet"]
    locatie = " ".join(dwelling_element.find(class_="location_txt").text.split("\n")[2].split())
    if "," in locatie:
        dwelling["oras"] = locatie.split(",")[0].replace("ş", "s").replace("ă", "a").replace("Î", "I").replace("â", "a").replace("ţ", "t")
        dwelling["zona"] = locatie.split(",")[1].replace("ş", "s").replace("ă", "a").replace("Î", "I").replace("â", "a").replace("ţ", "t")
    else:
        dwelling["oras"] = locatie.replace("ş", "s").replace("ă", "a").replace("Î", "I").replace("â", "a").replace("ţ", "t")
        dwelling["zona"] = "Nan"

    if len(dwelling_element.find(class_="comision").text.split("\n")) == 3:
        dwelling["comision"] = " ".join(dwelling_element.find(class_="comision").text.split("\n")[2].split())
    else:
        dwelling["comision"] = "Standard"

    if "TVA" in dwelling_element.find(class_="tva-luna").text:
        dwelling["tva"] = "Yes"
    else:
        dwelling["tva"] = "No"

    dwelling["anunt"] = dwelling_element.find(class_="titlu-anunt").text.split("\n")[1]
    dwelling["internalID"] = element_attribute_dictionary["id"]
    dwelling["data_integrity"] = True

    dwelling["pert_pe_mp"] = int(1000*float(dwelling["pret"])/float(dwelling["suprafata"]))

    return dwelling


def run_page_selenium(page_no):
    local_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    local_dataframe = pd.DataFrame()
    local_driver.get("https://www.imobiliare.ro/vanzare-apartamente/cluj-napoca?pagina={}".format(page_no))
    WebDriverWait(local_driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "box-anunt")))
    listings = local_driver.find_elements(By.CLASS_NAME, "box-anunt")
    for listing in listings:
        apartment_dict = decode_announcement_imobiliare_selenium(listing)
        # print(apartment_dict)
        if apartment_dict["data_integrity"]:
            df_dictionary = pd.DataFrame([apartment_dict])
            local_dataframe = pd.concat([local_dataframe, df_dictionary], ignore_index=True)
    local_driver.close()
    return local_dataframe


def run_page_beautifulsoup(city, page_no):
    local_dataframe = pd.DataFrame()
    url = "https://www.imobiliare.ro/vanzare-apartamente/{}pagina={}".format(city, page_no)
    page_html = re.get(url)
    page_souped = BeautifulSoup(page_html.content, 'html.parser')
    listings = page_souped.find_all(class_="box-anunt")
    for listing in listings:
        apartment_dict = decode_announcement_imobiliare_beautiful(listing)
        if apartment_dict["data_integrity"]:
            df_dictionary = pd.DataFrame([apartment_dict])
            local_dataframe = pd.concat([local_dataframe, df_dictionary], ignore_index=True)
    time.sleep(.5)
    return local_dataframe


if __name__ == "__main__":
    base_url = "https://www.imobiliare.ro/vanzare-apartamente/cluj-napoca"
    page = re.get(base_url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    anunturi = page_soup.find(class_="ultima butonpaginare double")
    attribute_dictionary = anunturi.attrs
    print(attribute_dictionary["data-pagina"])


#  print(anunturi[0].find(class_="tva-luna").text.split("\n"))

    # for anunt in anunturi:
    #     result =decode_announcement_imobiliare_beautiful(anunt)
    #     if result["data_integrity"]:
    #         print(result["pret"])

    # result = decode_announcement_imobiliare_beautiful(anunturi[0])
    # for element in result:
    #     print(element+":", result[element])
