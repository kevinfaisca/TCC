import requests
from collections import Counter
import matplotlib.pyplot as plt

# Função para buscar dados da API para um ano específico
def buscar_linguagens_por_ano(ano, headers):
    url = "https://api.github.com/search/repositories"
    language_counter = Counter()
    total_repos_desejados = 500
    repos_coletados = 0
    page = 1
    per_page = 100

    while repos_coletados < total_repos_desejados:
        # Filtro de data específico para o ano
        params = {
            "q": f"stars:>1000 pushed:{ano}-01-01..{ano}-12-31",
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page
        }
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            repos = response.json()["items"]
            repos_coletados += len(repos)

            for repo in repos:
                owner = repo["owner"]["login"]
                repo_name = repo["name"]
                languages_url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
                languages_response = requests.get(languages_url, headers=headers)

                if languages_response.status_code == 200:
                    languages = languages_response.json()
                    for language in languages:
                        language_counter[language] += languages[language]
                else:
                    print(f"Erro ao buscar linguagens para {repo_name}: {languages_response.status_code}")

            page += 1
        else:
            print(f"Erro na busca de repositórios: {response.status_code}")
            break

    # Filtrar linguagens indesejadas
    excluded_languages = {"HTML", "CSS", "SQL", "PLpgSQL", "PLSQL"}
    filtered_language_counter = {lang: count for lang, count in language_counter.items() if lang not in excluded_languages}
    
    # Calcular porcentagens
    total_bytes = sum(filtered_language_counter.values())
    top_languages = [language for language, count in Counter(filtered_language_counter).most_common(10)]
    percentages = [(count / total_bytes) * 100 for _, count in Counter(filtered_language_counter).most_common(10)]
    
    return top_languages, percentages

# Headers com token de autenticação
headers = {
    "Authorization": "token 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"
}

# Coletar dados para cada ano
anos = [,2020,2023,2022, 2023, 2024]
dados_anuais = {ano: buscar_linguagens_por_ano(ano, headers) for ano in anos}

# Configurar tamanho da figura e tamanho da fonte
plt.figure(figsize=(14, 10))

for i, (ano, (languages, percentages)) in enumerate(dados_anuais.items()):
    plt.barh(
        [f"{lang} ({ano})" for lang in languages],
        percentages,
        label=f"Ano {ano}",
        height=0.3,  # Altura da barra para aumentar o espaçamento entre elas
        alpha=0.7
    )

# Ajustes de fonte e título
plt.xlabel("Porcentagem de Código (%)", fontsize=14)
plt.ylabel("Linguagem", fontsize=14)
plt.title("Comparação das Linguagens Mais Usadas por Ano em Repositórios do GitHub", fontsize=16)
plt.legend(title="Ano", fontsize=12, title_fontsize=13)
plt.gca().tick_params(axis='both', which='major', labelsize=12)  # Tamanho das fontes dos eixos

# Adicionar a fonte na parte inferior do gráfico
plt.tight_layout()  # Ajusta o layout para garantir que tudo fique visível

plt.show()
