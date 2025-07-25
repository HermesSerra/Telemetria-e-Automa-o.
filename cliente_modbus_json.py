# ===============================================================
# Arquivo: cliente_modbus_json.py
# Autor: Hermes Renato Serra
# Descrição: Cliente Modbus TCP que lê dados, valida faixas e exporta para JSON
# ===============================================================

import json
from pymodbus.client import ModbusTcpClient

# Função auxiliar que verifica se um valor está dentro de uma faixa válida
def validar_faixa(valor, minimo, maximo):
    return minimo <= valor <= maximo

# Função principal para leitura, validação e exportação dos dados em JSON
def ler_dados_json(host='localhost', port=502, unit_id=1):
    client = ModbusTcpClient(host=host, port=port)
    client.connect()

    # Leitura dos 20 Holding Registers e 10 Coils
    response_hr = client.read_holding_registers(address=0, count=20, slave=unit_id)
    response_coils = client.read_coils(address=0, count=10, slave=unit_id)

    if response_hr.isError() or response_coils.isError():
        print("Erro na leitura Modbus")
        client.close()
        return

    registros = response_hr.registers if response_hr.registers else []
    coils = response_coils.bits if response_coils.bits else []

    print(f"Recebidos {len(registros)} registradores")

    # Garante que a lista tenha 20 posições (com None se faltar)
    while len(registros) < 20:
        registros.append(None)

    # Função segura com tratamento explícito para dados inválidos
    def seguro(idx, fator=1, minimo=None, maximo=None):
        valor = registros[idx]
        if valor is None:
            return "inválido"
        convertido = valor / fator if fator != 1 else valor
        if minimo is not None and maximo is not None:
            return convertido if validar_faixa(convertido, minimo, maximo) else "inválido"
        return convertido

    temperaturas = {
        "ambiente": seguro(0, 10, -50, 150),
        "motor": seguro(1, 10, -50, 150),
        "externa": seguro(2, 10, -50, 150)
    }

    pressoes = {
        "sistema": seguro(3, 100, 0, 50),
        "linha": seguro(4, 100, 0, 50)
    }

    vazoes = {
        "principal": seguro(5, 1, 0, 1000),
        "secundaria": seguro(6, 1, 0, 1000)
    }

    niveis = {
        "tanque1": seguro(7, 1, 0, 100),
        "tanque2": seguro(8, 1, 0, 100)
    }

    tensoes = {
        "L1": seguro(9, 10, 100, 300),
        "L2": seguro(10, 10, 100, 300),
        "L3": seguro(11, 10, 100, 300)
    }

    correntes = {
        "L1": seguro(12, 10, 0, 100),
        "L2": seguro(13, 10, 0, 100),
        "L3": seguro(14, 10, 0, 100)
    }

    # Tratamento adicional para valores None nos status
    def status_seguro(idx):
        return registros[idx] if registros[idx] is not None else "inválido"

    status = {
        "geral": status_seguro(15),
        "alarme_temperatura": status_seguro(16),
        "contador_producao": status_seguro(17),
        "contador_falhas": status_seguro(18),
        "horas_funcionamento": status_seguro(19)
    }

    coils_data = {
        "ligado": coils[0] if len(coils) > 0 else "inválido",
        "em_alarme": coils[1] if len(coils) > 1 else "inválido",
        "manual": coils[2] if len(coils) > 2 else "inválido"
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

    # === Saída no terminal em formato JSON ===
    print("\n=== JSON GERADO ===\n")
    print(json.dumps(saida, indent=2, ensure_ascii=False))

    # === Salva o JSON em arquivo local ===
    with open("dados_modbus.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=2, ensure_ascii=False)

    return saida

if __name__ == "__main__":
    ler_dados_json()
