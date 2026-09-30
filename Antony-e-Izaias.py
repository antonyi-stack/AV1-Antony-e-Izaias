from __future__ import annotations
from datetime import date

class ErroDeMedicamento(Exception):
	pass

class QuantidadeInvalidaError(Exception): 
	pass

class MedicamentoVencidoError(Exception): 
	pass

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
		partes = texto.split(";")
		nome = partes[0]
		lote = partes[1]
		validade = date.fromisoformat(partes[2])
		quantidade = int(partes[3])
		valor = float(partes[4])
		
		return cls(nome, lote, validade, quantidade, valor)
		
		# nome, lote, validade, quantidade, valor = texto.split(";")
		# d, m, a = validade.split("-")
		# return cls(nome, lote, date(int[d], int[m], date[a]), int(quantidade), float(valor))

	@staticmethod
	def dias_para_vencer(validade: date) -> int:
		hoje = date.today()
		return (validade - hoje).days
	
	def __str__(self) -> str: 
		validade_formatada = self.validade.strftime ("%d/%m/%Y")
		return f"{self.nome} ({self.lote}) - {self.quantidade} un. - val. {validade_formatada}"

	def __repr__(self) -> str: 
			return(f"Medicamento(nome={self.nome!r}, lote={self.lote!r}," 
		f"validade={self.validade!r}, quantidade={self.quantidade!r}, valor={self.valor!r})"
		)

	def __eq__(self, outro: object) -> bool:
		if not isinstance(outro, Medicamento):
			return NotImplemented
		return self.nome.lower() == outro.nome.lower() and self.lote == outro.lote

	def __lt__(self, outro: Medicamento) -> bool:
		if not isinstance(outro, Medicamento):
			return NotImplemented 
		return self.validade < outro.validade

	def dispensar (self, quantidade: int) -> None:
			if quantidade <= 0 or quantidade > self.quantidade:
				raise QuantidadeInvalidaError(quantidade)
			if self.validade < date.today():
				raise MedicamentoVencidoError(self.validade)
			self.quantidade -= quantidade

	def repor(self, quantidade: int) -> None:
			self.quantidade += quantidade


if __name__ == "__main__":
	m1 = Medicamento("Dipirona 500mg", "L2026A", date(2026, 12, 31), 100, 12.50)
	m2 = Medicamento.de_registro("Amoxicilina 500mg;L2026B;2026-10-15;40;18.90")
	print(f"Dados de m1: {m1}") # ex.: Dipirona 500mg (L2026A) - 100 un. - val. 31/12/2026
	print(f"Dados de m2: {m2}") # ex.: Amoxicilina 500mg (L2026B) - 40 un. - val. 15/10/2026
	print(f"Dias para vencer de m2: {Medicamento.dias_para_vencer(m2.validade)}")
	print("Dispensando 20 medicamentos de m1")
	m1.dispensar(20)
	print(f"Quantidade de m1: {m1.quantidade}")

	try:
		m2.dispensar(999)
	except QuantidadeInvalidaError as erro:
		print(f"Erro esperado: {erro}")

	vencido = Medicamento("Soro Fisiológico", "L2025X", date(2025, 1, 10), 10, 5.0)
	try:
		vencido.dispensar(1)
	except MedicamentoVencidoError as erro:
		print(f"Erro esperado: {erro}")

	outro = Medicamento("Dipirona 500mg", "L2026A", date(2026, 1, 1), 0, 1.0)
	print(f"m1 é igual a outro? {m1 == outro}")

	estoque = [m1, m2, vencido, outro]
	print("Exibindo lista ordenada por data (mais antigos primeiro): ")
	for lote in sorted(estoque):
		print(lote)

	try:
		m1.quantidade = -5
	except ValueError as erro:
		print(f"Erro esperado: {erro} é inválido")
