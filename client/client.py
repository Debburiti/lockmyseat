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
            print(f"🎬 Conectado ao servidor {self.host}:{self.port}")
            print("=" * 60)
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def send_command(self, command):
        """Envia comando e recebe resposta"""
        try:
            self.socket.send(command.encode('utf-8'))
            response = self.socket.recv(4096).decode('utf-8')
            return response
        except Exception as e:
            print(f"❌ Erro na comunicação: {e}")
            return None
    
    def show_menu(self):
        """Exibe menu de opções"""
        print("\n" + "=" * 60)
        print("🎬 SISTEMA DE RESERVAS - CINEMA")
        print("=" * 60)
        print("1. Listar sessões disponíveis")
        print("2. Ver assentos de uma sessão")
        print("3. Reservar assento")
        print("4. Sair")
        print("=" * 60)
    
    def run(self):
        """Loop principal do cliente"""
        if not self.connect():
            return
        
        try:
            while True:
                self.show_menu()
                choice = input("\nEscolha uma opção: ").strip()
                
                if choice == '1':
                    self.listar_sessoes()
                
                elif choice == '2':
                    self.listar_assentos()
                
                elif choice == '3':
                    self.reservar_assento()
                
                elif choice == '4':
                    print("\n👋 Encerrando conexão...")
                    break
                
                else:
                    print("❌ Opção inválida!")
                
                input("\nPressione ENTER para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Conexão interrompida pelo usuário")
        finally:
            self.socket.close()
            print("✅ Desconectado do servidor")
    
    def listar_sessoes(self):
        """Lista todas as sessões"""
        print("\n📋 Consultando sessões...")
        response = self.send_command("LISTAR_SESSOES")
        if response:
            print("\n" + response)
    
    def listar_assentos(self):
        """Lista assentos de uma sessão"""
        sessao_id = input("\n🎟️  Digite o ID da sessão: ").strip()
        if not sessao_id:
            print("❌ ID inválido")
            return
        
        print(f"\n📋 Consultando assentos da sessão {sessao_id}...")
        response = self.send_command(f"LISTAR_ASSENTOS {sessao_id}")
        if response:
            print("\n" + response)
    
    def reservar_assento(self):
        """Reserva um assento"""
        print("\n🎟️  RESERVAR ASSENTO")
        print("-" * 60)
        sessao_id = input("Digite o ID da sessão: ").strip()
        assento = input("Digite o assento (ex: A5): ").strip().upper()
        
        if not sessao_id or not assento:
            print("❌ Dados inválidos")
            return
        
        print(f"\n⏳ Tentando reservar assento {assento}...")
        response = self.send_command(f"RESERVAR {sessao_id} {assento}")
        
        if response:
            print("\n" + response)

if __name__ == "__main__":
    # Permite passar host e porta como argumentos
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
    
    client = CinemaClient(host, port)
    client.run()
