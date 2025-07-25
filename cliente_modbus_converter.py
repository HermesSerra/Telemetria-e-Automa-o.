# ===============================================================
# Arquivo: cliente_modbus_convertido.py
# Autor: Hermes Renato Serra
# Descrição: Cliente Modbus TCP que lê e converte dados de sensores
# ===============================================================

from pymodbus.client import ModbusTcpClient

# Função principal para conectar ao servidor Modbus TCP e ler dados convertidos
def ler_dados_convertidos(host='localhost', port=502, unit_id=1):
    # Cria o cliente Modbus TCP com IP e porta do servidor
    client = ModbusTcpClient(host=host, port=port)
    client.connect()  # Estabelece conexão

    # === Leitura dos Holding Registers ===
    # Endereço inicial: 0 | Quantidade: 20 | ID do escravo: unit_id
    response_hr = client.read_holding_registers(address=0, count=20, slave=unit_id)
    if not response_hr.isError():
        registros = response_hr.registers  # Armazena os registradores lidos
    else:
        print("Erro ao ler Holding Registers")
        return

    # === Leitura dos Coils ===
    # Lê 10 coils (bits digitais) a partir do endereço 0
    response_coils = client.read_coils(address=0, count=10, slave=unit_id)
    if not response_coils.isError():
        coils = response_coils.bits  # Armazena os bits lidos
    else:
        print("Erro ao ler Coils")
        return

    client.close()  # Encerra conexão com o servidor

    # === Exibição dos dados convertidos e organizados ===
    print("\n=== DADOS CONVERTIDOS E AGRUPADOS ===")

    # Temperaturas em graus Celsius (dividido por 10 para obter casas decimais)
    print("\nTemperaturas (°C)")
    print(f"  Temperatura ambiente: {registros[0] / 10:.1f} °C")
    print(f"  Temperatura motor: {registros[1] / 10:.1f} °C")
    print(f"  Temperatura externa: {registros[2] / 10:.1f} °C")

    # Pressões em bar (dividido por 100 para obter casas decimais)
    print("\nPressões (bar)")
    print(f"  Pressão sistema: {registros[3] / 100:.2f} bar")
    print(f"  Pressão linha: {registros[4] / 100:.2f} bar")

    # Vazões em litros por minuto (valores inteiros)
    print("\nVazões (L/min)")
    print(f"  Vazão principal: {registros[5]} L/min")
    print(f"  Vazão secundária: {registros[6]} L/min")

    # Níveis de tanque em porcentagem
    print("\nNíveis (%)")
    print(f"  Nível tanque 1: {registros[7]}%")
    print(f"  Nível tanque 2: {registros[8]}%")

    # Tensões em Volts (dividido por 10)
    print("\nTensões (V)")
    print(f"  Tensão L1: {registros[9] / 10:.1f} V")
    print(f"  Tensão L2: {registros[10] / 10:.1f} V")
    print(f"  Tensão L3: {registros[11] / 10:.1f} V")

    # Correntes em Amperes (dividido por 10)
    print("\nCorrentes (A)")
    print(f"  Corrente L1: {registros[12] / 10:.1f} A")
    print(f"  Corrente L2: {registros[13] / 10:.1f} A")
    print(f"  Corrente L3: {registros[14] / 10:.1f} A")

    # Outros dados diversos como status e contadores
    print("\nStatus e Contadores")
    print(f"  Status geral: {registros[15]}")
    print(f"  Alarme temperatura: {registros[16]}")
    print(f"  Contador produção: {registros[17]}")
    print(f"  Contador falhas: {registros[18]}")
    if len(registros) > 19:
        print(f"  Horas funcionamento: {registros[19]} h")
    else:
        print("  Dado 'Horas funcionamento' ausente ou não lido.")

    # Exibe o estado dos Coils (ligado/desligado)
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


# Ponto de entrada do script (executa a função principal)
if __name__ == "__main__":
    ler_dados_convertidos()
