import socketserver

class BlackJackServer(socketserver.StreamRequestHandler):
    def setup(self) -> None:
        return super().setup()

    def handle(self) -> None:
        return "hello"

    def finish(self) -> None:
        return super().finish()

if __name__ == "__main__":
    with socketserver.TCPServer(("192.168.31.187", 48897), BlackJackServer) as server:
        server.serve_forever()