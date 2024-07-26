import http.server
import socketserver
import json

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/order':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            global inventory
            item_type = data.get('itemType', '')
            quantity = data.get('quantity', 0)

            if item_type in inventory and inventory[item_type] >= quantity:
                inventory[item_type] -= quantity
                response = {'success': True, 'message': 'Thank you for the order!', 'new_quantity': inventory[item_type]}
            else:
                response = {'success': False, 'message': 'Not enough stock available.'}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

inventory = {
    'Tomato': 50,
    'Potato': 50,
    'Broccoli': 50
}

Handler = RequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
