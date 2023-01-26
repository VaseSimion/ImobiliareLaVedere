import ScrapingUtilities as Su
import time
from concurrent.futures import ThreadPoolExecutor
import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from tqdm import tqdm


def run_it_all():
    try:
        complete_dataframe = pd.DataFrame()
        cities = ["alba?id=82496862", "arad?id=82494820", "arges?id=82494624", "bacau?id=82495016", "bihor?id=82494332",
                  "bistrita-nasaud?id=82501822", "botosani?id=82497568", "brasov?id=82494170", "braila?id=82495458",
                  "bucuresti-ilfov?id=82493726", "buzau?id=82495122", "caras-severin?id=82495494", "calarasi?id=82524120",
                  "cluj?id=82493680", "constanta?id=82493534", "covasna?id=82500712", "dambovita?id=82495344",
                  "dolj?id=82493886", "galati?id=82493530", "giurgiu?id=82495198", "gorj?id=82494826",
                  "harghita?id=82505524",
                  "hunedoara?id=82495282", "ialomita?id=82499146", "iasi?id=82493900", "maramures?id=82496128",
                  "mehedinti?id=82495778", "mures?id=82493622", "neamt?id=82502954", "olt?id=82500594",
                  "prahova?id=82494706",
                  "satu-mare?id=82498096", "salaj?id=82506196", "sibiu?id=82494094", "suceava?id=82495730",
                  "teleorman?id=82500592", "timis?id=82493432", "tulcea?id=82495302", "vaslui?id=82495238",
                  "valcea?id=82495108", "vrancea?id=82495300"]
        for city in tqdm(cities, desc="Running..."):
            base_url = "https://www.imobiliare.ro/vanzare-apartamente/" + city
            page_soup = BeautifulSoup(re.get(base_url).content, 'html.parser')
            anunturi = page_soup.find(class_="ultima butonpaginare double")
            if anunturi is None:
                pagina_max = 1
            else:
                attribute_dictionary = anunturi.attrs
                pagina_max = int(attribute_dictionary["data-pagina"])

            with ThreadPoolExecutor(max_workers=100) as p:
                start_time = time.time()
                results = p.map(Su.run_page_beautifulsoup, [city+"&"]*pagina_max, range(1, pagina_max+1))
                for result in results:
                    complete_dataframe = pd.concat([result, complete_dataframe], ignore_index=True)
                # print(f"{(time.time() - start_time):.2f} seconds")
            #
            # for i in range(1, 21):
            #     print("Run number:", i)
            #     start_time = time.time()
            #     result = Su.run_page_beautifulsoup(city, i)
            #     complete_dataframe = pd.concat([result, complete_dataframe], ignore_index=True)
            #     print(f"{(time.time() - start_time):.2f} seconds")
        complete_dataframe.to_csv("Reports/" + datetime.datetime.now().strftime("%m-%d-%Y") + ".csv", index=False)
    except:
        run_it_all()

if __name__ == "__main__":
    run_it_all()