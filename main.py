from servidor_modbus_base import SimpleModbusServer
server = SimpleModbusServer('localhost', 502)
server.start_server()