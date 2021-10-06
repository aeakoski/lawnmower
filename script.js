const delayInMsBetweenRequests = 100
const requestOptions = {
  method: "GET",
  redirect: "follow"
}
const initialTime = new Date()
var lastEvent = initialTime.getTime()

var keyMap = {}

document.onkeydown = document.onkeyup = function(e){
    e = e || event // to deal with IE
    // Filter for our controller buttons being pressed
    if(e.type === "keydown"){
      switch(e.keyCode){
        case 37:
        document.getElementById("l").style.backgroundColor = "blue"
        break
        case 38:
          document.getElementById("u").style.backgroundColor = "blue"
        break
        case 39:
          document.getElementById("r").style.backgroundColor = "blue"
        break
        case 40:
          document.getElementById("d").style.backgroundColor = "blue"
        break
        case 66:
          document.getElementById("b").style.backgroundColor = "blue"
        break
      }
    }
    if(e.type === "keyup"){
      switch(e.keyCode){
        case 37:
        document.getElementById("l").style.backgroundColor = "white"
        break
        case 38:
          document.getElementById("u").style.backgroundColor = "white"
        break
        case 39:
          document.getElementById("r").style.backgroundColor = "white"
        break
        case 40:
          document.getElementById("d").style.backgroundColor = "white"
        break
        case 66:
        document.getElementById("b").style.backgroundColor = "white"
        break
      }
    }
    if (![37,38,39,40,66].includes(e.keyCode)){
      return
    }
    // Check time since last update so we dont spam requests, let through new presses
    const clickedTime = new Date()
    if (clickedTime.getTime() - lastEvent < delayInMsBetweenRequests) {
      if (keyMap[e.keyCode] === (e.type === "keydown")) {
        return
      }
    }
    lastEvent = clickedTime.getTime()

    keyMap[e.keyCode] = e.type === "keydown"

    pressedKeyCodes = Object.keys(keyMap).filter(keyCode => keyMap[keyCode])
    var up = `up=${+ pressedKeyCodes.includes("38")}`
    var down = `down=${+ pressedKeyCodes.includes("40")}`
    var left = `left=${+ pressedKeyCodes.includes("37")}`
    var right = `right=${+ pressedKeyCodes.includes("39")}`
    var _break = `break=${+ pressedKeyCodes.includes("66")}`

    var driveString = `${up}&${down}&${left}&${right}&${_break}`
    fetch(`http://localhost:4444/api/drive?${driveString}`, requestOptions)
      .then(response => response.text())
      .catch(error => console.log("error", error))
}
