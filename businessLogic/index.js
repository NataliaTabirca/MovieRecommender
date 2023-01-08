require('dotenv').config()

const {
    ExecuteQuery
} = require('./database/database');

var amqp = require('amqplib/callback_api');

amqp.connect(process.env.AMQPURL, (error0, connection) => {
    if (error0) {
        throw error0;
    }
    connection.createChannel((error1, channel) => {
        if (error1) {
            throw error1;
        }

        var queue = 'MOVIES';

        channel.assertQueue(queue, {
            durable: false
        });

        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

        channel.consume(queue, async (msg) => {
            console.log(" [x] Received %s", msg.content.toString());

            if(msg !== null) {
                const jsonPayload = JSON.parse(msg.content);
                try {
                    await ExecuteQuery("insert into movies (id, title, genre, description, rating, release_date) values (1005, $1, $2, $3, $4, $5)", 
                    [jsonPayload.title, jsonPayload.genre, jsonPayload.description, jsonPayload.rating, jsonPayload.release_date]);
                } catch (err) {
                    console.error(err);
                }
            }
        }, {
            noAck: true
        });
    });
});