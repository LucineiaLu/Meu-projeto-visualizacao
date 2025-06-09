from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Criar um novo PDF
c = canvas.Canvas("relatorio_visualizacao.pdf", pagesize=letter)
width, height = letter

# Adicionar título
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2.0, height - 50, "Análise de Taxas de Rendimento Escolar - 2023")

# Adicionar descrição
c.setFont("Helvetica", 12)
c.drawString(50, height - 100, "Este relatório apresenta uma análise das taxas de aprovação, reprovação e abandono escolar")
c.drawString(50, height - 115, "nos estados de Minas Gerais, São Paulo e Rio de Janeiro no ano de 2023.")

# Adicionar gráficos (certifique-se de que os gráficos foram salvos previamente como imagens)
c.drawImage("plot1_taxas_percentuais.png", 50, height - 400, width=500, height=250)
c.drawImage("plot2_abandono_pizza.png", 50, height - 700, width=500, height=250)


# Salvar o PDF
c.save()
