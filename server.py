import threading
from datetime import datetime
from banco import Banco


class Server:
    def __init__(self):
        self.banco = Banco()
        self.threads = []
        self.lock_log = threading.Lock()
        self.lock_resposta = threading.Lock()

    def registrar_log(self, mensagem):
        with self.lock_log:
            with open("log.txt", "a", encoding="utf-8") as f:
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                nome_thread = threading.current_thread().name
                f.write(f"[{agora}] [{nome_thread}] {mensagem}\n")

    def processar_requisicao(self, requisicao, conn_resposta):
        operacao = requisicao.get("operacao")
        id_registro = requisicao.get("id")
        nome = requisicao.get("nome")

        if operacao == "insert":
            if id_registro is None or nome is None or nome.strip() == "":
                resultado = "[ERRO] INSERT precisa de id e nome"
            else:
                resultado = self.banco.insert(id_registro, nome)

        elif operacao == "delete":
            if id_registro is None:
                resultado = "[ERRO] DELETE precisa de id"
            else:
                resultado = self.banco.delete(id_registro)

        elif operacao == "update":
            if id_registro is None or nome is None or nome.strip() == "":
                resultado = "[ERRO] UPDATE precisa de id e nome"
            else:
                resultado = self.banco.update(id_registro, nome)

        elif operacao == "select":
            if id_registro is None:
                resultado = "[ERRO] SELECT precisa de id"
            else:
                resultado = self.banco.select(id_registro)

        else:
            resultado = "[ERRO] Operação inválida"

        self.registrar_log(resultado)

        with self.lock_resposta:
            conn_resposta.send(resultado)

    def exec(self, conn_requisicao, conn_resposta):
        self.registrar_log("Servidor iniciado")

        while True:
            req = conn_requisicao.recv()

            if req == "sair":
                break

            t = threading.Thread(
                target=self.processar_requisicao,
                args=(req, conn_resposta)
            )
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        self.registrar_log("Servidor encerrado")