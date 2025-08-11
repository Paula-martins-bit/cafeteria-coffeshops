class Cliente:
    _contador = 0

    """Método para gerar o identificador único"""
    @classmethod
    def obter_codigo(cls) -> int:
        cls._contador += 1
        return cls._contador

    def __init__(self, nome: str, sobrenome: str,  telefone: str):
        self.codigo = Cliente.obter_codigo()
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone

    def obter_dicionario(self):
        return {"codigo": self.codigo, "nome": self.nome, "sobrenome": self.sobrenome, "telefone": self.telefone}

    @classmethod
    def carregar_dados(cls, d: dict):
        cliente = cls(d["nome"], d["sobrenome"], d["telefone"])
        cliente.codigo = d["codigo"]

        return cliente