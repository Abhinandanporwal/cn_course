import http.server
import socketserver
import os
import hashlib
from email.utils import formatdate, parsedate_to_datetime

PORT = 8088
FILE_PATH = "index.html"

class CachingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/":
            return super().do_GET()

        if not os.path.exists(FILE_PATH):
            self.send_error(404, "File not found")
            return

        with open(FILE_PATH, "rb") as f:
            content = f.read()

        # Generate ETag
        etag = hashlib.md5(content).hexdigest()

        # Last-Modified
        last_modified = formatdate(os.path.getmtime(FILE_PATH), usegmt=True)

        # Client headers
        client_etag = self.headers.get("If-None-Match")
        client_modified = self.headers.get("If-Modified-Since")

        if client_etag == etag or (
            client_modified and parsedate_to_datetime(client_modified).timestamp()
            >= os.path.getmtime(FILE_PATH)
        ):
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified)
        self.end_headers()
        self.wfile.write(content)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

