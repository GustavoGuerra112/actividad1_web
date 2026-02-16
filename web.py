from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        if self.url().path == '/':
            try:
                with open('home.html', 'r', encoding='utf-8') as archivo:
                    html = archivo.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            except FileNotFoundError:
                self.send_response(500)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Error: home.html no encontrado</h1>")

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina no encontrada</h1>")

    """def do_GET(self):
        if self.url().path == '/':
            archivo =open('home.html')
            html=archivo.read()
            self.send_response(200)
            self.send_header("Content-Type","text/html")
            self.end_headers()
            self.wfile.write(html).endcode("utf-8")

        if self.valida.autor():    
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_html(self.url().path,self.querydata()).encode("utf-8"))
        else:
            self.send_error(404,'El autor no existe')
    """
    def valida_autor(self):
        if 'autor' in self.query_data():
            return True
    def get_html(self, path, qs):
    
        return f"""
        <h1>Proyecto: {path} Autor: {qs['autor']} </h1>
"""
    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
"""


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
