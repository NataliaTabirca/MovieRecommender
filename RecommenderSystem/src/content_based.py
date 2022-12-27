
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from tabulate import tabulate

from dataset import metadata as md
from dataset import links, keywords, credits

import top_genres

links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')

# Pre-processing step
def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan


# Calculate a pairwise cosine similarity matrix for all the movies in our dataset.
md['id'] = md['id'].apply(convert_int)
md = md.drop([19730, 29503, 35587])
md['id'] = md['id'].astype('int')
smd = md[md['id'].isin(links)]
smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

# Get keywords and associate them with movies.
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
md['id'] = md['id'].astype('int')

md = md.merge(credits, on='id')
md = md.merge(keywords, on='id')
smd = md[md['id'].isin(links)]

# Add cast and crew data.
smd['cast'] = smd['cast'].apply(literal_eval)
smd['crew'] = smd['crew'].apply(literal_eval)
smd['keywords'] = smd['keywords'].apply(literal_eval)
smd['cast_size'] = smd['cast'].apply(lambda x: len(x))
smd['crew_size'] = smd['crew'].apply(lambda x: len(x))


def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


smd['director'] = smd['crew'].apply(get_director)
smd['cast'] = smd['cast'].apply(lambda x: [i['name']
                                for i in x] if isinstance(x, list) else [])
smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)
smd['keywords'] = smd['keywords'].apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

#  Process data to remove spaces and unwanted characters.
smd['cast'] = smd['cast'].apply(
    lambda x: [str.lower(i.replace(" ", "")) for i in x])
smd['director'] = smd['director'].astype('str').apply(
    lambda x: str.lower(x.replace(" ", "")))
smd['director'] = smd['director'].apply(lambda x: [x, x, x])

s = smd.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'
s = s.value_counts()
s[:5]
s = s[s > 1]


def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words


stemmer = SnowballStemmer('english')
smd['keywords'] = smd['keywords'].apply(filter_keywords)
smd['keywords'] = smd['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
smd['keywords'] = smd['keywords'].apply(
    lambda x: [str.lower(i.replace(" ", "")) for i in x])

smd['soup'] = smd['keywords'] + smd['cast'] + smd['director'] + smd['genres']
smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))

count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
count_matrix = count.fit_transform(smd['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)
smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])


# def get_recommendations(title):
#     idx = indices[title]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:31]
#     movie_indices = [i[0] for i in sim_scores]
#     return titles.iloc[movie_indices].head(10)


def get_recommendations(title, percentile=0.60):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    
    minVotes = vote_counts.quantile(percentile)
    topMovies = movies[(movies['vote_count'] >= minVotes) 
                & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]

    topMovies['vote_count'] = topMovies['vote_count'].astype('int')
    topMovies['vote_average'] = topMovies['vote_average'].astype('int')
    topMovies['wr'] = topMovies.apply(top_genres.weighted_rating, axis=1)
    topMovies = topMovies.sort_values('wr', ascending=False).head(10)

    return tabulate(topMovies.head(10), showindex=False, headers=topMovies.columns)
