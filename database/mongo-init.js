// Create DB and collection
db = new Mongo().getDB("MovieRecomnender");

db.createCollection("Movies", { capped: false });