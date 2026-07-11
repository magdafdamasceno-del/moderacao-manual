import streamlit as st
from google import genai

# Configuração visual da página
st.set_page_config(page_title="Gerador de Respostas RA", layout="wide")

st.title("🛡️ Gerador de Respostas Blindadas - Reclame AQUI")
st.caption("Crie respostas automáticas e factuais para garantir o sucesso de moderações futuras.")

# Mantemos vazio para você colar na tela com segurança
MINHA_CHAVE_FIXA = "" 

client = None

if MINHA_CHAVE_FIXA:
    client = genai.Client(api_key=MINHA_CHAVE_FIXA)
else:
    # Cria o campo na barra lateral para você colar a chave que gerou no AI Studio
    api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")
    if api_key:
        client = genai.Client(api_key=api_key)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dados da Reclamação")
    descricao = st.text_area("Cole aqui o Relato/Descrição do Cliente:", height=250)
    replica = st.text_area("Cole a Réplica (Se houver, para casos de reanálise):", height=150)
    
    botao_gerar = st.button("✨ Criar Resposta Blindada")

with col2:
    st.subheader("🤖 Resposta Sugerida pela IA")
    
    if botao_gerar:
        if client is None:
            st.error("⚠️ Por favor, abra a barra lateral esquerda e insira a sua Gemini API Key.")
        elif not descricao.strip():
            st.error("⚠️ Por favor, cole pelo menos o relato do cliente para gerar a resposta.")
        else:
            with st.spinner("Analisando o manual do RA e blindando o texto..."):
                prompt_sistema = f"""
                Você é um redator especialista em atendimento de alta performance e defesa corporativa no Reclame AQUI.
                Sua tarefa é ler o relato do cliente (e a réplica se houver) e criar uma RESPOSTA PÚBLICA que blinde a empresa para uma futura moderação na categoria "A empresa não violou o direito do cliente" ou "Este é um caso de fraude".

                [REGRAS DE OURO DO MANUAL DO RA PARA INCLUIR NA RESPOSTA]
                1. Se o caso envolver regras de promoção ou termos de uso, cite termos técnicos, itens exatos do regulamento e dados numéricos/fatos de forma incontestável.
                2. Se o erro foi do cliente (perda de prazos, falta de dados), evidencie isso de forma extremamente educada e factual.
                3. NUNCA use frases genéricas como "enviamos um e-mail". O robô do RA exige respostas condizentes no conteúdo público.
                4. EVITE adjetivos ou lamentações excessivas que o robô do RA interprete como "Falha no Atendimento" ou assunção de culpa por erros operacionais.

                DADOS ENVIADOS:
                - RELATO DO CLIENTE: {descricao}
                - RÉPLICA DO CLIENTE: {replica}

                Gere o retorno estruturado assim:
                ### 🛑 Alerta de Risco de Moderação
                (Diga se o relato tem risco de carimbo CO06 (Divergência) ou CO01 (Inelegível) por falha operacional, ou se a chance de moderação futura é ALTA).

                ### 📝 Resposta Pública Pronta (Copie e Cole)
                (Insira aqui o texto completo da resposta blindada, polida, profissional e factual, pronta para publicar).
                """
                
                try:
                    # Roda usando o modelo estável mais recente
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt_sistema,
                    )
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {e}")
