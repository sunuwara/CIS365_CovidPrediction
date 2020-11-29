
from covid_pred_model import CovidPredictorModel
from covid_pred_view import CovidPredictorView


if __name__ == "__main__":
    print("hello, world")

    # Initialize Model and View
    model = CovidPredictorModel
    view = CovidPredictorView

    # Download raw data for latest Covid cases in US by state
    model.downloadData()
