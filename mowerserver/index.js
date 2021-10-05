const express = require("express")
const bodyParser = require("body-parser")
const SerialPort = require("serialport")

const app = express()
const port = 4444
const serialPort = new SerialPort("/dev/ttyACM1")

app.use(bodyParser.json())

let sendResponseOk = (req, res) => {
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Methods", "GET")
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
}

app.get("/api/drive", (req, res) => {
  req.query.break = parseInt(req.query.break) || 0
  req.query.left = parseInt(req.query.left) || 0
  req.query.right = parseInt(req.query.right) || 0
  req.query.up = parseInt(req.query.up) || 0
  req.query.down = parseInt(req.query.down) || 0


  if (!req.query.up && !req.query.down && !req.query.left && !req.query.right && !req.query.break) {
    // Dont move
    sendResponseOk(req, res)
    return
  }


  if (req.query.up && req.query.down) {
    // Dont move
    sendResponseOk(req, res)
    return
  }


  console.log(req.query.up.toString() + req.query.down.toString() + req.query.left.toString() + req.query.right.toString() + req.query.break.toString())


  if (req.query.down && req.query.left && req.query.right) {
    console.log("d1")
    // Move backwards
    serialPort.write("d", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (!req.query.down && !req.query.up && req.query.left && req.query.right) {
    console.log("u3")
    // Move backwards
    serialPort.write("u", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.up && req.query.left && req.query.right) {
    console.log("u1")
    // Move forewards
    serialPort.write("u", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.down && req.query.left) {
    console.log("x")
    // Turn left
    serialPort.write("x", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.down && req.query.right) {
    console.log("y")
    // Turn left
    serialPort.write("y", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.up && req.query.left || req.query.left) {
    console.log("l1")
    // Turn left
    serialPort.write("l", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.up && req.query.right || req.query.right) {
    console.log("r1")
    // Turn right
    serialPort.write("r", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.up) {
    console.log("u2")
    // Turn right
    serialPort.write("u", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

  if (req.query.down) {
    console.log("d2")
    // Turn right
    serialPort.write("d", function(err) {
      if (err) {
        return console.log("Error on write: ", err.message)
      }
    })
    sendResponseOk(req, res)
    return
  }

})

app.listen(port, () => {
    console.log(`Server listening on the port::${port}`)
})
