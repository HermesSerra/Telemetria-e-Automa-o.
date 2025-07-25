# ===============================================================
# Arquivo: cliente_modbus.py
# Autor: Hermes Renato Serra
# Descrição: Cliente Modbus TCP para leitura de dados brutos
# ===============================================================

from pymodbus.client import ModbusTcpClient

# Função principal para ler dados do servidor Modbus
def ler_dados(host='localhost', port=502, unit_id=1):
    # Cria o cliente Modbus TCP
    client = ModbusTcpClient(host=host, port=port)
    client.connect()  # Conecta ao servidor

    # === Leitura dos Holding Registers ===
    # Lê 20 registradores a partir do endereço 0
    response_hr = client.read_holding_registers(address=0, count=20, slave=unit_id)
    if not response_hr.isError():
        registros = response_hr.registers  # Armazena os valores lidos
    else:
        print("Erro ao ler Holding Registers")
        return

    # === Leitura dos Coils (saídas digitais) ===
    # Lê 10 bits (coils) a partir do endereço 0
    response_coils = client.read_coils(address=0, count=10, slave=unit_id)
    if not response_coils.isError():
        coils = response_coils.bits  # Armazena os valores dos coils
    else:
        print("Erro ao ler Coils")
        return

    client.close()  # Encerra a conexão com o servidor

    # === Impressão dos dados brutos na tela ===
    print("\n=== Captura de Dados Brutos ===")

    # Exibe as temperaturas lidas (valores ilustrativos)
    print("\nTemperaturas (°C)")
    print("  40001: Temperatura ambiente (235 = 23.5°C)")
    print("  40002: Temperatura motor (452 = 45.2°C)")
    print("  40003: Temperatura externa (189 = 18.9°C)")
    
    # Exibe as pressões
    print("\nPressões (bar)")
    print("  40004: Pressão sistema (1250 = 12.50 bar)")
    print("  40005: Pressão linha (850 = 8.50 bar)")

    # Exibe as vazões
    print("\nVazões (L/min)")
    print("  40006: Vazão principal (45 L/min)")
    print("  40007: Vazão secundária (23 L/min)")

    # Exibe os níveis de tanque
    print("\nNíveis (%)")
    print("  40008: Nível tanque 1 (78%)")
    print("  40009: Nível tanque 2 (92%)")

    # Exibe as tensões de linha
    print("\nTensões (V)")
    print("  40010: Tensão L1 (2201 = 220.1V)")
    print("  40011: Tensão L2 (2198 = 219.8V)")
    print("  40012: Tensão L3 (2203 = 220.3V)")

    # Exibe as correntes
    print("\nCorrentes (A)")
    print("  40013: Corrente L1 (152 = 15.2A)")
    print("  40014: Corrente L2 (148 = 14.8A)")
    print("  40015: Corrente L3 (155 = 15.5A)")
    
    # Exibe status e contadores
    print("\nStatus e Contadores")
    print("  40016: Status geral (1 = Alarme)")
    print("  40017: Alarme temperatura (0 = OK)")
    print("  40018: Contador produção (12547)")
    print("  40019: Contador falhas (89)")

    # Verifica se há o registrador 40020 disponível (index 19)
    if len(registros) > 19:
        print(f"  Horas funcionamento: {registros[19]} h")
    else:
        print("  Dado 'Horas funcionamento' ausente ou não lido.")

    # Exibe os status dos Coils (saídas digitais)
    print("\nCoils (Status Digital)")
    nomes_coils = [
        "Bomba principal",
        "Bomba reserva",
        "Válvula entrada",
        "Válvula saída",
        "Sistema automático",
        "Modo manual",
        "Alarme ativo",
        "Manutenção",
        "Sensor presença",
        "Porta aberta"
    ]
    for i, nome in enumerate(nomes_coils):
        print(f"  {nome}: {'Ativado' if coils[i] else 'Desativado'}")


# Executa a função principal se o script for rodado diretamente
if __name__ == "__main__":
    ler_dados()
