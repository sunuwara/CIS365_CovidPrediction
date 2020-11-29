from covid_pred_model import CovidPredictorModel
from covid_pred_view import CovidPredictorView


from states import stateDict
from timeFrames import timeDict

if __name__ == "__main__":
    """ Runs the controller for the Covid-19 Predictor app """

    # Initialize Model and View
    model = CovidPredictorModel()
    view = CovidPredictorView()

    # Download raw data for latest Covid cases in US by state
    model.downloadData()

    # Get state and prediction window from view and send to model
    # TODO: Run view here and wait for user selections
    selectedState = stateDict['23']
    selectedTime = timeDict['1']
    model.setValues(selectedState, selectedTime)
