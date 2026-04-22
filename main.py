# ESTRUTURAS
class Peca:
  def __init__(self, id, peso, cor, comprimento, status, motivos):
    self.id = id
    self.peso = peso
    self.cor = cor
    self.comprimento = comprimento
    self.status = status
    self.motivos = motivos # lista

class Caixa:
  def __init__(self, numero, pecas, total_pecas, status):
    self.numero = numero
    self.pecas = pecas # lista
    self.total_pecas = total_pecas
    self.status = status

# VARIÁVEIS GLOBAIS
lista_aprovadas = []
lista_reprovadas = []
lista_caixas = []

contador_id = 1
contador_caixas = 1

caixa_atual = Caixa (
  numero = 1, 
  pecas = [], 
  total_pecas = 0, 
  status = "aberta"
  )

# FUNÇÔES

# função gerar id
def gerar_id():
  global contador_id

  id = contador_id
  contador_id = contador_id + 1
  return id

# função coletar dados
def coletar_dados():

  # coletar peso
  while True:
    entrada = input('Digite o peso (g): ')
    if not entrada.isnumeric():
      print('Erro: Digite um número.')
    elif float(entrada) <= 0:
      print('Erro: Valor deve ser positivo.')
    else:
      peso = float(entrada)
      break

  # coletar cor
  while True:
    entrada = input('Digite a cor: ')
    if entrada == "":
      print('Erro: cor não reconhecida.')
    else:
      cor = entrada.strip().lower()
      break

  # coletar comprimento
  while True:
    entrada = input('Comprimento (cm): ')
    if not entrada.isnumeric():
      print('Erro: Digite um número.')
    elif float(entrada) <= 0:
      print('Erro: Valor deve ser positivo.')
    else:
      comprimento = float(entrada)
      break

  return (peso, cor, comprimento)

# função validar
def validar(peso, cor, comprimento):
  motivos = []
  aprovada = True

  # critério peso
  if peso < 95 or peso > 105:
    aprovada = False
    motivos.append(f"Peso inválido: {peso}g (esperado: 95g–105g)")

  # critério cor
  if cor not in ["azul", "verde"]:
    aprovada = False
    motivos.append(f"Cor inválida: '{cor}' (esperado: azul ou verde)")

  # critério comprimento
  if comprimento < 10 or comprimento > 20:
    aprovada = False
    motivos.append(f"Comprimento inválido: {comprimento}cm (esperado: 10–20cm)")

  if aprovada == True:
    return("aprovada", [])
  else:
    return("reprovada", motivos)
  
# função gerenciar caixa
def gerenciar_caixa():
  global caixa_atual, contador_caixas

  if caixa_atual.total_pecas >= 10:

    # fecha caixa cheia
    caixa_atual.status = "fechada"
    lista_caixas.append(caixa_atual)
    print(f"Caixa {caixa_atual.numero} fechada (10/10 peças).")

    # abre nova caixa
    contador_caixas = contador_caixas + 1
    caixa_atual = Caixa(
      numero = contador_caixas,
      pecas = [],
      total_pecas = 0,
      status = "aberta"
      )
    print(f"Nova caixa {contador_caixas} aberta.")

# função armazenar peça
def armazenar(peca):
  
  if peca.status == "aprovada":
    gerenciar_caixa()
    caixa_atual.pecas.append(peca)
    caixa_atual.total_pecas = caixa_atual.total_pecas + 1
    lista_aprovadas.append(peca)
    print(f"Peça aprovada → Caixa {caixa_atual.numero} ({caixa_atual.total_pecas}/10)")
  else:
    lista_reprovadas.append(peca)
    print("Peça reprovada. Motivos:")
    for m in peca.motivos:
      print(f"  → {m}")

# função cadastrar peça
def cadastrar_peca():
  print("── CADASTRAR PEÇA ──")
  
  id = gerar_id()
  (peso, cor, comprimento) = coletar_dados()
  (status, motivos) = validar(peso, cor, comprimento)
  peca = Peca(
    id = id,
    peso = peso,
    cor = cor,
    comprimento = comprimento,
    status = status,
    motivos = motivos
    )
  armazenar(peca)

# função listar peças
def listar_pecas():
  print(f"── APROVADAS ({len(lista_aprovadas)}) ──")

  if len(lista_aprovadas) == 0:
    print("Nenhuma peça aprovada.")
  else:
    for p in lista_aprovadas:
      print(f"ID:{p.id} | {p.peso}g | {p.cor} | {p.comprimento}cm")
  
  print(f"── REPROVADAS ({len(lista_reprovadas)}) ──")

  if len(lista_reprovadas) == 0:
    print("Nenhuma peça reprovada.")
  else:
    for p in lista_reprovadas:
      print(f"ID:{p.id} | {p.peso}g | {p.cor} | {p.comprimento}cm")
      for m in p.motivos:
        print(f"  → {m}")

# função remover peça
def remover_peca():
    print("── REMOVER PEÇA ──")
    id_buscado = input("ID da peça: ")

    if not id_buscado.isnumeric():
        print("Erro: ID inválido.")
        return

    id_buscado = int(id_buscado)
    encontrada = False

    # busca em aprovadas
    for p in lista_aprovadas:
      if p.id == id_buscado:
        print(f"Encontrada (APROVADA): ID:{p.id} | {p.peso}g | {p.cor} | {p.comprimento}cm")
        confirmacao = input("Confirmar remoção? (S/N): ")

        if confirmacao.lower() == "s":
          lista_aprovadas.remove(p)

          # remove da caixa atual se estiver nela
          if p in caixa_atual.pecas:
            caixa_atual.pecas.remove(p)
            caixa_atual.total_pecas = caixa_atual.total_pecas - 1
          else:
            # busca em caixas fechadas
            for cx in lista_caixas:
              if p in cx.pecas:
                cx.pecas.remove(p)
                break
                    
          print("Peça removida com sucesso.")
        else:
          print("Operação cancelada.")

        encontrada = True
        break

    # busca em reprovadas (se não achou em aprovadas)
    if encontrada == False:
      for p in lista_reprovadas:
        if p.id == id_buscado:
          print(f"Encontrada (REPROVADA): ID:{p.id} | {p.peso}g | {p.cor} | {p.comprimento}cm")
          confirmacao = input("Confirmar remoção? (S/N): ")

          if confirmacao.lower() == "s":
            lista_reprovadas.remove(p)
            print("Peça removida com sucesso.")
          else:
            print("Operação cancelada.")
          
          encontrada = True
          break

    if encontrada == False:
      print(f"Peça ID {id_buscado} não encontrada.")

# função listar caixas
def listar_caixas():
  print(f"── CAIXAS FECHADAS ({len(lista_caixas)}) ──")

  if len(lista_caixas) == 0:
    print("Nenhuma caixa fechada.")
  else:
    for cx in lista_caixas:
      print(f"Caixa #{cx.numero} — {cx.total_pecas} peças")
      for p in cx.pecas:
        print(f"  • ID:{p.id} | {p.peso}g | {p.cor} | {p.comprimento}cm")

      # exibe caixa aberta atual
  print(f"── CAIXA ATUAL (aberta) — {caixa_atual.total_pecas}/10 ──")
  if caixa_atual.pecas == "":
    print("  (vazia)")
  else:
    for p in caixa_atual.pecas:
      print(f"  • ID:{p.id} | {p.peso}g | {p.cor} | {p.comprimento}cm")

# função gerar relatório
def gerar_relatorio():
  print("── RELATÓRIO FINAL ──")

  total_ap = len(lista_aprovadas)
  total_rep = len(lista_reprovadas)
  total = total_ap + total_rep

  if total > 0:
    taxa_ap = (total_ap / total) * 100
    taxa_rep = (total_rep / total) * 100
  else:
    taxa_ap = 0
    taxa_rep = 0

  print(f"Total cadastradas : {total}")
  print(f"Aprovadas         : {total_ap} ({taxa_ap}%)")
  print(f"Reprovadas        : {total_rep} ({taxa_rep}%)")
  print(f"Caixas fechadas   : {len(lista_caixas)}")
  print(f"Caixa atual       : #{caixa_atual.numero} com {caixa_atual.total_pecas} peça(s)")

  # contagem de motivos
  cont_peso = 0
  cont_cor = 0
  cont_comp = 0

  for p in lista_reprovadas:
    for m in p.motivos:
      if "Peso" in m: 
        cont_peso = cont_peso + 1
      if "Cor" in m:
        cont_cor = cont_cor + 1
      if "Comprimento" in m:
        cont_comp = cont_comp + 1

  print("── MOTIVOS DE REPROVAÇÃO ──")
  print(f"  Peso fora do padrão        : {cont_peso}")
  print(f"  Cor inválida               : {cont_cor}")
  print(f"  Comprimento fora do padrão : {cont_comp}")