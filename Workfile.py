import ScrapingUtilities as Su
import time
from concurrent.futures import ThreadPoolExecutor
import requests as re
from bs4 import BeautifulSoup
import pandas as pd


complete_dataframe = pd.DataFrame()

base_url = "https://www.imobiliare.ro/vanzare-apartamente/cluj-napoca"
page_soup = BeautifulSoup(re.get(base_url).content, 'html.parser')
anunturi = page_soup.find(class_="ultima butonpaginare double")
attribute_dictionary = anunturi.attrs
pagina_max = int(attribute_dictionary["data-pagina"])

with ThreadPoolExecutor(max_workers=100) as p:
    start_time = time.time()
    results = p.map(Su.run_page_beautifulsoup, range(1, pagina_max+1))
    for result in results:
        complete_dataframe = pd.concat([result, complete_dataframe], ignore_index=True)
    print(f"{(time.time() - start_time):.2f} seconds")

# for i in range(1, 21):
#     print("Run number:", i)
#     start_time = time.time()
#     result = Su.run_page_beautifulsoup(i)
#     complete_dataframe = pd.concat([result, complete_dataframe], ignore_index=True)
#     print(f"{(time.time() - start_time):.2f} seconds")

complete_dataframe.to_csv('20Jan.csv')