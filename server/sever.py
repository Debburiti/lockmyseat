import socket
import threading
import json
from datetime import datetime

class CinemaServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None

        self.lock = threading.Lock()

        self.sessoes = {
            '1': {
                'filme': 'Harry Potter e a Pedra Filosofal',
                'horario': '19:00',
                'sala': 'A1',
                'assentos': self._criar_assentos(5, 8)
            },
            '2': {
                'filme': 'Quarteto Fantástico: Primeiros Passos',
                'horario': '21:00',
                'sala': 'A2',
                'assentos': self._criar_assentos(5, 8)
            },
            '3': {
                'filme': 'Planeta dos Macacos: O Reinado',
                'horario': '18:30',
                'sala': 'B1',
                'assentos': self._criar_assentos(6, 10)
            },
            
            '4': {
                'filme': 'O Auto da Compadecida',
                'horario': '18:00',
                'sala': 'B2',
                'assentos': self._criar_assentos(6, 10)
            },
            
            '4': {
                'filme': 'Peter Pan',
                'horario': '17:00',
                'sala': 'C1',
                'assentos': self._criar_assentos(4, 8)
            },
            '5': {
                'filme': 'Bacurau',
                'horario': '19:45',
                'sala': 'C2',
                'assentos': self._criar_assentos(6, 10)
            }
        }

        self.cliente_count = 0
        
    def _criar_assentos(self, fileiras, colunas):
        """Cria matriz de assentos (False = livre, True = ocupado)"""
        assentos = {}
        for i in range(fileiras):
            letra = chr(65 + i) 
            for j in range(1, colunas + 1):
                assento_id = f"{letra}{j}"
                assentos[assento_id] = False
        return assentos
    
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"Servidor de Cinema iniciado em {self.host}:{self.port}")
        print(f"{datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                self.cliente_count += 1
                client_id = self.cliente_count
                
                print(f"\n Cliente #{client_id} conectado: {address}")

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_id, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n\n Servidor encerrado pelo usuário")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, client_id, address):
        print(f"Thread iniciada para Cliente #{client_id}")
        
        try:
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                
                if not data:
                    break
                
                print(f"\nCliente #{client_id}: {data}")

                response = self.process_command(data, client_id)

                client_socket.send(response.encode('utf-8'))
                
        except Exception as e:
            print(f"Erro com Cliente #{client_id}: {e}")
        finally:
            client_socket.close()
            print(f"\nCliente #{client_id} desconectado: {address}")
    
    def process_command(self, command, client_id):
        parts = command.strip().split()
        
        if not parts:
            return "ERRO: Comando vazio"
        
        cmd = parts[0].upper()
        
        if cmd == "LISTAR_SESSOES":
            return self.listar_sessoes()
        
        elif cmd == "LISTAR_ASSENTOS":
            if len(parts) < 2:
                return "ERRO: Sessão não especificada"
            sessao_id = parts[1]
            return self.listar_assentos(sessao_id, client_id)
        
        elif cmd == "RESERVAR":
            if len(parts) < 3:
                return "ERRO: Formato: RESERVAR <sessao_id> <assento>"
            sessao_id = parts[1]
            assento = parts[2].upper()
            return self.reservar_assento(sessao_id, assento, client_id)
        
        else:
            return "ERRO: Comando desconhecido"
    
    def listar_sessoes(self):
        resultado = "SESSOES\n"
        resultado += "=" * 60 + "\n"
        
        for sessao_id, info in self.sessoes.items():
            total = len(info['assentos'])
            ocupados = sum(1 for ocupado in info['assentos'].values() if ocupado)
            disponiveis = total - ocupados
            
            resultado += f"ID: {sessao_id}\n"
            resultado += f"Filme: {info['filme']}\n"
            resultado += f"Horário: {info['horario']}\n"
            resultado += f"Sala: {info['sala']}\n"
            resultado += f"Assentos: {disponiveis}/{total} disponíveis\n"
            resultado += "-" * 60 + "\n"
        
        return resultado
    
    def listar_assentos(self, sessao_id, client_id):
        """Lista assentos de uma sessão específica"""
        if sessao_id not in self.sessoes:
            return "ERRO: Sessão não encontrada"
        
        sessao = self.sessoes[sessao_id]
        resultado = f"ASSENTOS - {sessao['filme']} ({sessao['horario']})\n"
        resultado += "=" * 60 + "\n"
        resultado += "🟢 = Livre | 🔴 = Ocupado\n\n"

        assentos_por_fileira = {}
        for assento_id, ocupado in sessao['assentos'].items():
            fileira = assento_id[0]
            if fileira not in assentos_por_fileira:
                assentos_por_fileira[fileira] = []
            assentos_por_fileira[fileira].append((assento_id, ocupado))

        resultado += "    "
        num_colunas = len(assentos_por_fileira[list(assentos_por_fileira.keys())[0]])
        for i in range(1, num_colunas + 1):
            resultado += f"{i:3}"
        resultado += "\n"
        
        for fileira in sorted(assentos_por_fileira.keys()):
            resultado += f"{fileira}   "
            for assento_id, ocupado in sorted(assentos_por_fileira[fileira]):
                simbolo = "🔴" if ocupado else "🟢"
                resultado += f"{simbolo} "
            resultado += "\n"
        
        print(f"Cliente #{client_id} consultou assentos da sessão {sessao_id}")
        return resultado
    
    def reservar_assento(self, sessao_id, assento, client_id):
        with self.lock:
            if sessao_id not in self.sessoes:
                return "ERRO: Sessão não encontrada"
            
            sessao = self.sessoes[sessao_id]
            
            if assento not in sessao['assentos']:
                return f"ERRO: Assento {assento} não existe"
            
            if sessao['assentos'][assento]:
                print(f" Cliente #{client_id} tentou reservar {assento} (OCUPADO)")
                return f"INDISPONIVEL: Assento {assento} já está ocupado"

            sessao['assentos'][assento] = True
            
            print(f" Cliente #{client_id} reservou: Sessão {sessao_id}, Assento {assento}")
            return f"OK: Assento {assento} reservado com sucesso!\nFilme: {sessao['filme']}\nHorário: {sessao['horario']}\nSala: {sessao['sala']}"

if __name__ == "__main__":
    server = CinemaServer()
    server.start()
