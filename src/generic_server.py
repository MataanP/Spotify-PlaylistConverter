import dispatcher
from wsgiref.simple_server import make_server

def playlist_app(environ, start_response):
    dispatcher.setup()
    print (environ["PATH_INFO"])
    (status, body, headers)=dispatcher.handle_request(environ)
    start_response(status, headers)
    return [body.encode("UTF-8")]

if __name__ == "__main__":
    httpd = make_server('', 8000, playlist_app)
    print("Serving on port 8000...")
        # Serve until process is killed
    httpd.serve_forever()
