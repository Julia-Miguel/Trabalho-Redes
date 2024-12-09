import socket
import threading
import json
from lamp_device import Lampada

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 20002  # Uma porta única para o servidor da lâmpada
BUFFER_SIZE = 1024

# Instância da lâmpada
dispositivo = Lampada()

# Função para lidar com conexões de cliente
def handle_client_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            try:
                comando = json.loads(data.decode())
                acao = comando.get("acao")

                if acao == "alterar_nome":
                    novo_nome = comando.get("valor", "")
                    resposta = dispositivo.alterar_nome(novo_nome) or "Nome alterado, mas sem resposta do dispositivo."
                    print(f"Nome alterado para {novo_nome}")
                    client_socket.sendall(resposta.encode())

                elif acao == "alterar_intensidade":
                    nova_intensidade = int(comando.get("valor", 0))
                    resposta = dispositivo.alterar_intensidade(nova_intensidade)

                elif acao == "alterar_cor":
                    nova_cor = comando.get("valor", "").lower()
                    resposta = dispositivo.alterar_cor(nova_cor)

                else:
                    resposta = dispositivo.processar_comando(acao)

                dispositivo.salvar_estado()
                client_socket.sendall(resposta.encode())

            except json.JSONDecodeError as e:
                client_socket.sendall(f"Erro ao decodificar o comando: {str(e)}".encode())
            except KeyError as e:
                client_socket.sendall(f"Erro no comando recebido: {str(e)}".encode())
    except Exception as e:
        print(f"Erro na conexão: {e}")
    finally:
        client_socket.close()

# Inicializando o servidor TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor da Lâmpada rodando em {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
    thread.start()