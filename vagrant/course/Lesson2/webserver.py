#!/usr/bin/env python2

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ""
            output += """\
                <html>
                    <body>
                        <h1>Hello!</h1>
                        <form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name='message' type='text'>
                            <input type='submit' value='Submit'>
                        </form>
                    </body>
                </html>"""
            self.wfile.write(output)
            print(output)
            return
        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ""
            output += """\
                <html>
                    <body>
                        <h1>&#161Hola!</h1>
                        <a href='/hello'>Back to Hello</a>
                        <form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name='message' type='text'>
                            <input type='submit' value='Submit'>
                        </form>
                </body>
            </html>"""
            self.wfile.write(output)
            print(output)
            return
        else:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messageContent = fields.get('message')

        output = ""
        output += """\
            <html>
                <body>
                    <h2>Okay, how about this: </h2>"""
        output += "<h1> %s </h1>" % messageContent[0]
        output += """\
                    <form method='POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like me to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='Submit'>
                    </form>
                </body>
            </html>"""
        self.wfile.write(output)
        print(output)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
