import requests
import pandas as pd
import numpy as np
import csv
import os.path

from states import stateDict
from timeFrames import timeDict

mainFilepath = "./data/raw-us-states.csv"


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

        dataURL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        r = requests.get(dataURL)

        f = open(mainFilepath, 'w')
        f.write(str(r.content, 'utf-8'))

        self.cleanData()

    def cleanData(self):
        """ Clean the raw US states Covid cases data: split each data into different states """

        with open(mainFilepath, 'r') as csvFile:
            csvReader = csv.reader(csvFile)
            firstLine = next(csvReader)

            for line in csvReader:
                newFilepath = "./data/" + line[1] + ".csv"

                if not os.path.exists(newFilepath):
                    with open(newFilepath, 'w') as newFile:
                        # Open file normal mode to add column names to file
                        csvWriter = csv.writer(newFile)
                        csvWriter.writerow(firstLine)

                with open(newFilepath, 'a+', newline='') as writeObj:
                    # Open file in append mode to add following lines to file
                    csvWriter = csv.writer(writeObj)
                    csvWriter.writerow(line)
