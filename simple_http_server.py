from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length).decode('utf-8'))
        print (body)
        set_of_strings = body.get('setOfStrings', None)
        if not 'setOfStrings' in body:
            self.wfile.write(json.dumps({'status': 500, 'message': 'no body found in the post request'}).encode('utf-8'))
        elif not set_of_strings or len(set_of_strings)==0:
            self.wfile.write(json.dumps({'status': 500, 'message': 'setOfString should not be empty or null'}).encode('utf-8'))
        else:
            try:
                str_list = [x['value'] for x in set_of_strings]
                response = self.find_lcs(str_list)
                self.wfile.write(json.dumps({'lcs': response}).encode('utf-8'))
            except KeyError as k:
                self.wfile.write(json.dumps({'status': 500, 'message': 'key value is missing in one of the set', 'exception': str(k)}).encode('utf-8'))
            except ValueError as v:
                self.wfile.write(json.dumps({'status': 500, 'message': 'error while parsing data', 'exception': str(v)}).encode('utf-8'))
            except Exception as ex:
                self.wfile.write(json.dumps({'status': 500, 'message': 'something wrong happened', 'exception': str(ex)}).encode('utf-8'))

    def find_lcs(self, str_list):
        substr = ''
        if len(str_list) > 1 and len(str_list[0]) > 0:
            for i in range(len(str_list[0])):
                for j in range(len(str_list[0])-i+1):
                    if j > len(substr) and all(str_list[0][i:i+j] in x for x in str_list):
                        substr = str_list[0][i:i+j]
        elif len(str_list)==1:
            substr = str_list[0]
        print (substr)
        return [{'value': substr}]


def run(server_class=HTTPServer, handler_class=S, port=7071):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
