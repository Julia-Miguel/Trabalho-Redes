import subprocess
import time

def start_script(script_name):
    print(f"Iniciando {script_name}...")
    subprocess.Popen(f"start cmd.exe /k python {script_name}", shell=True)

if __name__ == "__main__":
    
    udp_server = start_script("udp_server.py")
    time.sleep(1)  # Aguarda 1 segundo

    ac_server = start_script("ac_server.py")
    time.sleep(1)

    lamp_server = start_script("lamp_server.py")
    time.sleep(1)

    tcp_server = start_script("tcp_server.py")
    time.sleep(1)

    tcp_cliente = start_script("tcp_cliente.py")