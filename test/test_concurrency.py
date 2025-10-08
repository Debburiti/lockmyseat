# test_concurrency.py
import socket
import threading
import time

def cliente_simulado(cliente_id, sessao_id, assento, delay=0):
    """Simula um cliente tentando reservar um assento"""
    try:
        # Conecta ao servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5555))
        
        print(f"🔵 Cliente {cliente_id} conectado")
        
        # Aguarda um pouco (simulando tempo de navegação)
        time.sleep(delay)
        
        # Tenta reservar o assento
        comando = f"RESERVAR {sessao_id} {assento}"
        print(f"📤 Cliente {cliente_id} enviando: {comando}")
        
        sock.send(comando.encode('utf-8'))
        response = sock.recv(4096).decode('utf-8')
        
        print(f"\n{'='*60}")
        print(f"📥 RESPOSTA para Cliente {cliente_id}:")
        print(response)
        print(f"{'='*60}\n")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Erro no Cliente {cliente_id}: {e}")

def teste_corrida():
    """
    Teste de condição de corrida:
    Dois clientes tentam reservar o mesmo assento simultaneamente
    """
    print("\n" + "="*60)
    print("🧪 TESTE DE CONDIÇÃO DE CORRIDA")
    print("="*60)
    print("Dois clientes tentarão reservar o mesmo assento (A1)")
    print("Apenas um deve conseguir!\n")
    
    # Cria duas threads que tentam reservar o mesmo assento
    thread1 = threading.Thread(target=cliente_simulado, args=(1, '1', 'A1', 0))
    thread2 = threading.Thread(target=cliente_simulado, args=(2, '1', 'A1', 0.1))
    
    # Inicia as threads quase simultaneamente
    thread1.start()
    thread2.start()
    
    # Aguarda conclusão
    thread1.join()
    thread2.join()
    
    print("\n✅ Teste concluído!")

def teste_multiplos_clientes():
    """
    Teste com múltiplos clientes reservando assentos diferentes
    """
    print("\n" + "="*60)
    print("🧪 TESTE COM MÚLTIPLOS CLIENTES")
    print("="*60)
    print("5 clientes reservando assentos diferentes simultaneamente\n")
    
    assentos = ['A1', 'A2', 'B1', 'B2', 'C1']
    threads = []
    
    for i, assento in enumerate(assentos, 1):
        thread = threading.Thread(
            target=cliente_simulado,
            args=(i, '1', assento, i * 0.1)
        )
        threads.append(thread)
        thread.start()
    
    # Aguarda todas as threads
    for thread in threads:
        thread.join()
    
    print("\n✅ Teste concluído!")

def teste_consultas_simultaneas():
    """
    Teste de consultas simultâneas
    """
    def consultar_assentos(cliente_id, sessao_id):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 5555))
            
            comando = f"LISTAR_ASSENTOS {sessao_id}"
            print(f"📤 Cliente {cliente_id} consultando sessão {sessao_id}")
            
            sock.send(comando.encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            
            print(f"✅ Cliente {cliente_id} recebeu resposta")
            sock.close()
            
        except Exception as e:
            print(f"❌ Erro no Cliente {cliente_id}: {e}")
    
    print("\n" + "="*60)
    print("🧪 TESTE DE CONSULTAS SIMULTÂNEAS")
    print("="*60)
    print("3 clientes consultando assentos simultaneamente\n")
    
    threads = []
    for i in range(1, 4):
        thread = threading.Thread(target=consultar_assentos, args=(i, '1'))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    print("\n🎬 TESTES DE CONCORRÊNCIA - SISTEMA DE CINEMA")
    print("="*60)
    print("Certifique-se de que o servidor está rodando!")
    print("="*60)
    
    input("\nPressione ENTER para iniciar os testes...")
    
    # Executa os testes
    teste_corrida()
    time.sleep(2)
    
    teste_multiplos_clientes()
    time.sleep(2)
    
    teste_consultas_simultaneas()
    
    print("\n" + "="*60)
    print("🎉 TODOS OS TESTES CONCLUÍDOS!")
    print("="*60)