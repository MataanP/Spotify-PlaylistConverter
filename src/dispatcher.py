import urllib.parse
import account
import convert
from config import CONFIG
import common as c
from jinja2 import Environment, PackageLoader, select_autoescape,FileSystemLoader

url = "spotify.mataan.me"

def handle_request(environ):
    if environ["HTTP_HOST"] != url:
        return ("404 File Not Found","",[])
    try:
        body= server_file_return(environ ["PATH_INFO"])
        return ("200 OK",body,c.header_creator(["html_content_header"]))
    except FileNotFoundError:
        if environ["PATH_INFO"] == "/login" or environ["PATH_INFO"] == "/":
            return ("200 OK", redirect("login.html"),c.header_creator(["html_content_header"]))
        if environ["PATH_INFO"] == "/account":
            return handle_account(environ)
        if environ["PATH_INFO"] == "/authenticate":
            return handle_authentication(environ)
        if environ["PATH_INFO"] == "/callback":
            return ("200 OK",server_file_return("/callback.html"),[])
        if environ["PATH_INFO"] == "/convert":
            return handle_conversion(environ)
        if environ["PATH_INFO"] == "/home":
            return handle_home()
        else:
            return ("404 File Not Found","",[])

def handle_home():
    template = CONFIG["environment"].get_template("home.html")
    list = CONFIG["converter"].get_all()
    print(list)
    return ("200 OK",template.render(playlists = list), c.header_creator(["html_content_header"]))

def handle_conversion(environ):
    try:
        cookie = get_cookie(environ)
    except KeyError:
        return ("200 OK", server_file_return("/badCookie.html"),\
            c.header_creator(["html_content_header"]))
    query = urllib.parse.parse_qs(environ["QUERY_STRING"])
    CONFIG["converter"].convert(cookie, query)
    return ("200 OK","",[])


def handle_authentication(environ):
    if environ ["REQUEST_METHOD"] == "POST":
        cookie = get_cookie(environ)
        body = get_body(environ)
        token = body["token"][0].split("=")[1].split("&")[0]#dumb parsing needed cause of how spotify deals with these things
        CONFIG["account"].add_spotifyID(cookie,token)
        return ("200 OK", redirect("account"), c.header_creator(["html_content_header"]))
    if environ["REQUEST_METHOD"] == "GET":
        return ("200 OK",server_file_return("/authenticate.html"), c.header_creator(["html_content_header"]))
    return ("200 OK","",[])

def get_body(environ):
    body= ''
    try:
        length= int(environ.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length = 0
    if length!=0:
        body= urllib.parse.parse_qs(environ['wsgi.input'].read(length).decode())
    return body

def handle_account(environ):
    body= get_body(environ)
    method = environ["REQUEST_METHOD"]
    account_manager = CONFIG["account"]


    #get the homepage for this account
    if method == "GET":
        try:
            cookie = get_cookie(environ)
            (links,names,ids,pictures) = account_manager.handle_R(cookie)
            return ("200 OK",render_account("account.html",links,names,ids,pictures),c.header_creator(\
                    ["html_content_header"]))
        except (account.BadAccountIdentifiersError, KeyError):
            return ("200 OK",server_file_return("/badCookie.html")\
                    ,c.header_creator(["html_content_header"]))
        except account.NotEnoughAuthentication:
            return ("200 OK",redirect("authenticate"),\
                    c.header_creator(["html_content_header"]))
        except account.SpotifyTokenExpired:
            account_manager.handle_D_token(cookie)
            return ("200 OK",redirect("login"),c.header_creator(["html_content_header"]))

    #sign in and sign up
    if method == "POST":
        try:
            #try successful creation or retrieval
            handle = account_manager.handle_CU(body)
            return ("200 OK",redirect("account"),c.header_creator(["cookie_header"\
                    ,"html_content_header"],cookie = handle))
        except account.BadSignInError:
            return ("200 OK",server_file_return("/badSignIn.html")\
                    ,c.header_creator(["html_content_header"]))
        except account.BadAccountIdentifiersError:
            return("200 OK", server_file_return("/usernameOrPasswordAlreadyUsed.html")\
                    ,c.header_creator(["html_content_header"]))
        except account.NotEnoughInfoError:
            return ("200 OK", server_file_return("/notEnoughInfo.html"),\
                    c.header_creator(["html_content_header"]))
    else:
        return ("405 wrong method","",[])

def get_cookie(environ):
    try:
        return environ["HTTP_COOKIE"].split("=")[1]
    except KeyError:
        raise KeyError

def render_account(filename, links,names,ids,pictures):
    template = CONFIG["environment"].get_template(filename)
    return template.render(playlists = zip(links,names,ids,pictures))

def server_file_return(filename):
    #this only works if run from SeverCode directory
    try:
        file = open("./WebPages"+filename,"r")
        return file.read()
    except FileNotFoundError:
        raise FileNotFoundError

def redirect(new_url):
    return "<meta http-equiv=\"refresh\" content=\"0; URL=/"+new_url+"\" />"

def setup():
    if CONFIG["converter"] == None:
        CONFIG["converter"] = convert.Converter()

    if CONFIG["account"] == None:
        CONFIG["account"] = account.Account()

    if CONFIG["environment"] == None:
        CONFIG["environment"] = Environment(loader=FileSystemLoader(\
                                searchpath="./WebPages"))
