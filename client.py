import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  #s.connect(("169.254.92.100", 50002))
  s.connect(("localhost", 50002))
  print(s)
  #s.sendall(b"Ola, mundo")
  dados = s.recv(1024)
  print(f"{dados.decode()}")
  cod = input(' ')
  s.sendall(bytes(cod, encoding='utf-8'))
  dados = s.recv(1024)
  print(f"{dados.decode()}")

  