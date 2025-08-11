
class Produto:
    _contador = 0

    """Método para gerar o identificador único"""
    @classmethod
    def obter_codigo(cls) -> int:
        cls._contador += 1
        return cls._contador

    def __init__(self, nome: str, descricao: str, preco: float):
        self.codigo = Produto.obter_codigo()
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    def obter_dicionario(self):  # -> para JSON
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco}

    @classmethod
    def carregar_dados(cls, d: dict):
        produto = cls( d["nome"], d["descricao"], d["preco"])
        produto.codigo = d["codigo"]
        return produto