import socket
import threading
import pickle
import struct

PORT = 5555
BUFFER_SIZE = 4096

# --- Fonctions pour envoi sécurisé de messages ---
def send_msg(sock, data):
    try:
        serialized = pickle.dumps(data)
        length = struct.pack('>I', len(serialized))
        sock.sendall(length + serialized)
    except Exception as e:
        print("❌ Envoi échoué :", e)

def recv_msg(sock):
    try:
        raw_len = recvall(sock, 4)
        if not raw_len:
            return None
        msg_len = struct.unpack('>I', raw_len)[0]
        return pickle.loads(recvall(sock, msg_len))
    except:
        return None

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

# --- Serveur ---
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

        def listen():
            self.conn, self.addr = self.socket.accept()
            print(f"[🔗 Client connecté depuis {self.addr}]")
            while self.running:
                data = recv_msg(self.conn)
                if data and self.on_receive:
                    self.on_receive(data)

        threading.Thread(target=listen, daemon=True).start()

    def send(self, data):
        if self.conn:
            send_msg(self.conn, data)

    def stop(self):
        self.running = False
        if self.conn:
            self.conn.close()
        self.socket.close()

# --- Client ---
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
            print(f"[✅ Connecté à {self.server_ip}:{self.port}]")

            def listen():
                while self.running:
                    data = recv_msg(self.socket)
                    if data and self.on_receive:
                        self.on_receive(data)

            threading.Thread(target=listen, daemon=True).start()
        except Exception as e:
            print(f"❌ Connexion échouée : {e}")

    def send(self, data):
        send_msg(self.socket, data)

    def stop(self):
        self.running = False
        self.socket.close()
