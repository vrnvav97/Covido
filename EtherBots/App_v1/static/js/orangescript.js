a = document.getElementsByClassName ('s003');
a[0].classList.add("orange");
a[0].classList.remove("s003");

a = document.getElementsByClassName ("inner-form");
var heading1 = document.createElement("h1");
heading1.innerText = 'Beaware';
a[0].prepend(heading1);

a = document.getElementsByTagName ('h1')
for (i of a)
	i.style.color = 'orangered';