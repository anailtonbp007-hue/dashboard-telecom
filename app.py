import pandas as pd
import streamlit as st

# Configuração da Página com visual escuro corporativo
st.set_page_config(
    page_title="Consulta de Lojas - Redes & Telecom", page_icon="🌐", layout="wide"
)

# Estilização visual parecida com a referência corporativa
st.markdown(
    """
    <style>
    .main { background-color: #121214; color: #e1e1e6; }
    .stTextInput input { background-color: #202024; color: white; border-radius: 8px; border: 1px solid #29292e; }
    .card { background-color: #202024; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #d90429; }
    </style>
""",
    unsafe_allow_html=True,
)


# Carregando as abas da planilha de forma otimizada
@st.cache_data
def carregar_dados():
  excel_file = "Redes_Telecom_Geral.xlsx"
  info_loja = pd.read_excel(excel_file, sheet_name="Info_Loja")
  detalhes_links = pd.read_excel(excel_file, sheet_name="Detalhes Links Lojas")
  tel_ip = pd.read_excel(excel_file, sheet_name="Telefonia Ip - Lojas")
  return info_loja, detalhes_links, tel_ip


info_loja, detalhes_links, tel_ip = carregar_dados()

# Cabeçalho da aplicação
st.markdown(
    "<h1 style='text-align: center; color: #ff0055;'>Consulta de Lojas</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #a8a8b3;'>Digite o ID da Loja e pressione Enter para consultar os dados de redes e telecom.</p>",
    unsafe_allow_html=True,
)

# Barra de Pesquisa centralizada
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  id_pesquisa = st.text_input("ID Loja", placeholder="Ex: 22, 43, 700...")

if id_pesquisa:
  try:
    id_int = int(id_pesquisa)

    # Filtrar dados nas planilhas
    loja_info = info_loja[info_loja["IDLoja"] == id_int]
    loja_link = detalhes_links[detalhes_links["Loja"] == id_int]
    loja_tel = tel_ip[tel_ip["Loja"] == id_int]

    if not loja_info.empty:
      info = loja_info.iloc[0]
      link = loja_link.iloc[0] if not loja_link.empty else {}
      tel = loja_tel.iloc[0] if not loja_tel.empty else {}

      # Bloco 1: Informações Básicas e Telefonia IP
      c1, c2 = st.columns(2)
      with c1:
        st.markdown(
            f"""
                <div class="card">
                    <h3>🏷️ Consulta de Lojas</h3>
                    <p><b>ID Loja:</b> {info.get('IDLoja', '-')}</p>
                    <p><b>Nome Filial:</b> {info.get('Nome Filial', '-')}</p>
                    <p><b>Ramal Loja:</b> {tel.get('Ramais Criados', '-')}</p>
                    <p><b>Telefone Marisa:</b> {info.get('Telefone Marisa', '-')}</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

      with c2:
        st.markdown(
            f"""
                <div class="card">
                    <h3>📊 Dados de Conectividade</h3>
                    <p><b>Operadora Principal:</b> {link.get('Operadora 1', '-')}</p>
                    <p><b>Banda / Tipo:</b> {link.get('Banda', '-')} ({link.get('Tipo', '-')})</p>
                    <p><b>IP Loopback:</b> {link.get('IP Loopback', '-')}</p>
                    <p><b>S/N Fortigate:</b> {link.get('S/N Fortigate', '-')}</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

      # Bloco 2: Endereço e Dados Cadastrais
      st.markdown(
          f"""
            <div class="card" style="border-left-color: #00b4d8;">
                <h3>📍 Dados de Endereço & Localização</h3>
                <p><b>Endereço:</b> {info.get('Logradouro', '-')} , {info.get('Núm.', '-')}</p>
                <p><b>Complemento:</b> {info.get('Complemento', 'Não Possui')}</p>
                <p><b>Bairro / Cidade / UF:</b> {info.get('Bairro', '-')}, {info.get('Cidade', '-')}/{info.get('UF', '-')}</p>
                <p><b>CEP:</b> {info.get('CEP', '-')} | <b>Região:</b> {info.get('Região Geográfica', '-')}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

    else:
      st.warning(
          "Nenhuma loja encontrada com este ID. Verifique o número digitado."
      )

  except ValueError:
    st.error("Por favor, digite um número de ID válido.")