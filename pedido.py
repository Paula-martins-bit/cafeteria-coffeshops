from datetime import datetime
from optparse import Option
from typing import List
from produto import Produto

class Pedido:
    _contador = 0

    """Método para gerar o identificador único"""
    @classmethod
    def obter_codigo(cls) -> int:
        cls._contador += 1
        return cls._contador

    def __init__(self, itens: List[int], cliente_telefone: str):
        self.codigo = Pedido.obter_codigo()
        self.itens: List[int] = list(itens)
        self.cliente_telefone: str = cliente_telefone
        self.data_criacao: datetime = datetime.today()
        self.data_finalizacao: Option[datetime] = None
        self.status = 'criado'

    """Atualiza o status do pedido"""
    def atualizar(self, status):
        self.status = status

    """Cancela o pedido"""
    def cancelar(self):
        self.status = 'cancelado'

    """Finaliza o pedido"""
    def finalizar(self):
        self.status = 'finalizado'
        self.data_finalizacao = datetime.today()

    """Calcula o total do pedido com base no preco dos produtos"""
    def total(self, produtos: List[Produto]) -> float:
        return sum(p.preco for p in produtos if p.id in self.itens)

    def obter_dicionario(self):  # -> para JSON
        return {
            "codigo": self.codigo,
            "itens": self.itens,
            "cliente_telefone": self.cliente_telefone,
            "data_criacao": self.data_criacao.isoformat(),
            "status": self.status,
            "data_finalizacao": (self.data_finalizacao.isoformat() if self.data_finalizacao else None)
        }

    @classmethod
    def carregar_dados(cls, d: dict):
        pedido = cls(d["itens"], d["cliente_telefone"])
        pedido.codigo = d["codigo"]
        pedido.status = d["status"]
        pedido.data_criacao = datetime.fromisoformat(d["data_criacao"])
        pedido.data_finalizacao = (
            datetime.fromisoformat(d["data_finalizacao"]) if d["data_finalizacao"] else None
        )
        return pedido