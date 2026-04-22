from flask import Flask, render_template, request, redirect, url_for, send_file
from main import *
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

# ROTAS
@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    peso = request.form["peso"]
    cor = request.form["cor"]
    comprimento = request.form["comprimento"]

    if not peso.replace(".","").isnumeric() or not comprimento.replace(".","").isnumeric():
      return render_template("index.html", erro="Dados inválidos.")

    peso = float(peso)
    cor = cor.strip().lower()
    comprimento = float(comprimento)
    id_peca = gerar_id()
    (status, motivos) = validar(peso, cor, comprimento)
    peca = Peca(id_peca, peso, cor, comprimento, status, motivos)
    armazenar(peca)

    return redirect(url_for("index"))

  total = len(lista_aprovadas) + len(lista_reprovadas)
  total_ap = len(lista_aprovadas)
  total_rep = len(lista_reprovadas)
  total_caixas = len(lista_caixas)
  taxa_ap = round((total_ap  / total) * 100, 1) if total > 0 else 0
  taxa_rep = round((total_rep / total) * 100, 1) if total > 0 else 0

  return render_template("index.html",
    total = total,
    total_ap = total_ap,
    total_rep = total_rep,
    taxa_ap = taxa_ap,
    taxa_rep = taxa_rep,
    total_caixas = total_caixas,
    caixa_numero = caixa_atual.numero,
    caixa_pecas = caixa_atual.total_pecas
  )

@app.route("/listar")
def listar():
  return render_template("listar.html", 
    aprovadas = lista_aprovadas, 
    reprovadas = lista_reprovadas
  )

@app.route("/caixas")
def caixas():
  return render_template("caixas.html",
    lista_caixas = lista_caixas,
    caixa_atual = caixa_atual
  )

@app.route("/remover", methods=["GET", "POST"])
def remover():
  mensagem = None

  if request.method == "POST":
    id_buscado = request.form["id"]

    if not id_buscado.isnumeric():
      mensagem = "Erro: ID inválido."
      return render_template("remover.html", mensagem=mensagem)

    id_buscado = int(id_buscado)
    encontrada = False

    for p in lista_aprovadas:
      if p.id == id_buscado:
        lista_aprovadas.remove(p)

        if p in caixa_atual.pecas:
          caixa_atual.pecas.remove(p)
          caixa_atual.total_pecas -= 1
        else:
          for cx in lista_caixas:
            if p in cx.pecas:
              cx.pecas.remove(p)
              break

        encontrada = True
        break

    if not encontrada:
      for p in lista_reprovadas:
        if p.id == id_buscado:
          lista_reprovadas.remove(p)
          encontrada = True
          break

    if encontrada:
      mensagem = "Peça removida com sucesso."
    else:
      mensagem = f"Peça ID {id_buscado} não encontrada."

  return render_template("remover.html", mensagem=mensagem)

@app.route("/relatorio")
def relatorio():
  total_ap = len(lista_aprovadas)
  total_rep = len(lista_reprovadas)
  total = total_ap + total_rep
  taxa_ap = round((total_ap / total) * 100, 1) if total > 0 else 0
  taxa_rep = round((total_rep / total) * 100, 1) if total > 0 else 0

  cont_peso = 0
  cont_cor = 0
  cont_comp = 0

  for p in lista_reprovadas:
    for m in p.motivos:
      if "Peso" in m:
        cont_peso += 1
      if "Cor" in m:
        cont_cor += 1
      if "Comprimento" in m:
        cont_comp += 1

  return render_template("relatorio.html",
    total = total,
    total_ap = total_ap,
    total_rep = total_rep,
    taxa_ap = taxa_ap,
    taxa_rep = taxa_rep,
    total_caixas = len(lista_caixas),
    caixa_atual = caixa_atual,
    cont_peso = cont_peso,
    cont_cor = cont_cor,
    cont_comp = cont_comp
  )

@app.route("/relatorio/download")
def download_relatorio():
  total_ap  = len(lista_aprovadas)
  total_rep = len(lista_reprovadas)
  total     = total_ap + total_rep
  taxa_ap   = round((total_ap  / total) * 100, 1) if total > 0 else 0
  taxa_rep  = round((total_rep / total) * 100, 1) if total > 0 else 0

  cont_peso = 0
  cont_cor  = 0
  cont_comp = 0

  for p in lista_reprovadas:
    for m in p.motivos:
      if "Peso" in m:
        cont_peso += 1
      if "Cor" in m:
        cont_cor += 1
      if "Comprimento" in m:
        cont_comp += 1

  buffer = io.BytesIO()
  c = canvas.Canvas(buffer, pagesize=A4)
  largura, altura = A4

  c.setFont("Helvetica-Bold", 16)
  c.drawString(50, altura - 60, "RELATÓRIO FINAL — SiCPQ")

  c.setFont("Helvetica", 12)
  c.drawString(50, altura - 100, f"Total cadastradas : {total}")
  c.drawString(50, altura - 120, f"Aprovadas         : {total_ap} ({taxa_ap}%)")
  c.drawString(50, altura - 140, f"Reprovadas        : {total_rep} ({taxa_rep}%)")
  c.drawString(50, altura - 160, f"Caixas fechadas   : {len(lista_caixas)}")
  c.drawString(50, altura - 180, f"Caixa atual       : #{caixa_atual.numero} com {caixa_atual.total_pecas} peca(s)")

  c.setFont("Helvetica-Bold", 12)
  c.drawString(50, altura - 220, "MOTIVOS DE REPROVAÇÃO:")

  c.setFont("Helvetica", 12)
  c.drawString(50, altura - 240, f"Peso fora do padrao        : {cont_peso}")
  c.drawString(50, altura - 260, f"Cor invalida               : {cont_cor}")
  c.drawString(50, altura - 280, f"Comprimento fora do padrao : {cont_comp}")

  c.save()
  buffer.seek(0)

  return send_file(
    buffer,
    as_attachment = True,
    download_name = "relatorio_sicpq.pdf",
    mimetype = "application/pdf"
  )

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)