from multiprocessing import Process, Pipe
from cliente import Requisicao
from server import Server


def iniciar_servidor(conn_req, conn_resp):
    servidor = Server()
    servidor.exec(conn_req, conn_resp)


def mostrar_banco():
    try:
        with open("banco.json", "r", encoding="utf-8") as f:
            print("\nConteúdo atual do banco.json:")
            print(f.read())
    except FileNotFoundError:
        print("banco.json ainda não existe.")


def menu_cliente(conn_req, conn_resp):
    while True:
        print("\nMenu")
        print("1 - insert")
        print("2 - delete")
        print("3 - update")
        print("4 - select")
        print("5 - mostrar o banco")
        print("7 - sair")

        op = input("Escolha uma opção: ").strip()

        if op == "1":
            try:
                id_registro = int(input("digite o id: "))
                nome = input("digite o nome: ").strip()
                req = Requisicao("insert", id_registro, nome)
                conn_req.send(req.to_dict())
                print(conn_resp.recv())
            except ValueError:
                print("ID inválido.")

        elif op == "2":
            try:
                id_registro = int(input("digite o id: "))
                req = Requisicao("delete", id_registro)
                conn_req.send(req.to_dict())
                print(conn_resp.recv())
            except ValueError:
                print("ID inválido.")

        elif op == "3":
            try:
                id_registro = int(input("digite o id: "))
                nome = input("digite o novo nome: ").strip()
                req = Requisicao("update", id_registro, nome)
                conn_req.send(req.to_dict())
                print(conn_resp.recv())
            except ValueError:
                print("ID inválido.")

        elif op == "4":
            try:
                id_registro = int(input("digite o id: "))
                req = Requisicao("select", id_registro)
                conn_req.send(req.to_dict())
                print(conn_resp.recv())
            except ValueError:
                print("ID inválido.")

        elif op == "5":
            mostrar_banco()

        elif op == "7":
            conn_req.send("sair")
            print("Encerrando cliente...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    conn_req_cliente, conn_req_servidor = Pipe()
    conn_resp_cliente, conn_resp_servidor = Pipe()

    processo_servidor = Process(
        target=iniciar_servidor,
        args=(conn_req_servidor, conn_resp_servidor)
    )
    processo_servidor.start()

    print("Servidor iniciado...")
    menu_cliente(conn_req_cliente, conn_resp_cliente)

    processo_servidor.join()
    print("Cliente encerrado.")