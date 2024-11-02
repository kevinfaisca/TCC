import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
df = pd.read_excel('stackoverflow_dataset.xlsx')

# Limpeza da coluna 'Country'
df['Country'] = df['Country'].str.strip()
df['Country'] = df['Country'].replace({
    'United States of America': 'United States',
    'United Kingdom': 'UK',
    'Russian Federation': 'Russia',
    'Viet Nam': 'Vietnam',
    'Iran, Islamic Republic of...': 'Iran'
})
df = df.dropna(subset=['Country'])

# Função para separar valores nas colunas de linguagens
def split_languages(language_str):
    return language_str.split(';') if pd.notnull(language_str) else []

# Aplicar a função de separação na coluna 'LanguageWorkedWith'
df['LanguageWorkedWith_list'] = df['LanguageWorkedWith'].apply(split_languages)

# Colunas binárias para cada linguagem
all_languages_worked = set([lang for sublist in df['LanguageWorkedWith_list'] for lang in sublist])
for language in all_languages_worked:
    df[f'WorkedWith_{language}'] = df['LanguageWorkedWith_list'].apply(lambda x: 1 if language in x else 0)

# Excluir colunas indesejadas
languages_to_exclude = ['WorkedWith_SQL', 'WorkedWith_HTML/CSS', 'WorkedWith_HTML', 
                        'WorkedWith_CSS', 'WorkedWith_Bash/Shell/PowerShell', 'WorkedWith_Bash/Shell']
for lang in languages_to_exclude:
    if lang in df.columns:
        df.drop(columns=[lang], inplace=True)

# Calcular a soma de cada linguagem e converter para porcentagem
language_worked_counts = df[[col for col in df.columns if col.startswith('WorkedWith_')]].sum()
language_worked_percent = (language_worked_counts / len(df)) * 100

# Filtrar top 10 linguagens e top 10 países com mais desenvolvedores
top_languages = language_worked_percent.sort_values(ascending=False).head(10).index
df_top_languages = df[top_languages]

# Agrupamento por país para as linguagens mais usadas nos top países
country_language_counts = df.groupby('Country')[top_languages].sum()
top_countries = country_language_counts.sum(axis=1).sort_values(ascending=False).head(10).index
filtered_country_language_counts = country_language_counts.loc[top_countries]

# Configurar o tamanho da figura e estilo do gráfico
plt.figure(figsize=(20, 12))  # Aumentar o tamanho da figura
sns.set(style="whitegrid")
colors = sns.color_palette("Paired", len(top_languages))  # Usar uma paleta de cores diferente

# Plotar o gráfico de barras com maior espaçamento
ax = filtered_country_language_counts.plot(
    kind='bar', color=colors, width=0.7, edgecolor='grey', linewidth=1
)

# Ajustes de título, rótulos e espaçamento
plt.title('Top 10 Linguagens de Programação por País', fontsize=20, pad=30)
plt.xlabel('País', fontsize=14, labelpad=15)
plt.ylabel('Número de Desenvolvedores', fontsize=14, labelpad=20)

# Configurar tamanhos dos rótulos e espaçamento entre barras e legendas
plt.xticks(rotation=45, fontsize=11, ha='right')
plt.yticks(fontsize=11)
plt.legend(
    [lang.split('_')[-1] for lang in top_languages],
    title="Linguagens", title_fontsize=12, fontsize=10,
    bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.
)

# Adicionar uma grade de fundo mais leve para facilitar a visualização dos valores
plt.grid(axis='y', linestyle='--', linewidth=0.5)

# Ajuste de layout para evitar sobreposição e melhorar o visual
plt.tight_layout()

# Salvar a figura em alta qualidade
plt.savefig('top_languages_by_country.png', dpi=300)  # Salvar com 300 DPI

# Exibir o gráfico
plt.show()
