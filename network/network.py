import socket
import threading
import pickle

PORT = 5555
BUFFER_SIZE = 4096

class GameServer:
    def __init__(self, host='0.0.0.0', port=PORT):
        self.host = host
        self.port = port
        self.conn = None
        self.addr = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_receive = None
        self.running = True

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"[🟢 Serveur en attente sur {self.host}:{self.port}]")

        def wait_for_client():
            self.conn, self.addr = self.socket.accept()
            print(f"[🔗 Client connecté depuis {self.addr}]")
            while self.running:
                try:
                    data = self.conn.recv(BUFFER_SIZE)
                    if data:
                        move = pickle.loads(data)
                        if self.on_receive:
                            self.on_receive(move)
                except:
                    break

        threading.Thread(target=wait_for_client, daemon=True).start()

    def send(self, move):
        if self.conn:
            try:
                data = pickle.dumps(move)
                self.conn.sendall(data)
            except:
                print("❌ Échec de l'envoi du coup.")

    def stop(self):
        self.running = False
        if self.conn:
            self.conn.close()
        self.socket.close()

class GameClient:
    def __init__(self, server_ip, port=PORT):
        self.server_ip = server_ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_receive = None
        self.running = True

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.port))
            print(f"[✅ Connecté au serveur {self.server_ip}:{self.port}]")

            def listen():
                while self.running:
                    try:
                        data = self.socket.recv(BUFFER_SIZE)
                        if data:
                            move = pickle.loads(data)
                            if self.on_receive:
                                self.on_receive(move)
                    except:
                        break

            threading.Thread(target=listen, daemon=True).start()
        except Exception as e:
            print(f"❌ Connexion échouée : {e}")

    def send(self, move):
        try:
            data = pickle.dumps(move)
            self.socket.sendall(data)
        except:
            print("❌ Échec de l'envoi du coup.")

    def stop(self):
        self.running = False
        self.socket.close()
