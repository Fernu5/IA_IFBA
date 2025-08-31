# DocString Genius: Analista de Código Python com IA

# O que é?
DocString Genius é uma aplicação inteligente, construída em Python, que atua como um assistente de qualidade de código para desenvolvedores. 
Utilizando o poder de um grande modelo de linguagem (LLM) do Google Gemini, a ferramenta analisa funções ou classes Python e gera automaticamente informação completa sobre elas, 
além de possiveis melhorias valiosas sobre o código.

# Objetivo Principal
O objetivo do projeto é resolver um problema comum e muitas vezes negligenciado no ciclo de desenvolvimento de software: a documentação de código. A ferramenta visa:
Economizar Tempo: Automatizar a criação de docstrings e explicações, tarefas que podem ser demoradas.
Padronizar a Qualidade: Garantir que a documentação seja consistente, completa e siga padrões como os estilos Google, NumPy e reStructuredText.
Acelerar o Aprendizado: Ajudar programadores, especialmente os mais iniciantes, a entender rapidamente o funcionamento, a complexidade e as possíveis melhorias em trechos de código.

# O que ele faz?
Ao colar um trecho de código Python na interface, o DocString Genius realiza uma análise completa e retorna quatro informações principais:
1. Explicação Simples: Gera um texto em linguagem natural, passo a passo, explicando o que o código faz, ideal para revisões e integração de novos membros na equipe.
2. Geração de Docstring: Cria uma docstring profissional e pronta para ser usada, com suporte para diferentes estilos de formatação.
3. Análise de Complexidade: Calcula e exibe a complexidade de tempo do algoritmo, fornecendo uma justificativa curta e direta.
4. Sugestões de Melhoria: Oferece recomendações para melhorar o código, sugerindo nomes de variáveis mais claros e outras boas práticas.

# Tecnologias Utilizadas
Linguagem Principal: Python 3
Inteligência Artificial: Google Gemini (gemini-1.5-flash-latest)
Utilizei a API do Gemini para as tarefas de compreensão, análise e geração de texto e código.
Interface: Streamlit - Uma biblioteca Python que permite criar interfaces web interativas com poucas linhas de código, ideal para prototipagem rápida.
Validação de Código: Módulo ast do Python - Usado para verificar se o texto inserido pelo usuário é sintaticamente um código Python válido antes de enviá-lo para a API.
Gerenciamento de Chaves de API: Python Dotenv - Para carregar as chaves de API a partir de um arquivo .env (O que está no repositorio está sem a KEY), evitando expô-las no código-fonte.

# Como foi Feito?
O funcionamento do DocString Genius segue um fluxo lógico e robusto que construímos passo a passo:
1. Interface Interativa: O Streamlit renderiza a página web com uma área de texto para o código do usuário e uma barra lateral para configurações (estilo da docstring e chave de API).
2. Validação em Camadas: Antes de qualquer processamento caro ou seja que custe cota na API, o aplicativo realiza múltiplas verificações:
   Limite de Linhas: Garante que o código não exceda um número pré-definido de linhas (150) para controlar o uso da API.
   Sintaxe Python: Usa o módulo ast para confirmar que a entrada é um código Python válido, rejeitando textos comuns ou malformados.
3. Engenharia de Prompt ("Prompt Mestre"): O coração do agente é um prompt cuidadosamente elaborado que instrui o modelo Gemini a realizar todas as tarefas de uma só vez e a formatar
    a saída com marcadores específicos (ex: "### EXPLICACAO", "### DOCSTRING").
4.  Comunicação com a API: O código validado é enviado ao modelo Gemini junto com o prompt mestre.
5.  Análise e Exibição: A resposta da API é recebida, dividida usando os marcadores, e cada seção é exibida de forma organizada na interface do Streamlit, usando componentes visuais
    diferentes para cada tipo.

# Como Executar o Projeto
Siga os passos abaixo para rodar o DocString Genius localmente.
1. Pré-requisitos: Ter o Python 3.7 ou superior instalado.
2. Instale as dependências:
    streamlit
    google-generativeai
    python-dotenv
3. Configure sua Chave de API: Crie um arquivo chamado .env na raiz do projeto. Dentro deste arquivo, adicione sua chave da API do Google Gemini:
    GOOGLE_API_KEY="CHAVE_AQUI"
5. Execute a aplicação: No seu terminal, rode o seguinte comando:
    streamlit run DocString.py
6. A aplicação será aberta automaticamente no seu navegador. Então só seguir as instruções em tela.
