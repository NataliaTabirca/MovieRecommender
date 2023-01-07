const express = require('express');
require('express-async-errors');

var amqp = require('amqplib/callback_api');
const movies = require("./models/movies")

let channel;

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
        /*
    How do I set up a consumer outside this function? 
         */
    });
});

const app = express();

app.use(express.json());

const port = process.env.PORT ?? 3000;

app.listen(port, () => {
  console.log(`Movie Service at ${port}`);
});

//add context for get
app.get('/get-movie', async (req, res) => {
  console.log("it works")
  const results = await movies.count();
  console.log(results)
  res.status(200).json(results);
});

app.get('/get-best-rated', async (req, res) => {
    const results = await Product.findAll();
  
    res.status(200).json(results);
  });

app.post('/add-movie', async (req, res) => {
  const { ids } = req.body;
  const products = await Product.findAll({
    where: {
      id: {
        [Sequelize.Op.in]: ids,
      },
    },
  });
  let order;

  channel.sendToQueue(
    'MOVIES',
    Buffer.from(
      JSON.stringify({
        products,
        userEmail: req.user.email,
      })
    )
  );
  await channel.consume('MOVIES', data => {
    order = JSON.parse(data.content);
  });
  res.json(order);
});

app.post('/delete-movie', async(req, res) => {

})
