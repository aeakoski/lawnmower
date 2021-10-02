const express = require('express');
const bodyParser = require("body-parser");
const SerialPort = require('serialport')

const app = express()
const port = 4444;
const serialPort = new SerialPort('/dev/ttyACM0')

app.use(bodyParser.json())

app.get('/api/drive', (req, res) => {
  req.query.break = parseInt(req.query.break) || 0
  req.query.left = parseInt(req.query.left) || 0
  req.query.right = parseInt(req.query.right) || 0
  req.query.up = parseInt(req.query.up) || 0
  req.query.down = parseInt(req.query.down) || 0

  if (req.query.up || (req.query.left && req.query.right)) {
    serialPort.write('u', function(err) {
      if (err) {
        return console.log('Error on write: ', err.message)
      }
    })
  }

  res.header("Access-Control-Allow-Origin", "*")
  res.header('Access-Control-Allow-Methods', 'GET')
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Cache-Control")
  res.status(200)
  res.json({
    status:"ok",
    up: req.query.up,
    down: req.query.down,
    left: req.query.left,
    right: req.query.right,
    break: req.query.break,
  })
})

app.listen(port, () => {
    console.log(`Server listening on the port::${port}`)
});
