const express = require("express");
const kafka = require("kafka-node");
const yaml = require("js-yaml");
const bodyParser = require("body-parser");
const fs = require('fs');
const path = require("path");
const io = require("socket.io-client");

var yamlPath = path.join(__dirname, "..", "config.yaml");

const app = express();
app.use(express.static("public"));

var config = undefined;

try {
        config = (
            yaml.load(fs.readFileSync(yamlPath, 'utf8'))
        )["servers"]["web"];
        console.log(config);

    } catch (error) {
        console.log(error);
}

const server = app.listen(config["port"], () => {
    console.log(`Server running at http://${config["host"]}:${config["port"]}`);
});

const socketIO = require("socket.io")(server);


var Consumer = kafka.Consumer,
    client = new kafka.KafkaClient(),
    consumer = new Consumer(
        client,
        [
            { topic: "basket_sink" }
        ],
        {
            autoCommit: false
        }
);

// client.loadMetadataForTopics(["NonExistentTopic"], (err, resp) => {
//     console.log(JSON.stringify(resp))
// });

consumer.on("message", (message) => {
    // console.log(message.value);
    (socketIO, message) => socketIO.sockets.emit("update", message.value)();
});


socketIO.sockets.emit("test", {description: "data from the test event"});


var conCount = 1;
socketIO.on("connection", () => {
    console.log(`${conCount} connections`);
    conCount = conCount + 1;
});

app.get("/", (request, response) => {
    response.sendFile(__dirname+"/index.html");
});




