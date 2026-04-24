# SiCPQ — Sistema de Controle de Produção e Qualidade Industrial

[![Banner SiCPQ](https://img.youtube.com/vi/5ttSijkh9MQ/maxresdefault.jpg)](https://youtu.be/5ttSijkh9MQ)

## 📌 Descrição do Projeto

Este projeto foi desenvolvido para a disciplina Algoritmos e Lógica de Programação — UNIFECAF.
O objetivo foi criar um sistema em Python capaz de automatizar o controle de produção e qualidade de peças industriais, substituindo um processo manual sujeito a erros e atrasos.
O sistema valida cada peça com base em critérios objetivos, organiza as aprovadas em caixas e gera relatórios completos com download em PDF.

## 🎯 Problema

Empresas industriais que realizam o controle de qualidade manualmente enfrentam:

- Erros de conferência por falha humana
- Atrasos no processo de inspeção
- Dificuldade de rastreabilidade das peças
- Aumento de custos operacionais
- Falta de relatórios padronizados

## 💡 Solução

Foi desenvolvido um sistema completo em Python com interface web utilizando Flask.

Fluxo: Cadastro → Validação → Armazenamento em Caixas → Relatório → Download PDF

O sistema:

- Cadastra peças com peso, cor e comprimento
- Valida automaticamente com base em critérios definidos
- Separa aprovadas e reprovadas com motivos detalhados
- Agrupa peças aprovadas em caixas de até 10 unidades
- Fecha caixas automaticamente ao atingir o limite
- Gera relatório completo com download em PDF

## 🛠 Tecnologias Utilizadas

- Python 3
- Flask (interface web)
- ReportLab (geração de PDF)
- Jinja2 (templates HTML)
- HTML + CSS (front-end dark mode)
- Gunicorn (servidor de produção)
- Render (hospedagem)
- GitHub (versionamento)

## ⚙ Critérios de Validação

| Critério    | Condição de Aprovação |
| ----------- | --------------------- |
| Peso        | Entre 95g e 105g      |
| Cor         | Azul ou Verde         |
| Comprimento | Entre 10cm e 20cm     |

Se qualquer critério não for atendido → peça reprovada com motivo registrado.

## 📂 Estrutura do Projeto

```text
sistema-pecas-qualidade/
├── main.py              # Lógica principal do sistema
├── app.py               # Rotas Flask
├── requirements.txt     # Dependências
├── Procfile             # Configuração para deploy
├── templates/
│   ├── base.html        # Layout global
│   ├── index.html       # Dashboard + Cadastro
│   ├── listar.html      # Listagem de peças
│   ├── caixas.html      # Caixas fechadas e atual
│   ├── remover.html     # Remoção de peça
│   └── relatorio.html   # Relatório final
└── static/
    └── style.css        # Estilo dark mode
```

## 🖥 Funcionalidades

1. Dashboard — resumo geral com cards de totais e taxas
2. Cadastrar Peça — formulário com validação automática
3. Listar Peças — tabelas de aprovadas e reprovadas com motivos
4. Caixas — visualização de caixas fechadas e caixa atual
5. Remover Peça — remoção por ID com confirmação
6. Relatório Final — totais, percentuais, motivos e download em PDF

## 🚀 Como Usar

### Online

Acesse diretamente pelo navegador:
🔗 https://sistema-pecas-qualidade.onrender.com

⚠ O serviço gratuito do Render pode demorar até 50 segundos para iniciar após inatividade.

### Local

git clone https://github.com/guipardindev/sistema-pecas-qualidade.git

cd sistema-pecas-qualidade

pip3 install -r requirements.txt

python3 app.py

Acesse em: http://127.0.0.1:5000

## 🎬 Vídeo Pitch

🔗 Link do vídeo — https://youtu.be/5ttSijkh9MQ

## 📄 Documentação Teórica

A análise e discussão teórica do projeto está disponível no arquivo abaixo:
🔗 [Parte Teórica — Análise e Discussão](https://github.com/guipardindev/sistema-pecas-qualidade/blob/84967405ecd36e90d3c600c15595132eaf98dc6b/docs/Algoritmos_Analise_Discussao_Guilherme.pdf)

## ⚠ Considerações

- Os dados são armazenados em memória — reiniciar o servidor limpa os dados
- Para uso em produção real, recomenda-se integração com banco de dados
- O sistema é um protótipo acadêmico

## 👨‍🎓 Autor

Guilherme Pardin de Almeida
Disciplina: Algoritmos e Lógica de Programação
UNIFECAF — 2026
