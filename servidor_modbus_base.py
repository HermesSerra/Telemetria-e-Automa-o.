#!/usr/bin/env python3

from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

class SimpleModbusServer:
    def __init__(self, host='localhost', port=502):
        self.host = host
        self.port = port
        
    def setup_data_blocks(self):
        # Holding Registers (endereços 40001-40020)
        holding_registers = [
            235, 452, 189,     # Temperaturas (x10)
            1250, 850,         # Pressões (x100)
            45, 23,            # Vazões (L/min)
            78, 92,            # Níveis (%)
            2201, 2198, 2203,  # Tensões (x10)
            152, 148, 155,     # Correntes (x10)
            1, 0,              # Status geral / alarme
            12547, 89, 1456    # Contador produção / falhas / horas
        ]
        
        # Coils (endereços 00001-00010)
        coils = [
            True, False, True, False, True,
            False, True, False, True, False
        ]
        
        # Blocos de dados Modbus
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [False] * 100),
            co=ModbusSequentialDataBlock(0, coils),
            hr=ModbusSequentialDataBlock(0, holding_registers),
            ir=ModbusSequentialDataBlock(0, [0] * 100)
        )
        return ModbusServerContext(slaves=store, single=True)

    def start_server(self):
        context = self.setup_data_blocks()

        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Teste Telemetria'
        identity.ProductCode = 'TT-SIMPLES'
        identity.ProductName = 'Servidor Teste Simples'
        identity.ModelName = 'Simulator v1.0'

        print(f"\nServidor Modbus TCP rodando em {self.host}:{self.port}")
        print("Use Ctrl+C para parar.")

        try:
            StartTcpServer(context=context, identity=identity, address=(self.host, self.port))
        except KeyboardInterrupt:
            print("\nServidor encerrado pelo usuário.")

def main():
    server = SimpleModbusServer()
    server.start_server()

if __name__ == "__main__":
    main()
