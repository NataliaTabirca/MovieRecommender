FROM mongo:5.0
 # Will be set through Environment Files
 ARG DATABASE_URI
 ARG USERNAME
 ARG PASSWORD

 ENV DATABASE_URI ${DATABASE_URI}
 ENV USERNAME ${USERNAME}
 ENV PASSWORD ${PASSWORD}

 COPY movies_metadata.csv /movies_metadata.csv

 CMD mongoimport --username ${USERNAME} --password ${PASSWORD} --uri ${DATABASE_URI} --collection Movies --drop --file /movies_metadata.csv
