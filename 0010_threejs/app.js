const express = require('express')
const app = express();
const server = require('http').createServer(app);

app.use(express.static('js'));
app.use(express.static('models'));

server.listen(3000, function() {
  console.log('Server in ascolto sulla porta 3000 ...');
});

app.get('/', function(req, res) {
  res.sendFile(__dirname+'/index.html');
});
