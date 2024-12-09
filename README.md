
# Projeto de Redes - Sistema de Casa Inteligente

## Descrição
Este projeto simula um sistema de casa inteligente, permitindo o controle remoto de dispositivos como ar-condicionado e lâmpadas. Implementa uma arquitetura de servidor-cliente para gerenciar os comandos dos dispositivos e permite a interação do usuário por meio de uma interface de cliente.

## Autores
- André Lucas Santos
- Júlia Roberta Gomes Miguel

## Instalação
Para executar este projeto, certifique-se de ter o Python instalado em seu sistema. Clone este repositório:

```bash
git clone https://github.com/Andre023/TP-redes-de-computadores.git
```

## Uso
Para iniciar o sistema, execute o seguinte comando no terminal:

```bash
python inicializador.py
```
Este comando inicia todos os serviços necessários em ordem, incluindo servidores para os dispositivos e o servidor central, além da interface do cliente.

## Arquivos no Projeto
- `ac_device.py`: Simula um dispositivo de ar-condicionado, permitindo alterações no estado e na temperatura.
- `ac_server.py`: Servidor dedicado ao dispositivo de ar-condicionado, gerencia comandos e atualizações de estado.
- `lamp_device.py`: Simula um dispositivo de lâmpada, permitindo alterações no estado, cor e intensidade.
- `lamp_server.py`: Servidor dedicado ao dispositivo de lâmpada, gerencia comandos e atualizações de estado.
- `tcp_cliente.py`: Interface de usuário para interação com os dispositivos, permite alterações de estado e configurações.
- `tcp_server.py`: Servidor central que gerencia os comandos dos usuários e os redireciona para o servidor do dispositivo apropriado.
- `udp_server.py`: Servidor usado para o registro inicial dos dispositivos, armazenando suas informações.
- `inicializador.py`: Script para iniciar todos os componentes necessários do sistema em ordem.
- `dispositivos.json`: Armazena informações sobre os dispositivos registrados no sistema.
- `estado_arcondicionado.json`: Armazena o estado atual do dispositivo de ar-condicionado.
- `estado_lampada.json`: Armazena o estado atual do dispositivo de lâmpada.

## Contribuição
Contribuições para o projeto são bem-vindas. Para contribuir, faça um fork do repositório, crie suas alterações e envie um pull request para revisão.
