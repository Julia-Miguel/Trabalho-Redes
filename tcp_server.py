import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024
FILE_NAME = "dispositivos.json"

# Carregar dispositivos do arquivo JSON
def carregar_dispositivos():
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Salvar dispositivos em arquivo JSON
def salvar_dispositivos(dispositivos):
    with open(FILE_NAME, 'w') as file:
        json.dump(dispositivos, file, indent=4)

def enviar_comando_para_dispositivo(dispositivo_info, comando):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((dispositivo_info['ip'], dispositivo_info['porta']))
            s.sendall(json.dumps(comando).encode())
            resposta = s.recv(BUFFER_SIZE)
            return resposta.decode()
    except Exception as e:
        return f"Erro ao enviar comando para o dispositivo: {e}"

def processar_comando(client_socket, comando_recebido, dispositivos):
    resposta = ""
    nome_dispositivo = comando_recebido.get("tipo_dispositivo")  # Este é o nome do dispositivo
    comando = comando_recebido.get("comando")

    if nome_dispositivo == "listar_dispositivos":
        dispositivos_atualizados = carregar_dispositivos()  # Recarrega os dispositivos do arquivo JSON
        resposta = json.dumps(dispositivos_atualizados)
    elif nome_dispositivo in dispositivos:
        dispositivo_info = dispositivos[nome_dispositivo]

        # Encaminha o comando para o servidor do dispositivo
        resposta = enviar_comando_para_dispositivo(dispositivo_info, comando)
    else:
        resposta = "Dispositivo não encontrado ou comando inválido."

    client_socket.sendall(resposta.encode())

def on_new_client(client_socket, addr, dispositivos):
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break

        try:
            comando_recebido = json.loads(data.decode())
            processar_comando(client_socket, comando_recebido, dispositivos)
        except Exception as e:
            resposta = f"Erro ao processar comando: {e}"
            client_socket.sendall(resposta.encode())

def start_tcp_server(dispositivos):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor TCP rodando em {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=on_new_client, args=(client_socket, addr, dispositivos))
            thread.start()

if __name__ == "__main__":
    dispositivos = carregar_dispositivos()
    start_tcp_server(dispositivos)
