#!/usr/bin/env python3


from pymodbus.server import StartTcpServer  # pymodbus 3.x sintaxe
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
            # Temperaturas (valores * 10)
            235,    # 40001: Temperatura ambiente (23.5°C)
            452,    # 40002: Temperatura motor (45.2°C)
            189,    # 40003: Temperatura externa (18.9°C)
            
            # Pressões (valores * 100)
            1250,   # 40004: Pressão sistema (12.50 bar)
            850,    # 40005: Pressão linha (8.50 bar)
            
            # Vazões (valores diretos em L/min)
            45,     # 40006: Vazão principal
            23,     # 40007: Vazão secundária
            
            # Níveis (valores em %)
            78,     # 40008: Nível tanque 1
            92,     # 40009: Nível tanque 2
            
            # Tensões (valores * 10)
            2201,   # 40010: Tensão L1 (220.1V)
            2198,   # 40011: Tensão L2 (219.8V)
            2203,   # 40012: Tensão L3 (220.3V)
            
            # Correntes (valores * 10)
            152,    # 40013: Corrente L1 (15.2A)
            148,    # 40014: Corrente L2 (14.8A)
            155,    # 40015: Corrente L3 (15.5A)
            
            # Status e contadores
            1,      # 40016: Status geral (0=OK, 1=Alarme, 2=Falha)
            0,      # 40017: Alarme temperatura (0=OK, 1=Ativo)
            12547,  # 40018: Contador produção
            89,     # 40019: Contador falhas
            1456    # 40020: Horas funcionamento
        ]
        
        # Coils (endereços 00001-00010)
        coils = [
            True,   # 00001: Bomba principal
            False,  # 00002: Bomba reserva
            True,   # 00003: Válvula entrada
            False,  # 00004: Válvula saída
            True,   # 00005: Sistema automático
            False,  # 00006: Modo manual
            True,   # 00007: Alarme ativo
            False,  # 00008: Manutenção
            True,   # 00009: Sensor presença
            False   # 00010: Porta aberta
        ]
        
        # Criar blocos de dados
        store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [False] * 100),
            co=ModbusSequentialDataBlock(0, coils),
            hr=ModbusSequentialDataBlock(0, holding_registers),
            ir=ModbusSequentialDataBlock(0, [0] * 100)
        )
        
        return ModbusServerContext(slaves=store, single=True)
    
    def start_server(self):
        """Inicia o servidor Modbus TCP"""
        context = self.setup_data_blocks()
        
        # Identificação do dispositivo
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Teste Telemetria'
        identity.ProductCode = 'TT-SIMPLES'
        identity.ProductName = 'Servidor Teste Simples'
        identity.ModelName = 'Simulator v1.0'
        
        print(f"Servidor Modbus TCP iniciado em {self.host}:{self.port}")
        print("\n" + "="*50)
        print("DADOS DISPONÍVEIS NO SERVIDOR:")
        print("="*50)
        print("HOLDING REGISTERS (40001-40020):")
        print("  40001: Temperatura ambiente (235 = 23.5°C)")
        print("  40002: Temperatura motor (452 = 45.2°C)")
        print("  40003: Temperatura externa (189 = 18.9°C)")
        print("  40004: Pressão sistema (1250 = 12.50 bar)")
        print("  40005: Pressão linha (850 = 8.50 bar)")
        print("  40006: Vazão principal (45 L/min)")
        print("  40007: Vazão secundária (23 L/min)")
        print("  40008: Nível tanque 1 (78%)")
        print("  40009: Nível tanque 2 (92%)")
        print("  40010: Tensão L1 (2201 = 220.1V)")
        print("  40011: Tensão L2 (2198 = 219.8V)")
        print("  40012: Tensão L3 (2203 = 220.3V)")
        print("  40013: Corrente L1 (152 = 15.2A)")
        print("  40014: Corrente L2 (148 = 14.8A)")
        print("  40015: Corrente L3 (155 = 15.5A)")
        print("  40016: Status geral (1 = Alarme)")
        print("  40017: Alarme temperatura (0 = OK)")
        print("  40018: Contador produção (12547)")
        print("  40019: Contador falhas (89)")
        print("  40020: Horas funcionamento (1456)")
        print("\nCOILS (00001-00010):")
        print("  00001: Bomba principal (True)")
        print("  00002: Bomba reserva (False)")
        print("  00003: Válvula entrada (True)")
        print("  00004: Válvula saída (False)")
        print("  00005: Sistema automático (True)")
        print("  00006: Modo manual (False)")
        print("  00007: Alarme ativo (True)")
        print("  00008: Manutenção (False)")
        print("  00009: Sensor presença (True)")
        print("  00010: Porta aberta (False)")
        print("\n" + "="*50)
        print("Para parar o servidor, pressione Ctrl+C")
        print("="*50)
        
        try:
            StartTcpServer(
                context=context,
                identity=identity,
                address=(self.host, self.port)
            )
        except KeyboardInterrupt:
            print("\nServidor interrompido pelo usuário")

def main():
    server = SimpleModbusServer()
    server.start_server()

if __name__ == "__main__":
    main()