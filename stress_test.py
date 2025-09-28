import threading
from client import ChatClient
import time
from itertools import product

# Parâmetros de stress test
THREAD_OPTIONS = [10, 100, 500]
CONNECTION_OPTIONS = [10, 100, 500]
PACKET_OPTIONS = [10, 100, 1000]
SIZE_OPTIONS = [100, 1024, 10240] 

def run_stress_test(num_clients, msgs_per_client, msg_size):
    threads = []
    msg = "x" * msg_size
    response_times = {f"User{i}": [] for i in range(num_clients)}

    def client_behavior(name):
        try:
            client = ChatClient(name)
            time.sleep(1)  
            for i in range(msgs_per_client):
                start = time.time()
                client.send(msg)
                end = time.time()
                duration = end - start
                response_times[name].append(duration)
        except Exception as e:
            print(f"[ERRO] {name}: {e}")

    start_time = time.time()

    for i in range(num_clients):
        t = threading.Thread(target=client_behavior, args=(f"User{i}",))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    total_time = end_time - start_time

    total_msgs = sum(len(times) for times in response_times.values())
    total_duration = sum(sum(times) for times in response_times.values())
    avg_time = total_duration / total_msgs if total_msgs else 0

    return {
        "conexões": num_clients,
        "pacotes": msgs_per_client,
        "tamanho_pacote": msg_size,
        "tempo_total": total_time,
        "media_resposta": avg_time,
        "mensagens_enviadas": total_msgs
    }

def main():
    print("Iniciando Stress Test com múltiplas configurações...\n")
    resultados = []

    for threads_no_servidor, conexoes, pacotes, tamanho in product(
        THREAD_OPTIONS, CONNECTION_OPTIONS, PACKET_OPTIONS, SIZE_OPTIONS
    ):
        print(f"Testando: Threads={threads_no_servidor} | Conexões={conexoes} | Pacotes={pacotes} | Tamanho={tamanho} bytes")
        resultado = run_stress_test(
            num_clients=conexoes,
            msgs_per_client=pacotes,
            msg_size=tamanho
        )
        resultado["threads"] = threads_no_servidor
        resultados.append(resultado)

        print(f" -> Tempo total: {resultado['tempo_total']:.2f}s | Média por mensagem: {resultado['media_resposta']:.4f}s\n")

    print("\n=== RESULTADOS DO STRESS TEST ===")
    print(f"{'Threads':<10}{'Conexões':<12}{'Pacotes':<10}{'Tam(Bytes)':<12}{'Total(s)':<10}{'Média(s)':<10}")
    for r in resultados:
        print(f"{r['threads']:<10}{r['conexões']:<12}{r['pacotes']:<10}{r['tamanho_pacote']:<12}{r['tempo_total']:<10.2f}{r['media_resposta']:<10.4f}")

if __name__ == "__main__":
    main()
