import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Carregar o dataset
df = pd.read_excel('stackoverflow_dataset.xlsx')

# Visualizar as primeiras linhas do dataset
print(df.head())

# Verificar valores ausentes
print(df.isnull().sum())

### Pré-processamento
# Amostragem da base (por exemplo, usar 10% dos dados originais) código comentados pois agora está rodando a base inteira
#df = df.sample(frac=0.9, random_state=42) 

# Função para separar valores nas colunas de linguagens
def split_languages(language_str):
    if pd.isnull(language_str):
        return []
    return language_str.split(';')

# Aplicar a função de separação nas colunas 'LanguageWorkedWith' e 'LanguageDesireNextYear'
df['LanguageWorkedWith_list'] = df['LanguageWorkedWith'].apply(split_languages)
df['LanguageDesireNextYear_list'] = df['LanguageDesireNextYear'].apply(split_languages)

# Explorar todas as linguagens presentes no dataset
all_languages_worked = set([lang for sublist in df['LanguageWorkedWith_list'] for lang in sublist])
all_languages_desire = set([lang for sublist in df['LanguageDesireNextYear_list'] for lang in sublist])

# Criar colunas binárias (one-hot encoding) para cada linguagem
for language in all_languages_worked.union(all_languages_desire):
    df[f'WorkedWith_{language}'] = df['LanguageWorkedWith_list'].apply(lambda x: 1 if language in x else 0)
    df[f'DesireNextYear_{language}'] = df['LanguageDesireNextYear_list'].apply(lambda x: 1 if language in x else 0)

# Remover colunas desnecessárias
df.drop(columns=['LanguageWorkedWith', 'LanguageDesireNextYear', 'LanguageWorkedWith_list', 'LanguageDesireNextYear_list'], inplace=True)

# Identificar colunas categóricas e aplicar Label Encoding
label_columns = df.select_dtypes(include=['object']).columns
le = LabelEncoder()

for col in label_columns:
    df[col] = le.fit_transform(df[col].astype(str))

# Análise da distribuição das linguagens mais usadas
language_worked_counts = df[[col for col in df.columns if col.startswith('WorkedWith_')]].sum()

# Converter para porcentagem
language_worked_percent = (language_worked_counts / len(df)) * 100

# Remover linguagens indesejadas
languages_to_exclude = [
    'WorkedWith_SQL', 'WorkedWith_HTML/CSS', 'WorkedWith_HTML', 'WorkedWith_CSS',
    'WorkedWith_Bash/Shell/PowerShell', 'WorkedWith_Bash/Shell'
]
language_worked_percent = language_worked_percent.drop(languages_to_exclude)

# Identificar as linguagens com menos de 1% de representação
languages_below_1_percent_worked = language_worked_percent[language_worked_percent < 1].index

# Somar as porcentagens das linguagens abaixo de 1% e criar uma nova categoria "WorkedWith_Others"
others_worked_sum = language_worked_percent[languages_below_1_percent_worked].sum()

# Remover as linguagens abaixo de 1% da lista original
language_worked_percent = language_worked_percent.drop(languages_below_1_percent_worked)

# Adicionar a nova categoria "WorkedWith_Others"
language_worked_percent['WorkedWith_Others'] = others_worked_sum

# Ordenar as linguagens pela porcentagem
language_worked_percent = language_worked_percent.sort_values(ascending=False)

# Gráfico de linguagens usadas (em porcentagem)
plt.figure(figsize=(12, 8))
sns.barplot(x=language_worked_percent.values, y=language_worked_percent.index, palette='viridis')

# Adicionando porcentagem como texto ao lado de cada barra
for i, v in enumerate(language_worked_percent.values):
    plt.text(v + 0.5, i, f"{v:.2f}%", color='black', va='center')

plt.title('Distribuição de Linguagens de Programação Usadas (%)')
plt.xlabel('Porcentagem de Desenvolvedores')
plt.ylabel('Linguagem')

# Ajustar layout para evitar sobreposição
plt.tight_layout()
plt.show()

# Análise de linguagens desejadas
language_desire_counts = df[[col for col in df.columns if col.startswith('DesireNextYear_')]].sum()

# Converter para porcentagem
language_desire_percent = (language_desire_counts / len(df)) * 100

# Remover linguagens indesejadas
languages_to_exclude = [
    'DesireNextYear_SQL', 'DesireNextYear_HTML/CSS', 'DesireNextYear_HTML', 'DesireNextYear_CSS',
    'DesireNextYear_Bash/Shell/PowerShell', 'DesireNextYear_Bash/Shell'
]
language_desire_percent = language_desire_percent.drop(languages_to_exclude)

# Identificar as linguagens com menos de 1% de representação
languages_below_1_percent_desire = language_desire_percent[language_desire_percent < 1].index

# Somar as porcentagens das linguagens abaixo de 1% e criar uma nova categoria "DesireNextYear_Others"
others_desire_sum = language_desire_percent[languages_below_1_percent_desire].sum()

# Remover as linguagens abaixo de 1% da lista original
language_desire_percent = language_desire_percent.drop(languages_below_1_percent_desire)

# Adicionar a nova categoria "DesireNextYear_Others"
language_desire_percent['DesireNextYear_Others'] = others_desire_sum

# Ordenar as linguagens pela porcentagem
language_desire_percent = language_desire_percent.sort_values(ascending=False)

# Gráfico de linguagens desejadas para o próximo ano (em porcentagem)
plt.figure(figsize=(12, 8))
sns.barplot(x=language_desire_percent.values, y=language_desire_percent.index, palette='viridis')

# Adicionando porcentagem como texto ao lado de cada barra
for i, v in enumerate(language_desire_percent.values):
    plt.text(v + 0.5, i, f"{v:.2f}%", color='black', va='center')

plt.title('Distribuição de Linguagens Desejadas para o Próximo Ano (%)')
plt.xlabel('Porcentagem de Desenvolvedores')
plt.ylabel('Linguagem')

# Ajustar layout para evitar sobreposição
plt.tight_layout()
plt.show()
