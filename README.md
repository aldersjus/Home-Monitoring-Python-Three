# Home Monitorying Python Three

In the app file is a motion detecting application for a Raspberry Pi that stores movements in Google Firebase real time database.You need a push button, PIR sensor and an LCD to run this. It also needs a Google Firebase realtime database
that it can write to.

In the web_app file is the code to display data from Google Firebase that was uploaded by the app. The code in this
file is for a Python Flask web application. The html file that displays the information requires Bootstrap to be in
the static file of the web server.

Both these can be run on a Raspberry Pi if you have the necessary libraies installed. The web server needs some
data to return from Firebase, so it is best to run the app file code first.

This project was a continuation of two previous Python projects which were started due to various issues encountered with Android Things.

[Android Things Repository](https://github.com/aldersjus/Home-Monitoring-Android-Things)
[Python Part One](https://github.com/aldersjus/Home-Monitoring-Python)
[Python Part Two](https://github.com/aldersjus/Home-Monitoring-Python-Two)

