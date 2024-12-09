import subprocess
import time
import socket
import json

HOST = '127.0.0.1'
PORT = 20001
BUFFER_SIZE = 1024
FILE_NAME = "dispositivos.json"

dispositivos = {}

def carregar_dispositivos():
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salvar_dispositivos():
    with open(FILE_NAME, 'w') as file:
        json.dump(dispositivos, file, indent=4)


def main():
    
    global dispositivos
    dispositivos = carregar_dispositivos()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
        UDPServerSocket.bind((HOST, PORT))
        print("Servidor UDP ouvindo em {}:{}".format(HOST, PORT))

        while True:
            mensagem, endereco = UDPServerSocket.recvfrom(BUFFER_SIZE)
            print(f"Mensagem recebida de {endereco}: {mensagem.decode()}")
            dispositivo_info = json.loads(mensagem.decode())

            # Verifica se o dispositivo já está registrado
            dispositivo_existente = next((nome for nome, info in dispositivos.items() if info['ip'] == dispositivo_info['ip'] and info['porta'] == dispositivo_info['porta']), None)
            if dispositivo_existente:
                # Atualiza a entrada existente
                dispositivos[dispositivo_existente] = dispositivo_info
            else:
                # Adiciona novo dispositivo
                dispositivos[dispositivo_info['nome']] = dispositivo_info

            salvar_dispositivos()

if __name__ == "__main__":
    main()
