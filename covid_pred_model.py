import requests
import pandas as pd
import numpy as np
import csv
import os.path

from states import stateDict
from timeFrames import timeDict

rawdataFilepath = "./data/raw-us-states.csv"


class CovidPredictorModel:
    """ Class to handle the logic for the Covid-19 Predictor app """

    def __init__(self):
        self.state = ""
        self.predictionWindow = ""

    def setValues(self, state, predictionWindow):
        self.state = state
        self.predictionWindow = predictionWindow
        print(self.state, self.predictionWindow)

    def downloadData(self):
        """ Gets Covid data for US states from: https://github.com/nytimes/covid-19-data """

        data_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        r = requests.get(data_URL)

        f = open(rawdataFilepath, 'w')
        f.write(str(r.content, 'utf-8'))

        self.cleanData()

    def cleanData(self):
        """ Clean the raw US states Covid cases data: split each data into different states """

        # Split raw data by state
        with open(rawdataFilepath, 'r') as csvFile:
            csvReader = csv.reader(csvFile)
            firstline = next(csvReader)
            stateFilepaths = []

            for line in csvReader:
                stateFilepath = "./data/" + line[1] + ".csv"

                if stateFilepath in stateFilepaths:
                    with open(stateFilepath, 'a+', newline='') as appendFile:
                        # Open file in append mode to add following lines to file
                        csvWriter = csv.writer(appendFile)
                        csvWriter.writerow(line)
                else:
                    stateFilepaths.append(stateFilepath)
                    with open(stateFilepath, 'w') as writeFile:
                        # Open file write mode and add column names to file
                        csvWriter = csv.writer(writeFile)
                        csvWriter.writerow(firstline)

    def prepareData(self):
        pass
