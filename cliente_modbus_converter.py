from pymodbus.client import ModbusTcpClient

def ler_dados_convertidos(host='localhost', port=502, unit_id=1):
    client = ModbusTcpClient(host=host, port=port)
    client.connect()

    # Holding Registers
    response_hr = client.read_holding_registers(address=0, count=20, slave=unit_id)
    if not response_hr.isError():
        registros = response_hr.registers
    else:
        print("Erro ao ler Holding Registers")
        return

    # Coils
    response_coils = client.read_coils(address=0, count=10, slave=unit_id)
    if not response_coils.isError():
        coils = response_coils.bits
    else:
        print("Erro ao ler Coils")
        return

    client.close()

    # Exibição dos dados
    print("\n=== DADOS CONVERTIDOS E AGRUPADOS ===")

    print("\nTemperaturas (°C)")
    print(f"  Temperatura ambiente: {registros[0] / 10:.1f} °C")
    print(f"  Temperatura motor: {registros[1] / 10:.1f} °C")
    print(f"  Temperatura externa: {registros[2] / 10:.1f} °C")

    print("\nPressões (bar)")
    print(f"  Pressão sistema: {registros[3] / 100:.2f} bar")
    print(f"  Pressão linha: {registros[4] / 100:.2f} bar")

    print("\nVazões (L/min)")
    print(f"  Vazão principal: {registros[5]} L/min")
    print(f"  Vazão secundária: {registros[6]} L/min")

    print("\nNíveis (%)")
    print(f"  Nível tanque 1: {registros[7]}%")
    print(f"  Nível tanque 2: {registros[8]}%")

    print("\nTensões (V)")
    print(f"  Tensão L1: {registros[9] / 10:.1f} V")
    print(f"  Tensão L2: {registros[10] / 10:.1f} V")
    print(f"  Tensão L3: {registros[11] / 10:.1f} V")

    print("\nCorrentes (A)")
    print(f"  Corrente L1: {registros[12] / 10:.1f} A")
    print(f"  Corrente L2: {registros[13] / 10:.1f} A")
    print(f"  Corrente L3: {registros[14] / 10:.1f} A")

    print("\nStatus e Contadores")
    print(f"  Status geral: {registros[15]}")
    print(f"  Alarme temperatura: {registros[16]}")
    print(f"  Contador produção: {registros[17]}")
    print(f"  Contador falhas: {registros[18]}")
    if len(registros) > 19:
        print(f"  Horas funcionamento: {registros[19]} h")
    else:
        print("  Dado 'Horas funcionamento' ausente ou não lido.")

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


if __name__ == "__main__":
    ler_dados_convertidos()
