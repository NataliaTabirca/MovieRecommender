import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from tabulate import tabulate

from dataset import metadata as md
from dataset import links, keywords, credits,ratings

from content_based import smd, indices, cosine_sim

# surprise reader API to read the dataset
reader = Reader()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

svd = SVD()
trainset = data.build_full_trainset()
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5)

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

id_map = pd.read_csv('../dataset/links_small.csv')[['movieId', 'tmdbId']]
id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(smd[['title', 'id']], on='id').set_index('title')
indices_map = id_map.set_index('id')

def hybrid(userId, title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    movies = smd.iloc[movie_indices][['title', 'genres', 'vote_count', 'release_date', 'popularity', 'vote_average', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False)
    movies.drop(['vote_count', 'id', 'est'], axis=1, inplace=True)
    return tabulate(movies.head(10), showindex=False, headers=movies.columns)
