import socket

from encrypted_dns import parse, upstream


class Server:

    def __init__(self, ip='127.0.0.1', port=10053):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.server.bind((self.ip, self.port))

        while True:
            query_data, query_address = self.server.recvfrom(512)
            print('query_data:', query_data)
            self.handle_query(query_data, query_address)

    def _send(self, response_data, address):
        self.server.sendto(response_data, address)

    def handle_query(self, query_data, query_address):
        query_parser = parse.ParseQuery(query_data)
        parse_result = query_parser.parse_plain()
        print('parse_result:', parse_result)

        https_upstream = upstream.HTTPSUpsream('https://cloudflare-dns.com/dns-query?')
        response = https_upstream.query(query_data)
        self.server.sendto(response, query_address)


test_server = Server()
test_server.start()
