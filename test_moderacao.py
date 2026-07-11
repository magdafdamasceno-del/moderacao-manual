import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Gerador de Respostas RA", layout="wide")

st.title("🛡️ Gerador de Respostas Blindadas - Reclame AQUI")

# Barra lateral para configurar a API Key de forma segura
api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

# Configuração do Modelo
if api_key:
    genai.configure(api_key=api_key)
    # Usando o modelo estável que possui cota gratuita garantida
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.sidebar.warning("Por favor, insira sua chave no campo acima para começar.")

# Layout do formulário
col1, col2 = st.columns(2)

with col1:
    st.subheader("Dados da Reclamação")
    descricao = st.text_area("Relato do Cliente:", height=150)
    resposta_atual = st.text_area("Resposta Atual (Opcional):", height=100)
    replica = st.text_area("Réplica do Cliente (Opcional):", height=100)
    botao_gerar = st.button("✨ Criar Resposta Blindada")

with col2:
    st.subheader("🤖 Resposta Sugerida")
    if botao_gerar:
        if not api_key:
            st.error("⚠️ Insira sua chave de API na barra lateral.")
        elif not descricao:
            st.error("⚠️ O relato é obrigatório.")
        else:
            try:
                with st.spinner("Analisando e gerando resposta..."):
                    prompt = f"""
                    Você é um redator especialista em atendimento de alta performance no Reclame AQUI.
                    Analise o caso abaixo e crie uma resposta factual que evite falhas operacionais:
                    
                    Relato: {descricao}
                    Resposta Atual: {resposta_atual}
                    Réplica: {replica}
                    
                    Gere a resposta com foco em fatos e termos técnicos.
                    """
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro ao conectar com o Gemini: {e}")
