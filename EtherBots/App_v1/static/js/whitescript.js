a = document.getElementsByClassName ('s003');
a[0].classList.add("white");
a[0].classList.remove("s003");

a = document.getElementsByClassName('navbar');
a[0].remove();


a = document.getElementsByClassName('inner-form');
var heading1 = document.createElement("h1");
heading1.innerText = 'No Requested Pincode Found';
a[0].innerHTML = '<h1> No Requested Pincode Found </h1> <a href="/"><button id="backButton">Back</button></a>';