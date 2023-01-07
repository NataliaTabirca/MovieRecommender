// Create DB and collection
db = new Mongo().getDB("MovieRecommender");

db.createCollection("Movies", { capped: false });