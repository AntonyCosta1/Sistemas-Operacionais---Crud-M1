class Requisicao:
    def __init__(self, operacao, id_registro=None, nome=None):
        self.operacao = operacao.lower()
        self.id = id_registro
        self.nome = nome

    def to_dict(self):
        return {
            "operacao": self.operacao,
            "id": self.id,
            "nome": self.nome
        }