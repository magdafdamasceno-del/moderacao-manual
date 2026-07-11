import streamlit as st
import google.generativeai as genai
import os

# Configuração da página
st.set_page_config(page_title="Reclame AI", layout="wide")

# Título
st.title("🛡️ Reclame AI - Assistente de Moderação")

# Configuração da API (Busca do painel de Secrets do Streamlit Cloud)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')
except Exception as e:
    st.error("Erro na configuração da chave de API. Verifique as 'Secrets' no Streamlit Cloud.")

# Interface
tipo_caso = st.selectbox("Tipo de Caso", ["Fraude", "Cobrança", "Promoção", "Entrega", "Cadastro"])
descricao = st.text_area("Relato da Reclamação:", height=200)
resposta_atual = st.text_area("Resposta da Empresa (opcional):", height=150)

if st.button("ANALISAR CASO"):
    if descricao:
        with st.spinner("Analisando riscos e gerando resposta..."):
            prompt = f"""
            Atue como especialista em moderação do Reclame AQUI.
            Tipo: {tipo_caso}
            Relato: {descricao}
            Resposta Atual: {resposta_atual}
            
            Gere uma análise de riscos e uma proposta de resposta factual.
            """
            try:
                response = model.generate_content(prompt)
                st.markdown("### Resultado da Análise:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")
    else:
        st.warning("Por favor, cole a descrição da reclamação.")
