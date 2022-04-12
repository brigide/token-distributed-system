import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('169.254.92.100', 50002))
  print(s)
  s.listen()
  conexao, addr = s.accept()
  with conexao:
    print(f"Cliente conectado: {addr}")
    while True:
      dados = conexao.recv(1024)
      if not dados:
        break
      print(f"Mensagem recebida: {dados.decode()}")
      conexao.sendall(b"OBRIGADO. Desconectando")