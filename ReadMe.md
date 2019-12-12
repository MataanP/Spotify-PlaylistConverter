Hello there!

To use this program, CD into the Downloaded directory.
From there you can run
    $python3 src/generic_server.py
Now in a web browser, direct to 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;localhost:8000/login

Make an account or sign in. After signing in you should then be prompted to oauth into your spotify account

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You can use my dummy account if you want

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;User = ThrowyAcc@gmail.com

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Password = jALcW3LiD6Ujw6snu3WRGQcRHCNkUL
    
Then you will have a chance to make a parallel playlist from any of your
current playlists
If you do this, your account will have a playlist added to it that contains similar
music as the original.
Then you can navigate to localhost:8000/home and get links to playlists that have been created by other users. (if running on local machine, this will be just your playlists, unless you let someone else log in)
From there you can look for playlists with parallel at the end of the name and look at what the webapp has created!



**Future Ideas**

Currently we have no support for TLS secure web connections (certificates). In the future I plan on switching from using wsgi as the http server to a more robust one that allows for certificates to be plugged in. If you still want to host this service, you can download a web server with TLS support and shunt all requests and responses between the current build running on your local machine. 
