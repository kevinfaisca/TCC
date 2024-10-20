import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
df = pd.read_excel('stackoverflow_dataset.xlsx')

# Limpeza da coluna 'Country'
df['Country'] = df['Country'].str.strip()  # Remover espaços extras
df['Country'] = df['Country'].replace({
    'United States of America': 'United States',
    'United Kingdom': 'UK',
    'Russian Federation': 'Russia',
    'Viet Nam': 'Vietnam',
    'Iran, Islamic Republic of...': 'Iran'
})
# Remover valores ausentes na coluna 'Country'
df = df.dropna(subset=['Country'])

# Função para separar valores nas colunas de linguagens
def split_languages(language_str):
    if pd.isnull(language_str):
        return []
    return language_str.split(';')

# Aplicar a função de separação na coluna 'LanguageWorkedWith'
df['LanguageWorkedWith_list'] = df['LanguageWorkedWith'].apply(split_languages)

# Criar colunas binárias (one-hot encoding) para cada linguagem
all_languages_worked = set([lang for sublist in df['LanguageWorkedWith_list'] for lang in sublist])
for language in all_languages_worked:
    df[f'WorkedWith_{language}'] = df['LanguageWorkedWith_list'].apply(lambda x: 1 if language in x else 0)

# Remover colunas indesejadas
languages_to_exclude = ['WorkedWith_SQL', 'WorkedWith_HTML/CSS', 'WorkedWith_HTML', 
                        'WorkedWith_CSS', 'WorkedWith_Bash/Shell/PowerShell', 
                        'WorkedWith_Bash/Shell/PowerShell', 'WorkedWith_Bash/Shell']
for lang in languages_to_exclude:
    if lang in df.columns:
        df.drop(columns=[lang], inplace=True)

# Calcular a soma de cada linguagem e criar a categoria "Others" para linguagens <1%
language_worked_counts = df[[col for col in df.columns if col.startswith('WorkedWith_')]].sum()

# Converter para porcentagem
language_worked_percent = (language_worked_counts / len(df)) * 100

# Garantir que todos os valores sejam numéricos
language_worked_percent = pd.to_numeric(language_worked_percent, errors='coerce').fillna(0)

# Identificar linguagens a serem agrupadas como "Others"
languages_others = language_worked_percent[language_worked_percent < 1].index.tolist()

# Criar coluna "WorkedWith_Others" somando todas as linguagens com menos de 1%
df['WorkedWith_Others'] = df[languages_others].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# Remover as colunas individuais das linguagens agrupadas em "Others"
df.drop(columns=languages_others, inplace=True)

# Agrupamento por país para análise das linguagens
country_language_counts = df.groupby('Country').sum(numeric_only=True)

# Filtrar os top 10 países com mais desenvolvedores para uma visualização mais limpa
top_countries = country_language_counts.sum(axis=1).sort_values(ascending=False).head(10).index
filtered_country_language_counts = country_language_counts.loc[top_countries]

# Gráfico de barras para mostrar as linguagens mais populares nos top países
plt.figure(figsize=(14, 10))
sns.set(style="whitegrid")

# Plotar o gráfico de barras empilhado com melhor espaçamento
ax = filtered_country_language_counts.loc[:, [col for col in filtered_country_language_counts.columns if col.startswith('WorkedWith_')]].plot(
    kind='barh', stacked=True, figsize=(14, 8), colormap='viridis', width=0.85)

# Ajustar títulos e legendas para melhorar a leitura
plt.title('Linguagens de Programação Mais Usadas por País (Top 10)', fontsize=16)
plt.xlabel('Número de Desenvolvedores', fontsize=14)
plt.ylabel('País', fontsize=14)
plt.tight_layout()
plt.legend(title='Linguagens', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', linewidth=0.5)

# Exibir o gráfico
plt.show()
