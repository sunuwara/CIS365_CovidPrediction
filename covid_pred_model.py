import requests
import pandas as pd
import numpy as np

mainFile = "./data/raw-us-states.csv"


class CovidPredictorModel:
    """ Class to handle the logic for the Covid-19 Predictor app """

    def __init__(self):
        """ Initialization """
        pass

    def downloadData(self):
        """ Gets Covid data for US states from: https://github.com/nytimes/covid-19-data """
        r = requests.get(
            'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
        f = open(mainFile, 'w')
        f.write(str(r.content, 'utf-8'))

    def cleanData(self):
        """ Clean the raw US states Covid cases data """
