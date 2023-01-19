from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re


def decode_announcement(dwelling_element: WebElement):
    dwelling = dict()
    dwelling["data_integrity"] = True
    if dwelling_element.get_attribute("class") == "box-anunt proiect standard":
        dwelling["data_integrity"] = False
        return dwelling

    dwelling["pret"] = dwelling_element.get_attribute("data-price")
    dwelling["judet"] = dwelling_element.get_attribute("data-judet")
    dwelling["zona"] = dwelling_element.get_attribute("data-zona")
    dwelling["NoCamere"] = dwelling_element.get_attribute("data-camere")
    dwelling["Suprafata"] = dwelling_element.get_attribute("data-surface")
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
    charact = temp.find_elements(By.CLASS_NAME, "caracteristica")
    for element in charact:
        split_element = element.get_attribute("innerHTML").split()
        if "etaj" in split_element[2]:
            if len(split_element) == 6:
                dwelling["Etaj"] = split_element[5][:split_element[5].find("</strong")]
            if len(split_element) == 5:
                dwelling["Etaj"] = split_element[4][split_element[4].find("strong>")+7:split_element[4].find("</strong")]
        elif "camere" in split_element[2]:
            dwelling["Partajare"] = split_element[3][split_element[3].find("<strong>") + 8:split_element[3].find("</strong>")]
        else:
            dwelling["error"] = True
    #apartment["banner"] = temp.get_attribute("innerHTML")
    return dwelling


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.imobiliare.ro/vanzare-apartamente/cluj/floresti")
    WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "box-anunt")))
    anunturi = driver.find_elements(By.CLASS_NAME, "box-anunt")
    for anunt in anunturi:
        apartment_dict = decode_announcement(anunt)
        if apartment_dict["data_integrity"]:
            print(apartment_dict["pret"], apartment_dict["TVA"])
    #for property_detail in apartment_dict:
    #    print(property_detail+":", apartment_dict[property_detail])
    driver.close()
