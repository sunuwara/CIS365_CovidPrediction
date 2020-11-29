# CIS365_CovidPrediction

Covid-19 Prediction app for CIS 365: Artificial Intelligence. Raw data for US States prediction was retrieved from New York Times github page: https://github.com/nytimes/covid-19-data.

## Setup project environment:

1. Install poetry: `curl -SSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`
2. Download zip or clone: `git clone https://github.com/sunuwara/CIS365_CovidPrediction.git`
3. Navigate to project local repository from Terminal
4. Install project dependencies: `poetry install`

## How to run: `poetry run python covid_pred_controller.py`

## Development tips using Poetry:

- Poetry create new project: `poetry new project-name`
- Initializing pre-existing project: `cd project-name` then `poetry init`
- Adding dependencies: `poetry add dependency-name`
- Adding developer dependencies: `poetry add -dev dependency-name`
- Removing dependencies: `poetry remove dependency-name`
- Updating dependencies: `poetry update`
- Activating virtual environment: `poetry shell`
- Deactivating virtual environment and leaving shell: `poetry exit`
- Deactivating virtual environment without leaving shell: `poetry deactivate`
- Run program: `poetry run project-name`
