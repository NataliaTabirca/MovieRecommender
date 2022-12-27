import pandas as pd
import numpy as np
from ast import literal_eval
from tabulate import tabulate

from dataset import metadata as md

md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
m = vote_counts.quantile(0.95)

md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(
    lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

topMovies = md[(md['vote_count'] >= m) &
               (md['vote_count'].notnull()) &
               (md['vote_average'].notnull())][['title',
                                                'year',
                                                'vote_count',
                                                'vote_average',
                                                'popularity',
                                                'genres']]

topMovies['vote_count'] = topMovies['vote_count'].astype('int')
topMovies['vote_average'] = topMovies['vote_average'].astype('int')


def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)


topMovies['wr'] = topMovies.apply(weighted_rating, axis=1)
topMovies = topMovies.sort_values('wr', ascending=False).head(250)

s = md.apply(lambda x: pd.Series(x['genres'], dtype='object'), axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genre'
gen_md = md.drop('genres', axis=1).join(s)
gen_md.head(3).transpose()


def get_genre_recommendation(genre, percentile=0.85):
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    
    avgVote = vote_averages.mean()              # average votes per genre
    minVotes = vote_counts.quantile(percentile) # minimum required no. of votes for a movie to be considered

    topMovies = df[(df['vote_count'] >= minVotes) & (df['vote_count'].notnull()) &
                   (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
    topMovies['vote_count'] = topMovies['vote_count'].astype('int')
    topMovies['vote_average'] = topMovies['vote_average'].astype('int')
    
    topMovies['wr'] = topMovies.apply(lambda x: (
        x['vote_count'] / (x['vote_count'] + minVotes) * x['vote_average']) + (minVotes / (minVotes + x['vote_count']) * avgVote), axis=1)
    
    topMovies = topMovies.sort_values('wr', ascending=False).head(250)

    return tabulate(topMovies.head(10), showindex=False, headers=topMovies.columns)
