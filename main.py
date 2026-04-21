from multiprocessing import Process, Pipe
from cliente import requisicao
from server import Server

def iniciar_servidor(conn):
    servidor = Server()
    servidor.exec(conn)

def menu_cliente(conn):
    while True:
        print("\nMenu")
        print("1 - insert")
        print("2 - delete")
        print("3 - update")
        print("4 - select")
        print("5 - mostrar o banco")
        print("7 - sair")

        op = input("Escolha uma opção: \n").strip()

        if op == "1":
            try:
                id = int(input("digite o id: "))
                nome = input("digite o nome: ")
                req = requisicao("insert", id, nome)
                conn.send(req.to_dict())
            except ValueError:
                print("ID invalido, digite um numero inteiro!")

        elif op =="2":
            try:
                id = int(input("digite o id: "))
                
                req = requisicao("delete", id)
                conn.send(req.to_dict())
            except ValueError:
                print("ID invalido, digite um numero inteiro!")

        elif op =="3":
            try:
                id = int(input("digite o id: "))
                nome = input("digite o novo nome: ")
                req = requisicao("update", id, nome)
                conn.send(req.to_dict())
            except ValueError:
                print("ID invalido, digite um numero inteiro!")

        elif op =="4":
            try:
                id = int(input("digite o id: "))
                req = requisicao("select", id)
                conn.send(req.to_dict())
            except ValueError:
                print("ID invalido, digite um numero inteiro!")

        elif op == "5":
            try:
                with open("banco.json", "r", encoding="utf-8") as f:
                    print("Segue conteudo:")
                    print(f.read())
            except FileNotFoundError:
                    print("Banco não existe")

        elif op =="7":
            conn.send("sair")
            print("Encerrando servidor")
            break

        else:
            print("Opção invalida, tente denovo")


if __name__ == "__main__":
    conn_cliente, conn_servidor = Pipe()

    processo_servidor = Process(target=iniciar_servidor, args=(conn_servidor,))
    processo_servidor.start()

    menu_cliente(conn_cliente)
    processo_servidor.join()

    print("Cliente encerrado.")