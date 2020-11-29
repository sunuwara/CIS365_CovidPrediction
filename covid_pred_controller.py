from covid_pred_model import CovidPredictorModel
from covid_pred_view import CovidPredictorView


if __name__ == "__main__":
    """ Runs the controller for the Covid-19 Predictor app """

    # Initialize Model and View
    model = CovidPredictorModel()
    view = CovidPredictorView()

    # Download raw data for latest Covid cases in US by state
    model.downloadData()
