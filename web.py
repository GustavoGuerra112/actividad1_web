from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def valida_autor(self):
        if 'autor' in self.query_data():
            return True

    def get_html(self, path, qs):
        proyecto = path.split("/")[-1]
        return f"""
        <html>
        <h1>Proyecto: {proyecto} Autor: {qs['autor']}</h1>
        </html>
        """
    def ruta(self):
         return self.url().path

    def do_GET(self):
        print("----- REQUEST -----")
        print("Host:", self.headers.get("Host"))
        print("User-Agent:", self.headers.get("User-Agent"))
        print("Ruta solicitada:", self.path)

        contenido = {
            "/proyecto/web-uno": """
                <html><h1>Proyecto: web-uno</h1></html>
            """,
            "/proyecto/web-dos": """
                <html><h1>Proyecto: web-dos</h1></html>
            """,
            "/proyecto/web-tres": """
                <html><h1>Proyecto: web-tres</h1></html>
            """
        }

    
        if self.ruta() == "/":
            try:
                with open("home.html", "r", encoding="utf-8") as archivo:
                    html = archivo.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                print("----- RESPONSE -----")
                print("Content-Type: text/html")
                print("Server:", self.version_string())
                print("Date:", self.date_time_string())

                self.wfile.write(html.encode("utf-8"))

            except FileNotFoundError:
                self.send_error(500, "home.html no encontrado")

        
        elif self.valida_autor():
            html = self.get_html(self.ruta(), self.query_data())

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            print("----- RESPONSE -----")
            print("Content-Type: text/html")
            print("Server:", self.version_string())
            print("Date:", self.date_time_string())

            self.wfile.write(html.encode("utf-8"))

        
        elif self.ruta() in contenido:

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            print("----- RESPONSE -----")
            print("Content-Type: text/html")
            print("Server:", self.version_string())
            print("Date:", self.date_time_string())

            self.wfile.write(contenido[self.ruta()].encode("utf-8"))

      
        else:
            self.send_error(404, "Ruta no encontrada")

    
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
