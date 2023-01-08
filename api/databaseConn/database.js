const { Pool } = require('pg')

const options = {
  host: process.env.POSTGRES_HOST,
  database: process.env.POSTGRES_DB,
  port: process.env.POSTGRES_PORT,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD
}

const pool = new Pool(options);

pool.on('error', (err, client) => {
    console.error('Unexpected error on idle client', err)
    process.exit(-1)
  });

const ExecuteQuery = async (text, params) => {
    const {
      rows,
    } = await pool.query(text, params);
    return rows;
};

module.exports = {
    ExecuteQuery
}