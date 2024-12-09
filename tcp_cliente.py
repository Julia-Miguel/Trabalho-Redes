import socket
import json

def enviar_comando(tipo_dispositivo, comando):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_TCP))
        comando_completo = {"tipo_dispositivo": tipo_dispositivo, "comando": comando}
        s.sendall(json.dumps(comando_completo).encode())
        resposta = s.recv(BUFFER_SIZE)
        if tipo_dispositivo == "listar_dispositivos":
            dispositivos = json.loads(resposta.decode())
            for nome, info in dispositivos.items():
                print(f"{nome}: {info}")
        else:
            print("Resposta:", resposta.decode())

def obter_lista_dispositivos():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_TCP))
        s.sendall(json.dumps({"tipo_dispositivo": "listar_dispositivos", "comando": {}}).encode())
        resposta = s.recv(BUFFER_SIZE).decode()
    try:
        return json.loads(resposta)
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta.")
        return {}

def menu_controle_dispositivo(tipo_dispositivo):
    dispositivos = obter_lista_dispositivos()
    if not dispositivos:
        print("Nenhum dispositivo encontrado.")
        return

    nome_dispositivo = input("Digite o código do dispositivo que deseja alterar: ")
    if nome_dispositivo not in dispositivos:
        print("Dispositivo não encontrado.")
        return
    while True:
        print(f"\nControle do {tipo_dispositivo}:")
        print("1. Ligar")
        print("2. Desligar")
        if tipo_dispositivo == "ar-condicionado":
            print("3. Alterar temperatura")
            print("4. Alterar modo")
        elif tipo_dispositivo == "lampada":
            print("3. Alterar intensidade")
            print("4. Alterar cor")
        print("5. Alterar nome")
        print("6. Voltar")
        escolha_dispositivo = input("Escolha uma opção: ")

        if escolha_dispositivo in ["1", "2"]:
            acao = "ligar" if escolha_dispositivo == "1" else "desligar"
            enviar_comando(nome_dispositivo, {"acao": acao})
        elif escolha_dispositivo in ["3", "4"]:
            if escolha_dispositivo == "3":
                acao = "alterar_temperatura" if tipo_dispositivo == "ar-condicionado" else "alterar_intensidade"
                valor = input(f"Digite o valor para {acao}: ")
                enviar_comando(nome_dispositivo, {"acao": acao, "valor": int(valor)})
            elif escolha_dispositivo == "4":
                acao = "alterar_modo" if tipo_dispositivo == "ar-condicionado" else "alterar_cor"
                valor = input(f"Digite o valor para {acao}: ")
                enviar_comando(nome_dispositivo, {"acao": acao, "valor": valor})
        elif escolha_dispositivo == "5":
            novo_nome = input("Digite o novo nome para o dispositivo: ")
            enviar_comando(nome_dispositivo, {"acao": "alterar_nome", "valor": novo_nome})
        elif escolha_dispositivo == "6":
            break

HOST = '127.0.0.1'
PORT_TCP = 20000
BUFFER_SIZE = 1024

while True:
    print("\nMenu Principal:")
    print("1. Listar dispositivos")
    print("2. Controlar Ar-condicionado")
    print("3. Controlar Lâmpada")
    print("4. Sair")
    escolha_principal = input("Escolha uma opção: ")

    if escolha_principal == '1':
        enviar_comando("listar_dispositivos", {})
    elif escolha_principal == '2':
        menu_controle_dispositivo("ar-condicionado")
    elif escolha_principal == '3':
        menu_controle_dispositivo("lampada")
    elif escolha_principal == '4':
        break
