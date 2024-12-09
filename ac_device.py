import json
import socket

class ArCondicionado:
    def __init__(self):
        self.nome = "nome"
        self.estado = "desligado"
        self.temperatura = 24
        self.modo = "resfriamento"
        self.arquivo_estado = "estado_arcondicionado.json"
        self.carregar_estado()
        self.registrar_no_servidor_udp()
        
    def registrar_no_servidor_udp(self):
        HOST_UDP = '127.0.0.1'
        PORT_UDP = 20001
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Inclua o IP e a porta do servidor do ar-condicionado
        IP_ARCONDICIONADO = '127.0.0.1'  # Substitua pelo IP real do servidor do ar-condicionado
        PORTA_ARCONDICIONADO = 20003     # Substitua pela porta real do servidor do ar-condicionado

        dispositivo_info = {
            "nome": self.nome,
            "tipo": "ar-condicionado",
            "ip": IP_ARCONDICIONADO,
            "porta": PORTA_ARCONDICIONADO,
            "configuracoes": {
                "estado": self.estado,
                "temperatura": self.temperatura,
                "modo": self.modo
            }
        }

        mensagem = json.dumps(dispositivo_info).encode()
        udp_socket.sendto(mensagem, (HOST_UDP, PORT_UDP))
        udp_socket.close()
        
    def dispositivo_do_tipo_ja_registrado(self):
        try:
            with open('dispositivos.json', 'r') as file:
                dispositivos = json.load(file)
                return any(dispositivo['tipo'] == 'ar-condicionado' for dispositivo in dispositivos.values())
        except FileNotFoundError:
            return False
        
    def alterar_nome(self, novo_nome):
        self.nome = novo_nome
        self.salvar_estado()
        self.registrar_no_servidor_udp()
        return f"Nome do ar-condicionado alterado para {novo_nome}"

    def alterar_temperatura(self, nova_temperatura):
        if 16 <= nova_temperatura <= 30:
            self.temperatura = nova_temperatura
            self.salvar_estado()
            self.registrar_no_servidor_udp()
            return f"Temperatura ajustada para {nova_temperatura}°C."
        else:
            return "Temperatura fora da faixa permitida (16-30°C)."

    def alterar_modo(self, novo_modo):
        modos_aceitaveis = ['resfriamento', 'aquecimento', 'ventilacao']
        if novo_modo.lower() in modos_aceitaveis:
            self.modo = novo_modo.lower()
            self.salvar_estado()
            self.registrar_no_servidor_udp()
            return f"Modo ajustado para {novo_modo}."
        else:
            return f"Erro: Modo '{novo_modo}' não é aceitável. Os modos aceitáveis são {', '.join(modos_aceitaveis)}."

    def salvar_estado(self):
        estado = {
            "nome": self.nome,
            "tipo": "ar-condicionado",
            "ip": "127.0.0.1",  # Você pode atualizar o IP, se necessário
            "porta": 20003,     # Você pode atualizar a porta, se necessário
            "configuracoes": {
                "estado": self.estado,
                "temperatura": self.temperatura,
                "modo": self.modo
            }
        }
        try:
            with open(self.arquivo_estado, 'w') as file:
                json.dump(estado, file)
        except Exception as e:
            print(f"Erro ao salvar o estado: {e}")

    def carregar_estado(self):
        try:
            with open(self.arquivo_estado, 'r') as file:
                estado = json.load(file)
                self.nome = estado.get("nome", self.nome)
                self.estado = estado.get("configuracoes", {}).get("estado", self.estado)
                self.temperatura = estado.get("configuracoes", {}).get("temperatura", self.temperatura)
                self.modo = estado.get("configuracoes", {}).get("modo", self.modo)
        except FileNotFoundError:
            self.salvar_estado()

    def processar_comando(self, comando):
        if comando == "ligar":
            self.estado = "ligado"
        elif comando == "desligar":
            self.estado = "desligado"
        else:
            return "Comando inválido."

        self.salvar_estado()
        self.registrar_no_servidor_udp()
        return f"Ar-Condicionado {self.estado}, Temperatura: {self.temperatura}°C, Modo: {self.modo}"
