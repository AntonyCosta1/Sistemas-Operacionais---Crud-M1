import threading
from banco import Banco
from datetime import datetime

class Server:
    def __init__(self):
        self.banco = Banco()
        self.threads = []
        self.lock_log = threading.Lock()

    def registrar_log(self, mensagem):
        with self.lock_log:
            with open("log.txt", "a", encoding="utf-8") as f:
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                nome_thread = threading.current_thread().name
                f.write(f"[{agora}] [{nome_thread}] {mensagem}\n")

    def processar_requisicao(self, requisicao):
        operacao = requisicao.get("operacao")
        id_registro =  requisicao.get("id")
        nome = requisicao.get("nome")

        if operacao == "insert":
            if id_registro is None or nome is None or nome.strip() == "":
                resultado = "ERRO NO INSERT, PRECISA INSERIR ID E NOME"
            else:
                resultado = self.banco.insert(id_registro, nome)

        elif operacao == "delete":
            if id_registro is None:
                resultado = "ERRO NO DELTE, PRECISA INSERIR ID"
            else:
                resultado = self.banco.delete(id_registro)

        elif operacao == "select":
            if id_registro is None:
                resultado = "ERRO NO SELECT, PRECISA INSERIR ID"
            else:
                resultado = self.banco.select(id_registro)

        elif operacao == "update":
            if id_registro is None or nome is None or nome.strip() == "":
                resultado = "ERRO NO update, PRECISA INSERIR ID E NOME"
            else:
                resultado = self.banco.update(id_registro, nome)

        else:
            resultado = "[ERRO] Operação inválida"

        print(resultado)
        self.registrar_log(resultado)

    def exec(self, conn):
        print("Servidor iniciado...")

        while True:
            req = conn.recv()

            if req == "sair":
                break

            t = threading.Thread(target=self.processar_requisicao, args=(req,))
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        self.registrar_log("Servidor")
        print("Servidor encerrado.")