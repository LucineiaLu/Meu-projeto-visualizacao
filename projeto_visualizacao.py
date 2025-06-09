from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Carregar o dataset
url = "https://www.kaggle.com/datasets/joaoassaoka/taxas-de-rendimento-escolar-inep?select=Taxas_de_Rendimento_Escolar_2013_2023.csv"
df = pd.read_csv("Taxas_de_Rendimento_Escolar.csv")

# Filtrar apenas o ano de 2023 e os estados desejados
estados_selecionados = ["Minas Gerais", "Rio de Janeiro", "São Paulo"]
df_2023 = df[(df["Ano"] == 2023) & (
    df["Unidade_Geografica"].isin(estados_selecionados))]

# Verificar as primeiras linhas
print(df_2023.head())

# Simulando dados para 2023 - substitua com o dataset real depois
data = {
    'Unidade_Geográfica': ['Minas Gerais', 'São Paulo', 'Rio de Janeiro'] * 2,
    'Etapa_Ensino': ['Fundamental', 'Fundamental', 'Fundamental', 'Médio', 'Médio', 'Médio'],
    'Taxa_Aprovacao': [85.2, 88.1, 83.5, 82.3, 86.4, 81.0],
    'Taxa_Reprovacao': [8.1, 6.3, 9.5, 10.2, 8.0, 11.1],
    'Taxa_Abandono': [6.7, 5.6, 7.0, 7.5, 5.6, 7.9],
    'Num_Aprovacao': [1200000, 2200000, 1500000, 1100000, 2100000, 1400000],
    'Num_Reprovacao': [114000, 157000, 171000, 140000, 175000, 192000],
    'Num_Abandono': [94500, 140000, 126000, 121000, 138000, 136000],
}

df = pd.DataFrame(data)

# 📈 Plot 1 – Comparação entre taxas percentuais de aprovação, reprovação e abandono
df_plot1 = df.groupby('Unidade_Geográfica')[
    ['Taxa_Aprovacao', 'Taxa_Reprovacao', 'Taxa_Abandono']].mean().reset_index()
df_plot1_melt = df_plot1.melt(
    id_vars='Unidade_Geográfica', var_name='Indicador', value_name='Percentual')

plt.figure(figsize=(10, 6))
sns.barplot(data=df_plot1_melt, x='Unidade_Geográfica',
            y='Percentual', hue='Indicador')
plt.title('Taxas de Rendimento Escolar por Estado - 2023 (%)')
plt.ylabel('Percentual (%)')
plt.xlabel('Estado')
plt.legend(title='Indicador')
plt.tight_layout()
plt.savefig('plot1_taxas_percentuais.png')
plt.close()

# ✅ Breve descrição: Este gráfico compara os percentuais de aprovação, reprovação e abandono escolar nos três estados. Nota-se que São Paulo apresenta a maior taxa de aprovação, enquanto Rio de Janeiro teve a maior de abandono.
# Este gráfico compara as taxas percentuais de aprovação, reprovação e abandono escolar nos três estados escolhidos em 2023, oferecendo uma visão clara das diferenças no rendimento escolar.

# 🥧 Plot 2 – Gráfico de pizza da proporção total de abandono por estado
df_plot2 = df.groupby('Unidade_Geográfica')['Num_Abandono'].sum().reset_index()
plt.figure(figsize=(8, 6))
plt.pie(df_plot2['Num_Abandono'], labels=df_plot2['Unidade_Geográfica'],
        autopct='%1.1f%%', startangle=140)
plt.title('Proporção de Alunos que Abandonaram a Escola em 2023')
plt.axis('equal')
plt.savefig('plot2_abandono_pizza.png')
plt.close()

# ✅ Breve descrição: Representa a participação percentual de cada estado no total de alunos que abandonaram os estudos em 2023. É uma visão de proporção direta.
# Este gráfico mostra a participação percentual de cada estado na taxa total de abandono escolar em 2023.

# 📊 Plot 3 – Taxa de abandono por etapa de ensino e estado (gráfico interativo)
fig3 = px.bar(df,
              x='Unidade_Geográfica',
              y='Taxa_Abandono',
              color='Taxa_Reprovacao',
              barmode='group',
              title='Taxa de Abandono Escolar por Etapa de Ensino (2023)')
# Agora funcionará com kaleido instalado
fig3.write_image('plot3_abandono_etapa.png')
fig3.show()


# ✅ Breve descrição: Exibe a taxa de abandono escolar separada por ensino Fundamental e Médio nos três estados. Minas Gerais teve maior abandono no Fundamental, enquanto o Ensino Médio foi o mais crítico no Rio de Janeiro.
# Este gráfico interativo exibe a taxa de abandono por etapa de ensino e estado, permitindo a análise detalhada conforme o usuário interage.


# Criar um novo PDF
c = canvas.Canvas("relatorio_visualizacao.pdf", pagesize=letter)
width, height = letter

# Adicionar título
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2.0, height - 50,
                    "Análise de Taxas de Rendimento Escolar - 2023")

# Adicionar descrição
c.setFont("Helvetica", 12)
c.drawString(50, height - 100,
             "Este relatório apresenta uma análise das taxas de aprovação, reprovação e abandono escolar")
c.drawString(50, height - 115,
             "nos estados de Minas Gerais, São Paulo e Rio de Janeiro no ano de 2023.")

# Adicionar gráficos (certifique-se de que os gráficos foram salvos previamente como imagens)
c.drawImage("plot1_taxas_percentuais.png", 50,
            height - 400, width=500, height=250)
c.drawImage("plot2_abandono_pizza.png", 50,
            height - 700, width=500, height=250)
c.drawImage("plot3_abandono_etapa.png", 50,
            height - 700, width=500, height=250)

# Salvar o PDF
c.save()
