import os
import pandas as pd
import numpy as np


def return_mean_price_history(oras, no_camere):
    list_of_prices = []
    for file in os.listdir("./Reports/"):
        data = pd.read_csv("Reports/" + file)
        cluj = data[(data["oras"] == oras) & (data["noCamere"] == no_camere)]
        cluj = cluj[["pret", "suprafata", "etaj", "partajare", "zona", "pret_pe_mp", "noCamere"]]
        Q1 = np.percentile(cluj['pret'], 25, method='midpoint')
        Q3 = np.percentile(cluj['pret'], 75, method='midpoint')
        IQR = Q3 - Q1
        cluj.drop(cluj[(cluj.pret < Q1 - 1.5 * IQR) | (cluj.pret > Q3 + 1.5 * IQR)].index, inplace=True)
        list_of_prices.append(cluj.pret.mean())
    return list_of_prices


def return_mean_price_mp_history(oras, no_camere):
    list_of_prices = []
    for file in os.listdir("./Reports/"):
        data = pd.read_csv("Reports/" + file)
        cluj = data[(data["oras"] == oras) & (data["noCamere"] == no_camere)]
        cluj = cluj[["pret", "suprafata", "etaj", "partajare", "zona", "pret_pe_mp", "noCamere"]]
        Q1 = np.percentile(cluj['pret_pe_mp'], 25, method='midpoint')
        Q3 = np.percentile(cluj['pret_pe_mp'], 75, method='midpoint')
        IQR = Q3 - Q1
        cluj.drop(cluj[(cluj.pret_pe_mp < Q1 - 1.5 * IQR) | (cluj.pret_pe_mp > Q3 + 1.5 * IQR)].index, inplace=True)
        list_of_prices.append(cluj.pret_pe_mp.mean())
    return list_of_prices