import streamlit as st
import google.generativeai as genai
import ast
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

MAX_LINES = 150

def is_valid_python_code(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

st.set_page_config(
    page_title="DocString Genius 🤖",
    page_icon="💡",
    layout="wide"
)

st.title("💡 DocString Genius: O Analista IA de Python")
st.markdown(
    "Cole uma função Python abaixo para receber informações completa, análise de complexidade e sugestões de melhoria.")

st.sidebar.header("⚙️ Configurações")
try:
    api_key = os.getenv("GOOGLE_API_KEY")
except (FileNotFoundError, KeyError):
    api_key = st.sidebar.text_input("Cole sua API Key do Google Gemini aqui:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Por favor, insira sua API Key do Google Gemini na barra lateral para continuar.")
    st.stop()

estilos_docstring = ['Google', 'NumPy', 'reStructuredText (Padrão)']
estilo_selecionado = st.sidebar.selectbox(
    "Escolha o Estilo da Docstring:",
    options=estilos_docstring
)
st.sidebar.markdown("---")
st.sidebar.info(f"Limite de análise: {MAX_LINES} linhas de código.")

def construir_prompt_mestre(codigo, estilo):
    prompt = f"""
    Sua tarefa é atuar como um programador Python Sênior e especialista em qualidade de código.
    Analise a seguinte função Python e gere um relatório completo com quatro seções distintas.
    Use EXATAMENTE os seguintes marcadores para separar as seções: ### EXPLICACAO, ### DOCSTRING, ### ANALISE DE COMPLEXIDADE, ### SUGESTOES DE MELHORIA.

    ### EXPLICACAO
    Escreva uma explicação clara e concisa, em formato de lista (passo a passo), do que a função faz. O público-alvo é um programador júnior.

    ### DOCSTRING
    Gere uma docstring completa no formato {estilo}. A docstring deve incluir: um resumo, descrição dos argumentos (Args) com tipos, e a descrição do retorno (Returns) com tipo. Coloque a docstring dentro de um bloco de código Python.

    ### ANALISE DE COMPLEXIDADE
    Determine a complexidade de tempo (Big O Notation) da função. Forneça a notação e uma justificativa muito breve (uma linha) para sua análise.

    ### SUGESTOES DE MELHORIA
    Forneça uma lista de sugestões para melhorar o código, focando em legibilidade e código "Pythônico". Se o código já estiver excelente, apenas elogie.

    Aqui está o código para analisar:
    ```python
    {codigo}
    ```
    """
    return prompt

# --- Interface Principal ---
st.subheader("Cole sua função Python aqui:")
codigo_usuario = st.text_area(
    "Caixa de texto para o código", height=250, label_visibility="collapsed",
    placeholder="def buscar_elemento(lista, elemento):\n    for i in range(len(lista)):\n        if lista[i] == elemento:\n            return i\n    return -1"
)

if st.button("Analisar Código ✨"):
    if codigo_usuario and api_key:

        linhas_codigo = codigo_usuario.split('\n')
        if len(linhas_codigo) > MAX_LINES:
            st.error(f"❌ Erro: O código inserido excede o limite de {MAX_LINES} linhas. Por favor, envie um trecho menor.")

        elif not is_valid_python_code(codigo_usuario):
            st.error(
                "❌ Erro: O texto inserido não parece ser um código Python válido. Por favor, verifique e tente novamente.")
        else:
            with st.spinner("🧠 O Genius está pensando... Analisando, documentando e buscando melhorias..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    prompt_final = construir_prompt_mestre(codigo_usuario, estilo_selecionado)
                    response = model.generate_content(prompt_final)

                    st.subheader("Relatório de Análise do Código:")
                    partes = response.text.split("###")
                    explicacao, docstring, complexidade, sugestoes = "", "", "", ""

                    for parte in partes:
                        if "EXPLICACAO" in parte:
                            explicacao = parte.replace("EXPLICACAO", "").strip()
                        elif "DOCSTRING" in parte:
                            docstring = parte.replace("DOCSTRING", "").strip()
                        elif "ANALISE DE COMPLEXIDADE" in parte:
                            complexidade = parte.replace("ANALISE DE COMPLEXIDADE", "").strip()
                        elif "SUGESTOES DE MELHORIA" in parte:
                            sugestoes = parte.replace("SUGESTOES DE MELHORIA", "").strip()

                    col1, col2 = st.columns(2)
                    with col1:
                        if explicacao: st.markdown("#### 📖 Explicação da Função"); st.markdown(explicacao)
                        if complexidade: st.markdown("#### 🧠 Análise de Complexidade"); st.info(complexidade)
                        if sugestoes: st.markdown("#### 💡 Sugestões de Melhoria"); st.warning(sugestoes)
                    with col2:
                        if docstring: st.markdown(f"#### 📝 Docstring (Estilo {estilo_selecionado})"); st.code(docstring,
                                                                                                              language='python')
                except Exception as e:
                    st.error(f"Ocorreu um erro ao chamar a API do Gemini: {e}")
    elif not api_key:
        st.error("Erro: A API Key do Gemini não foi configurada.")
    else:
        st.warning("Por favor, cole um trecho de código para analisar.")