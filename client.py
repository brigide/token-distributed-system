import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  #s.connect(("169.254.92.100", 50002))
  s.connect(("localhost", 50002))
  print(s)
  cod = input(' ')
  #cod = '15000000&10000'
  s.sendall(bytes(cod, encoding='utf-8'))
  dados = s.recv(1024)
  print(f"{dados.decode()}")

  s.sendall(bytes('/end', encoding='utf-8'))
  s.close()


  