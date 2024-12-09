# lampada_device.py
import json
import socket

class Lampada:
    def __init__(self):
        self.nome = "nome"
        self.estado = "desligada"
        self.cor = "branca"
        self.intensidade = 50  # Intensidade em porcentagem
        self.arquivo_estado = "estado_lampada.json"
        self.carregar_estado()
        self.registrar_no_servidor_udp()
        
    def registrar_no_servidor_udp(self):
        HOST_UDP = '127.0.0.1'
        PORT_UDP = 20001
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Inclua o IP e a porta do servidor da lâmpada
        IP_LAMPADA = '127.0.0.1'  # Substitua pelo IP real do servidor da lâmpada
        PORTA_LAMPADA = 20002     # Substitua pela porta real do servidor da lâmpada

        dispositivo_info = {
            "nome": self.nome,
            "tipo": "lampada",
            "ip": IP_LAMPADA,
            "porta": PORTA_LAMPADA,
            "configuracoes": {
                "estado": self.estado,
                "cor": self.cor,
                "intensidade": self.intensidade
            }
        }

        mensagem = json.dumps(dispositivo_info).encode()
        udp_socket.sendto(mensagem, (HOST_UDP, PORT_UDP))
        udp_socket.close()
        
    def dispositivo_do_tipo_ja_registrado(self):
        try:
            with open('dispositivos.json', 'r') as file:
                dispositivos = json.load(file)
                return any(dispositivo['tipo'] == 'lampada' for dispositivo in dispositivos.values())
        except FileNotFoundError:
            return False
        
    def alterar_nome(self, novo_nome):
        self.nome = novo_nome
        self.salvar_estado()
        self.registrar_no_servidor_udp()
        return f"Nome da lâmpada alterado para {novo_nome}"

        
    def alterar_intensidade(self, nova_intensidade):
        if 0 <= nova_intensidade <= 100:
            self.intensidade = nova_intensidade
            self.salvar_estado()
            self.registrar_no_servidor_udp()
            return f"Intensidade ajustada para {nova_intensidade}%."
        else:
            return "Intensidade fora da faixa permitida (0-100)."

    def alterar_cor(self, nova_cor):
        cores_aceitaveis = ['cinza', 'verde', 'vermelho', 'azul', 'amarelo', 'branco','laranja', 'roxo', 'rosa', 'marrom', 'bege', 'ciano', 'magenta', 'turquesa', 'aqua', 'salmao', 'verde limao', 'verde musgo', 'verde oliva', 'verde escuro', 'verde claro', 'verde agua', 'verde mar', 'verde floresta', 'verde prima']
        
        if nova_cor.lower() in cores_aceitaveis:
            self.cor = nova_cor
            self.salvar_estado()
            self.registrar_no_servidor_udp()
            return f"Cor ajustada para {nova_cor}."
        else:
            return f"Erro: Cor '{nova_cor}' não é aceitável. As cores aceitáveis são {cores_aceitaveis}."

    def salvar_estado(self):
        estado = {
            "nome": self.nome,
            "tipo": "lampada",
            "ip": "127.0.0.1",  # Você pode atualizar o IP, se necessário
            "porta": 20002,     # Você pode atualizar a porta, se necessário
            "configuracoes": {
                "estado": self.estado,
                "cor": self.cor,
                "intensidade": self.intensidade
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
                self.cor = estado.get("configuracoes", {}).get("cor", self.cor)
                self.intensidade = estado.get("configuracoes", {}).get("intensidade", self.intensidade)
        except FileNotFoundError:
            self.salvar_estado()

    def processar_comando(self, comando):
        if comando == "ligar":
            self.estado = "ligada"
        elif comando == "desligar":
            self.estado = "desligada"
        elif comando.startswith("cor "):
            self.cor = comando.split(" ")[1]
        elif comando.startswith("intensidade "):
            try:
                intensidade = int(comando.split(" ")[1])
                if 0 <= intensidade <= 100:
                    self.intensidade = intensidade
                else:
                    return "Intensidade fora da faixa permitida (0-100)."
            except ValueError:
                return "Comando inválido para intensidade."
        else:
            return "Comando inválido."

        self.salvar_estado()
        self.registrar_no_servidor_udp()
        return f"Lâmpada {self.estado}, Cor: {self.cor}, Intensidade: {self.intensidade}%"
