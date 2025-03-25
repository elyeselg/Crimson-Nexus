import socket
import threading
import pickle

BUFFER_SIZE = 4096


class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.conn = None
        self.addr = None
        self.running = False
        self.on_receive = None  # Callback à définir côté jeu

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(1)
        print(f"Serveur prêt sur {self.host}:{self.port}, en attente d’un joueur...")

        self.conn, self.addr = server.accept()
        print(f"Joueur connecté depuis {self.addr}")
        self.running = True

        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def listen(self):
        while self.running:
            try:
                data = self.conn.recv(BUFFER_SIZE)
                if data:
                    obj = pickle.loads(data)
                    if self.on_receive:
                        self.on_receive(obj)
            except:
                print("Erreur de réception (serveur)")
                self.running = False
                break

    def send(self, obj):
        if self.conn:
            try:
                data = pickle.dumps(obj)
                self.conn.sendall(data)
            except:
                print("Erreur d’envoi (serveur)")

    def stop(self):
        self.running = False
        if self.conn:
            self.conn.close()


class GameClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self.on_receive = None  # Callback à définir côté jeu

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.running = True
            thread = threading.Thread(target=self.listen, daemon=True)
            thread.start()
            print(f"Connecté au serveur {self.host}:{self.port}")
        except:
            print("Impossible de se connecter au serveur")

    def listen(self):
        while self.running:
            try:
                data = self.sock.recv(BUFFER_SIZE)
                if data:
                    obj = pickle.loads(data)
                    if self.on_receive:
                        self.on_receive(obj)
            except:
                print("Erreur de réception (client)")
                self.running = False
                break

    def send(self, obj):
        if self.sock:
            try:
                data = pickle.dumps(obj)
                self.sock.sendall(data)
            except:
                print("Erreur d’envoi (client)")

    def disconnect(self):
        self.running = False
        if self.sock:
            self.sock.close()
