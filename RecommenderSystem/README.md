# RecommenderSystem
This component contains the Recommendation API used for the app.

## How to build and run app:
1. Download *The Movies Dataset* dataset hosted on Kaggle: [Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) and add the files in a folder named *dataset*.
or run:

> ./scripts/download_dataset.sh

2. Build and run app.

- To create a virtual environment and install all requirements use:

    > python3 -m venv ./venv
	> pip install -r requirements.txt

This step applies only the first time the project is created.

- To activate the virtual environment use:

    > source ./venv/bin/activate

This step applies before running the program.

- To run the app use:
    > make

