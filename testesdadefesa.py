# print(f"Thread entrou no banco: {threading.current_thread().name}") PARA TESTAR DENTRO DOS PROCESSOS SE ESTÃO ENTRANDO NO BANCO DE DADOS OU NÃO

from multiprocessing import Process, Pipe
from cliente import Requisicao
from server import Server
import time


def iniciar_servidor(conn_req, conn_resp):
    servidor = Server()
    servidor.exec(conn_req, conn_resp)


if __name__ == "__main__":
    conn_req_cliente, conn_req_servidor = Pipe()
    conn_resp_cliente, conn_resp_servidor = Pipe()

    processo_servidor = Process(
        target=iniciar_servidor,
        args=(conn_req_servidor, conn_resp_servidor)
    )
    processo_servidor.start()

    inicio = time.time()

    for i in range(1, 21):
        conn_req_cliente.send(Requisicao("insert", i, f"Nome {i}").to_dict())

    for i in range(1, 21):
        print(conn_resp_cliente.recv())

    fim = time.time()

    conn_req_cliente.send("sair")
    processo_servidor.join()

    print(f"\nTempo total: {fim - inicio:.4f} segundos")