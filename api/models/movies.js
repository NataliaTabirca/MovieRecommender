const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const MovieSchema = new Schema({
    adult: Boolean,
    belongs_to_collection: String,
    budget: String,
    genres: String,
    homepage: String,
    id: String,
    imdb_id: String,
    original_language: String,
    original_title: String,
    overview: String,
    popularity: String,
    poster_path: String,
    production_companies: String,
    production_countries: String,
    release_date: Date,
    revenue: Number,
    runtime: Number,
    spoken_languages:String,
    status: String,
    tagline: String,
    title: String,
    video: Boolean,
    vote_average: Number,
    vote_count: Number
});

module.exports = mongoose.model("movie", MovieSchema, "movies");
