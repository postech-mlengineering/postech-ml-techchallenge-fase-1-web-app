# Repositório do Aplicativo Web para o Tech Challenge da Fase 1 da Pós-Graduação em Machine Learning Engineering da FIAP

Este repositório consiste em um aplicativo web desenvolvido com Streamlit cujo objetivo é disponibilizar uma interface de usuário para o consumo das funcionalidades da API BooksToScrape.

Como resultado, a solução consolidou uma experiência de navegação completa que abrange o gerenciamento de identidade, através de fluxos de cadastro e login e a exploração dinâmica do catálogo por meio de filtros de preço, gênero e título. Ademais, o aplicativo integra-se ao motor de recomendação para fornecer recomendações personalizadas e disponibiliza um dashboard para a visualização de indicadores do acervo.

### Arquitetura

O diagrama abaixo ilustra a arquitetura do projeto na sua integridade e com suas principais funcionalidades:

<br><p align='center'><img src='https://github.com/postech-mlengineering/postech-ml-engineering-fase-1-tech-challenge-web-app/blob/f5c7fcc0ee041491799bbc4a9717ad7699b205c6/docs/arquitetura.svg' alt='Arquitetura'></p>

### Pré-requisitos

Certifique-se de ter o Python 3.11, o Poetry 2.1.1 e o Docker 29.1.1 (opcional) instalados em seu sistema.

### Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/jorgeplatero/postech-ml-techchallenge-fase-1-streamlit.git
cd postech-ml-techchallenge-fase-1-streamlit

poetry install
```

### Como Rodar a Aplicação

**Docker:**

1. Configure as variável de ambiente criando um arquivo .env na raiz do projeto e preencha com o conteúdo abaixo:

```bash
API_URL=http://postech_mlengineering_api:5000
```

2. Crie a rede externa (necessária para a comunicação entre os serviços):

```bash
docker network create postech_mlengineering_api
```

3. Inicie a aplicação:

```bash
docker-compose up --build
```

**Local:**

```bash
poetry run streamlit run main.py
```

O aplicativo estará disponível em `http://localhost:8501`. 

Certifique-se de que a API esteja em execução para que o aplicativo possa autenticar e buscar os dados.

### Funcionalidades

#### Autenticação

O aplicativo implementa um fluxo completo de controle de acesso e persistência de sessão.

- **Cadastro e Login:** página dedicada para registro de novos usuários e autenticação de usuários existentes

#### Acervo

Página desenvolvida para o consumo do acervo.

- **Filtros:** painel lateral com controles para alternar entre buscas por título/gênero e/ou faixa de preço
- **Navegação:** exibição do acervo organizada em grids responsivos, apresentando capas, preços e avaliações
- **Detalhamento:** uso de janelas de diálogo para exibição de informações completas de livro especificado sem perda de contexto da navegação
- **Recomendações:** carrossel paginado e interativo que apresenta recomendações de livros com base na preferência indicada pelo o usuário

#### Personalização 

Página integrada com o motor de recomendação da API.

- **Preferências:** fluxo guiado onde o usuário seleciona gêneros de interesse e favorita título para alimentar o motor de recomendação

#### Estatísticas

Página com painel para visualização de métricas fornecidas pela API.

### Tecnologias

| Componente | Tecnologia | Versão | Descrição |
| :--- | :--- | :--- | :--- |
| **Frontend/App** | **Streamlit** | `^1.51.0` | Framework para desenvolvimento de aplicativo web |
| **Visualização** | **Plotly** | `^6.5.0` | Biblioteca para criação de gráficos dinâmicos e interativos |
| **Análise de Dados** | **Pandas** | `^2.3.3` | Biblioteca para manipulação de dados |
| **Comunicação** | **Requests** | `^2.32.5` | Biblioteca para requisições HTTP e consumo de API |
| **Sessão** | **Cookies Controller**| `^0.0.3` | Biblioteca para gestão de estados da sessão |
| **Linguagem** | **Python** | `>=3.11, <3.14` | Linguagem para desenvolvimento de scripts |
| **Infraestrutura** | **Docker** | `29.1.1` | Ferramenta de containerização para paridade entre ambientes |
| **Gerenciamento** | **Poetry** | `2.2.1` | Gerenciador de ambientes virtuais para isolamento de dependências |

### Integrações

Este aplicativo web faz requisições a uma API RESTful desenvolvida com Flask que gerencia o banco de dados e um motor de recomendação cujo fluxo de atualização e processamento é orquestrado pelo Apache Airflow.

Link para o repositório da API: https://github.com/postech-mlengineering/postech-ml-techchallenge-fase-1-api

Link para o repositório do Airflow: https://github.com/postech-mlengineering/postech-ml-techchallenge-fase-1-airflow/tree/main

### Deploy

A arquitetura e o deploy foram concebidos para suportar um ecossistema distribuído, utilizando uma instância EC2 na AWS como infraestrutura e Docker para a padronização e o isolamento dos ambientes.

A solução é composta por três camadas de containers integrados:

- **Orquestração (Apache Airflow)**: implementada em containers dedicados, esta camada é responsável pelo agendamento e execução dos pipelines de dados, acionando as rotas de /scrape e /training-data da API

- **API (Flask)**: é o coração da arquitetura. Esta camada interage com o site Books To Scrape para aquisição de dados via web scraping e expõe endpoints para consumo

- **Consumo (Web App Streamlit)**: é a interface web que consome os serviços da API, permitindo que os usuários finais interajam com a API

A comunicação entre os containers é otimizada via Docker network, permitindo a interação entre serviços através de nomes de host em vez de IPs dinâmicos. Essa configuração reduz a latência, elimina custos de tráfego externo e melhora a eficiência ao processar as requisições localmente no host.

Os seviços podem ser acessados nos endereços abaixo:

- **API**: http://18.208.50.37:5000
- **Web App Streamlit**: http://18.208.50.37:8501
- **Apache Airflow**: http://18.208.50.37:8080

#### Persistência

A camada de persistência foi definida em um banco de dados gerenciado via Supabase (integrado à plataforma Vercel). Esta infraestrutura é responsável pela centralização do acervo de livros, pelo histórico de preferências de usuários e pela persistência dos logs de auditoria.

### Link da Apresentação

https://youtu.be/mSAH299OHDs

### Colaboradores

[Jorge Platero](https://github.com/jorgeplatero)

[Leandro Delisposti](https://github.com/LeandroDelisposti)

[Hugo Rodrigues](https://github.com/Nokard)