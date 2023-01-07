FROM mongo:latest
COPY movies_metadata.csv /movies_metadata.csv
CMD ["mongoimport", "--host", "mongodb", "--db", "MovieRecommender", "--collection", "Movies", "--type", "csv", "--headerline", "--file", "/movies_metadata.csv"]