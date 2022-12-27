# RecommenderSystem
This component contains the Recommendation API used for the app.

## How to build and run app:
1. Download *The Movies Dataset* dataset hosted on Kaggle: [Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) and add the files in a folder named *dataset*.

The folder strucure should be like this:

.
├── dataset
│   ├── credits.csv        
│   ├── keywords.csv       
│   ├── links.csv
│   ├── links_small.csv    
│   ├── movies_metadata.csv
│   ├── ratings.csv        
│   └── ratings_small.csv      
├── src
│   ├── ...

2. Build and run app.

- To create a virtual environment and install all requirements use:

    > make venv_create

This step applies only the first time the project is created.

- To activate the virtual environment use:

    > make venv_activate

This step applies before running the program.

- To run the app use:
    > make

or

    > make run