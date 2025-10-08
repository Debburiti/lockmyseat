import socket
import sys

class CinemaClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Conecta ao servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Conectado ao servidor {self.host}:{self.port}")
            return True
        except Exception as e:
            print("Erro ao conectar ao servidor:", e)
            return False
    
    def send_command(self, command):
        """Envia comando e recebe resposta do servidor"""
        try:
            self.socket.send(command.encode())
            data = self.socket.recv(4096)
            return data.decode()
        except Exception as e:
            print("Erro na comunicação com o servidor:", e)
            return None

    def show_menu(self):
        print("\n" + "=" * 50)
        print("SISTEMA DE RESERVAS - CINEMA")
        print("=" * 50)
        print("1. Listar sessões")
        print("2. Ver assentos de uma sessão")
        print("3. Reservar assento")
        print("4. Sair")
        print("=" * 50)

    def listar_sessoes(self):
        print("\nListando sessões disponíveis...")
        resposta = self.send_command("LISTAR_SESSOES")
        if resposta:
            print(resposta)

    def listar_assentos(self):
        sessao_id = input("Digite o ID da sessão: ").strip()
        if not sessao_id:
            print("ID inválido.")
            return
        print(f"Consultando assentos da sessão {sessao_id}...")
        resposta = self.send_command(f"LISTAR_ASSENTOS {sessao_id}")
        if resposta:
            print(resposta)

    def reservar_assento(self):
        print("\nReserva de assento")
        sessao_id = input("ID da sessão: ").strip()
        assento = input("Assento (ex: A5): ").strip().upper()

        if not sessao_id or not assento:
            print("Dados inválidos.")
            return

        print(f"Tentando reservar o assento {assento}...")
        resposta = self.send_command(f"RESERVAR {sessao_id} {assento}")
        if resposta:
            print(resposta)

    def run(self):
        if not self.connect():
            return

        try:
            while True:
                self.show_menu()
                opcao = input("Escolha uma opção: ").strip()

                if opcao == '1':
                    self.listar_sessoes()
                elif opcao == '2':
                    self.listar_assentos()
                elif opcao == '3':
                    self.reservar_assento()
                elif opcao == '4':
                    print("Encerrando conexão...")
                    break
                else:
                    print("Opção inválida.")

                input("\nPressione ENTER para continuar...")

        except KeyboardInterrupt:
            print("\nConexão encerrada pelo usuário.")
        finally:
            self.socket.close()
            print("Desconectado do servidor.")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555

    client = CinemaClient(host, port)
    client.run()
