import json
from pymodbus.client import ModbusTcpClient

def validar_faixa(valor, minimo, maximo):
    return minimo <= valor <= maximo

def ler_dados_json(host='localhost', port=502, unit_id=1):
    client = ModbusTcpClient(host=host, port=port)
    client.connect()

    response_hr = client.read_holding_registers(address=0, count=20, slave=unit_id)
    response_coils = client.read_coils(address=0, count=10, slave=unit_id)

    if response_hr.isError() or response_coils.isError():
        print("Erro na leitura Modbus")
        client.close()
        return

    registros = response_hr.registers
    coils = response_coils.bits

    if len(registros) < 20:
        print("Erro: registros incompletos")
        client.close()
        return

    # Conversões com validação
    temperaturas = {
        "ambiente": registros[0] / 10 if validar_faixa(registros[0] / 10, -40, 150) else None,
        "motor": registros[1] / 10 if validar_faixa(registros[1] / 10, -40, 150) else None,
        "externa": registros[2] / 10 if validar_faixa(registros[2] / 10, -40, 150) else None
    }

    pressoes = {
        "sistema": registros[3] / 100 if validar_faixa(registros[3] / 100, 0, 20) else None,
        "linha": registros[4] / 100 if validar_faixa(registros[4] / 100, 0, 20) else None
    }

    vazoes = {
        "principal": registros[5] if validar_faixa(registros[5], 0, 100) else None,
        "secundaria": registros[6] if validar_faixa(registros[6], 0, 100) else None
    }

    niveis = {
        "tanque1": registros[7] if validar_faixa(registros[7], 0, 100) else None,
        "tanque2": registros[8] if validar_faixa(registros[8], 0, 100) else None
    }

    tensoes = {
        "L1": registros[9] / 10 if validar_faixa(registros[9] / 10, 180, 260) else None,
        "L2": registros[10] / 10 if validar_faixa(registros[10] / 10, 180, 260) else None,
        "L3": registros[11] / 10 if validar_faixa(registros[11] / 10, 180, 260) else None
    }

    correntes = {
        "L1": registros[12] / 10 if validar_faixa(registros[12] / 10, 0, 100) else None,
        "L2": registros[13] / 10 if validar_faixa(registros[13] / 10, 0, 100) else None,
        "L3": registros[14] / 10 if validar_faixa(registros[14] / 10, 0, 100) else None
    }

    status = {
        "geral": registros[15],
        "alarme_temperatura": registros[16],
        "contador_producao": registros[17],
        "contador_falhas": registros[18],
        "horas_funcionamento": registros[19]
    }

    coils_data = {
        "ligado": coils[0] if len(coils) > 0 else None,
        "em_alarme": coils[1] if len(coils) > 1 else None,
        "manual": coils[2] if len(coils) > 2 else None
    }

    saida = {
        "temperaturas": temperaturas,
        "pressoes": pressoes,
        "vazoes": vazoes,
        "niveis": niveis,
        "tensoes": tensoes,
        "correntes": correntes,
        "status": status,
        "coils": coils_data
    }

    client.close()

    # Exibe no terminal
    print("\n=== JSON GERADO ===\n")
    print(json.dumps(saida, indent=2))

    # Salva no arquivo
    with open("dados_modbus.json", "w") as f:
        json.dump(saida, f, indent=2)

    return saida

# Executa se o arquivo for rodado diretamente
if __name__ == "__main__":
    ler_dados_json()
