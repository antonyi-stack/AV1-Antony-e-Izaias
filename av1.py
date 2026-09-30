from __future__ import annotations
from datetime import date


class Medicamento:
	def __init__(self, nome: str, lote: str, validade: date, quantidade: int, valor: float) -> None:
		self.nome = nome
		self.lote = lote
		self.validade = validade
		self.quantidade = quantidade
		self.valor = valor

	@property
	def quantidade(self) -> int:
		return self._quantidade

	@quantidade.setter
	def quantidade(self, quantidade: int) -> None:
		if quantidade < 0:
			raise ValueError(quantidade)
		self._quantidade = quantidade

	@property
	def valor(self) -> float:
		return self._valor

	@valor.setter
	def valor(self, valor: float) -> None:
		if valor <= 0:
			raise ValueError(valor)
		self._valor = valor

	@classmethod
	def de_registro(cls, texto: str) -> Medicamento:
		# partes = texto.split(";")
		# nome = partes[0]
		# lote = partes[1]
		# validade = date(partes[2])
		# quantidade = int(partes[3])
		# valor = float(partes[4])
		
        # return cls(nome, lote, validade, quantidade, valor)
		
		nome, lote, validade, quantidade, valor = texto.split(";")
		d, m, a = validade.split("-")
		return cls(nome, lote, date(int[d], int[m], date[a]), int(quantidade), float(valor))

	@staticmethod
	def dias_para_vencer(validade: date) -> date:
		hoje = date.today()
		return (validade - hoje).days

