import dispatcher
from wsgiref.simple_server import make_server

def playlist_app(environ, start_response):
    dispatcher.setup()
    print (environ["PATH_INFO"])
    (status, body, headers)=dispatcher.handle_request(environ)
    start_response(status, headers)
    return [body.encode("UTF-8")]

if __name__ == "__main__":
    httpd = make_server('', 80, playlist_app)
    print("Serving on port 80...")
        # Serve until process is killed
    httpd.serve_forever()



{'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:',
 'SSH_CONNECTION': '192.70.253.17 9807 157.245.177.58 22',
 'LESSCLOSE': '/usr/bin/lesspipe %s %s',
 'LANG': 'C.UTF-8',
 'XDG_SESSION_ID': '188',
 'USER': 'root',
 'PWD': '/root/Spotify-PlaylistConverter',
 'HOME': '/root',
 'LC_TERMINAL': 'iTerm2',
 'SSH_CLIENT': '192.70.253.17 9807 22',
 'LC_TERMINAL_VERSION': '3.3.2',
 'XDG_DATA_DIRS': '/usr/local/share:/usr/share:/var/lib/snapd/desktop',
 'SSH_TTY': '/dev/pts/0',
 'MAIL': '/var/mail/root',
 'TERM': 'xterm-256color',
 'SHELL': '/bin/bash',
 'SHLVL': '1',
 'LOGNAME': 'root',
 'XDG_RUNTIME_DIR': '/run/user/0',
 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin',
 'LESSOPEN': '| /usr/bin/lesspipe %s',
 '_': '/usr/bin/python3',
 'OLDPWD': '/root/Spotify-PlaylistConverter/src',
 'SERVER_NAME': 'PlaylistConverter',
 'GATEWAY_INTERFACE': 'CGI/1.1',
 'SERVER_PORT': '80',
 'REMOTE_HOST': '',
 'CONTENT_LENGTH': '',
 'SCRIPT_NAME': '',
 'SERVER_PROTOCOL': 'HTTP/1.1',
 'SERVER_SOFTWARE': 'WSGIServer/0.2',
 'REQUEST_METHOD': 'GET',
 'PATH_INFO': '/login.css',
 'QUERY_STRING': '',
 'REMOTE_ADDR': '192.70.253.22',
 'CONTENT_TYPE': 'text/plain',
 'HTTP_HOST': 'mataan.me',
 'HTTP_CONNECTION': 'keep-alive',
 'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
 like Gecko) Chrome/76.0.3809.132 Safari/537.36',
 'HTTP_ACCEPT': 'text/css,
*/*;q=0.1',
 'HTTP_REFERER': 'http://mataan.me/login.html',
 'HTTP_ACCEPT_ENCODING': 'gzip,
 deflate',
 'HTTP_ACCEPT_LANGUAGE': 'en-US,
en;q=0.9',
 'wsgi.input': <_io.BufferedReader name=4>,
 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>,
 'wsgi.version': (1,
 0),
 'wsgi.run_once': False,
 'wsgi.url_scheme': 'http',
 'wsgi.multithread': True,
 'wsgi.multiprocess': False,
 'wsgi.file_wrapper': <class 'wsgiref.util.FileWrapper'>}
