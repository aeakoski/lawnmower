const delayInMsBetweenRequests = 100
const requestOptions = {
  method: 'GET',
  redirect: 'follow'
}
const initialTime = new Date()
var lastEvent = initialTime.getTime()

document.onkeydown = function(event) {
  const clickedTime = new Date()
  if (clickedTime.getTime() - lastEvent < delayInMsBetweenRequests) {
    return
  }
  lastEvent = clickedTime.getTime()

  switch (event.keyCode) {
    case 37: // Left
      console.log("Left key is pressed.");
      break;
    case 38: // Up
      fetch("http://localhost:4444/api/drive?up=1", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
      break;
    case 39: // Right
      console.log("Right key is pressed.");
      break;
    case 40: // Down
      console.log("Down key is pressed.");
      break;
    case 66: // B
      console.log("Brake key is pressed.");
      break;
  }
}
