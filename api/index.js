const express = require('express');
require('express-async-errors');

var amqp = require('amqplib/callback_api');

const {
  ExecuteQuery
} = require('./databaseConn/database');

let channel;

const app = express();

app.use(express.json());

const port = process.env.PORT ?? 3000;

app.listen(port, () => {
  console.log(`Movie Service at ${port}`);
});

app.get('/get-movie', async (req, res) => {
  console.log("INTRA IN GET")
  var values = await ExecuteQuery("SELECT * FROM movies LIMIT 10")

  console.log(values)
  res.status(200).json(values);
});

app.get('/get-by-id/:id', async (req, res) => {
  const id = parseInt(req.params.id)
  var values = await ExecuteQuery("SELECT * FROM movies WHERE id = $1",[id])

  console.log(values)
  res.status(200).json(values);
});

app.get('/get-best-rated', async (req, res) => {
  var values = await ExecuteQuery("SELECT * FROM movies ORDER BY rating DESC LIMIT 10")

  console.log(values)
  res.status(200).json(values);
});

app.post('/add-movie', async (req, res) => {

  console.log(req.body)

  const { title, genre, description, rating, release_date } = req.body;

  console.log(title, genre, description, rating, release_date);

  amqp.connect(process.env.AMQPURL, function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }

        var queue = 'MOVIES';

        channel.assertQueue(queue, {
            durable: false
        });

        console.log(" [*] Sending messages CTRL+C", queue);

        channel.sendToQueue(
          'MOVIES',
          Buffer.from(
            JSON.stringify({
              title,
              genre,
              description,
              rating,
              release_date
            })
          )
        );
    });
  });

  res.json("done");
});

app.get('/delete-movie/:id', async(req, res) => {
  const id = parseInt(req.params.id)

  var values = await ExecuteQuery("SELECT * FROM movies WHERE id = $1", [id])

  await ExecuteQuery("DELETE FROM movies WHERE id = $1", [id])

  console.log(`${values} was deleted`)
  res.status(200).json(values);
})
