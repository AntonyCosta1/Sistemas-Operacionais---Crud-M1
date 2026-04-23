import threading
import json
import os


class Reg:
    def __init__(self, id_registro, nome):
        self.id = id_registro
        self.nome = nome

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome
        }


class Banco:
    def __init__(self, arquivo="banco.json"):
        self.arquivo = arquivo
        self.registros = []
        self.lock = threading.Lock()
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    self.registros = [Reg(item["id"], item["nome"]) for item in dados]
            except (json.JSONDecodeError, FileNotFoundError):
                self.registros = []
        else:
            self.salvar()

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(
                [registro.to_dict() for registro in self.registros],
                f,
                indent=4,
                ensure_ascii=False
            )

    def insert(self, id_registro, nome):
        with self.lock:
            for reg in self.registros:
                if reg.id == id_registro:
                    return f"[INSERT] O id {id_registro} já está no banco"

            self.registros.append(Reg(id_registro, nome))
            self.salvar()
            return f"[INSERT] ID {id_registro} inserido com sucesso - nome: {nome}"

    def delete(self, id_registro):
        with self.lock:
            for reg in self.registros:
                if reg.id == id_registro:
                    self.registros.remove(reg)
                    self.salvar()
                    return f"[DELETE] ID {id_registro} deletado com sucesso"

            return f"[DELETE] O id {id_registro} não foi encontrado no banco"

    def select(self, id_registro):
        with self.lock:
            for reg in self.registros:
                if reg.id == id_registro:
                    return f"[SELECT] ID: {reg.id} - Nome: {reg.nome}"

            return f"[SELECT] O id {id_registro} não foi encontrado no banco"

    def update(self, id_registro, nome):
        with self.lock:
            for reg in self.registros:
                if reg.id == id_registro:
                    reg.nome = nome
                    self.salvar()
                    return f"[UPDATE] ID {id_registro} atualizado com sucesso - nome: {nome}"

            return f"[UPDATE] O id {id_registro} não foi encontrado no banco"