# Mercado Bitcoin ETL Pipeline

Pipeline de ingestão de dados (camada Bronze) consumindo a API pública do Mercado Bitcoin. 

O foco deste projeto não é apenas a extração dos dados, mas a implementação de um padrão de arquitetura resiliente, assíncrono e tipado, simulando as exigências de um ambiente de produção real.

## 🛠️ Stack e Decisões de Arquitetura

- **Python 3.13 + [uv](https://github.com/astral-sh/uv):** Gerenciamento de dependências e ambiente virtual extremamente rápido, substituindo o pip/poetry padrão.
- **Concorrência (`ThreadPoolExecutor` + `requests.Session`):** Como a extração de APIs é uma tarefa I/O bound, o uso de múltiplas threads aliado ao reaproveitamento de conexões TCP (Session) reduz drasticamente o tempo de extração.
- **Resiliência (`Tenacity`):** Tratamento de indisponibilidades da API (erros 500) e limites de taxa com estratégia de retry e *exponential backoff*. Ativos inexistentes (404) são logados adequadamente sem derrubar a esteira.
- **Validação de Contrato (`Pydantic V2`):** Coerção de tipos automática (strings da API convertidas para float) e garantia do esquema de dados logo na entrada. Se o contrato da API mudar, o erro é capturado na extração, protegendo o *Data Lake*.
- **Processamento (`Polars`):** Substituição do Pandas pelo Polars para manipulação dos DataFrames, aproveitando o motor em Rust/C++ para filtragem, ordenação e cálculo do spread das moedas com execução otimizada.
- **Armazenamento:** Exportação nativa dos dados transformados para o formato `.parquet` particionado na camada Bronze.
- **Deploy (`Docker`):** Ambiente 100% conteinerizado (imagem slim) para evitar o problema de "na minha máquina funciona".

## 🚀 Como executar

Você pode rodar o projeto localmente ou via Docker.

### Opção 1: Usando o Docker (Recomendado)
Apenas certifique-se de ter o Docker e o Docker Compose instalados.
```bash
# Sobe o container, executa a esteira e mapeia os dados para a sua máquina
docker compose up --build
```
*O arquivo `arquivo_final.parquet` será gerado automaticamente na pasta `./data/bronze/` do seu diretório atual.*

### Opção 2: Ambiente Local (com uv)

1. Clone o repositório.
2. Sincronize as dependências usando o `uv`:
```bash
uv sync --no-dev
```
3. Execute o módulo principal a partir da raiz do projeto:
```bash
uv run python -m src.main
```

## 📂 Estrutura do Projeto

```text
├── src/
│   ├── extract.py      # Lógica de conexão, concorrência e retries da API
│   ├── transform.py    # Processamento em lote usando Polars
│   ├── models.py       # Contratos de dados com Pydantic
│   └── main.py         # Orquestração do pipeline
├── data/
│   └── bronze/         # Destino dos arquivos Parquet locais
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml      # Configuração de dependências (formato uv)
└── README.md
```

## 📌 Próximos Passos (Roadmap)
- [ ] Implementar testes unitários automatizados com `pytest`.
- [ ] Adicionar pipeline de CI/CD via GitHub Actions para validação de PRs.
- [ ] Migrar o armazenamento do destino local para um bucket S3 na nuvem.