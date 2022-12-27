import warnings; warnings.simplefilter('ignore')

import pandas as pd

credits = pd.read_csv("../dataset/credits.csv")
keywords = pd.read_csv('../dataset/keywords.csv')
links = pd.read_csv('../dataset/links_small.csv')
metadata = pd.read_csv('../dataset/movies_metadata.csv')
ratings = pd.read_csv('../dataset/ratings_small.csv')


