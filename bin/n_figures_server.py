from server.ChessServer import ChessServer

if __name__ == "__main__":
    server = ChessServer("localhost", 9998)

    server.start()
