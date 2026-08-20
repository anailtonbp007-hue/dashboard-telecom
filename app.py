import pandas as pd
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Consulta de Redes & Telecom", page_icon="🌐", layout="wide"
)

# Estilização visual executiva (Dark Theme com cards limpos)
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput input { background-color: #1f2937; color: white; border-radius: 8px; border: 1px solid #374151; font-size: 18px; }
    .card { background-color: #1f2937; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 6px solid #3b82f6; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .card-green { border-left-color: #10b981; }
    .card-purple { border-left-color: #8b5cf6; }
    .card-orange { border-left-color: #f59e0b; }
    h3 { color: #f3f4f6; margin-top: 0; font-size: 20px; }
    p { color: #d1d5db; font-size: 16px; margin-bottom: 8px; }
    </style>
""",
    unsafe_allow_html=True,
)


# Carregando dados de todas as abas necessárias
@st.cache_data(ttl=1)
def carregar_dados():
  excel_file = "Redes_Telecom_Geral.xlsx"
  info_loja = pd.read_excel(excel_file, sheet_name="Info_Loja")
  detalhes_links = pd.read_excel(excel_file, sheet_name="Detalhes Links Lojas")
  tel_ip = pd.read_excel(excel_file, sheet_name="Telefonia Ip - Lojas")
  tel_fixa = pd.read_excel(excel_file, sheet_name="Telefonia Fixa")
  tel_movel = pd.read_excel(excel_file, sheet_name="Telefonia Móvel")
  return info_loja, detalhes_links, tel_ip, tel_fixa, tel_movel


(
    df_info_loja,
    df_detalhes_links,
    df_tel_ip,
    df_tel_fixa,
    df_tel_movel,
) = carregar_dados()

# Título Principal
st.markdown(
    "<h1 style='text-align: center; color: #f43f5e; margin-bottom: 0;'>🌐 Consulta de Redes & Telecom - Lojas</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #9ca3af;'>Digite o ID da Loja para visualizar todas as informações operacionais em tempo real.</p>",
    unsafe_allow_html=True,
)

# Barra de Pesquisa Centralizada
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  id_pesquisa = st.text_input(
      "🔍 Digite o ID da Loja:", placeholder="Ex: 689, 22, 43..."
  )

if id_pesquisa:
  try:
    id_int = int(id_pesquisa)

    # Filtrar dados para a loja buscada
    info = df_info_loja[df_info_loja["IDLoja"] == id_int]
    link = df_detalhes_links[df_detalhes_links["Loja"] == id_int]
    telip = df_tel_ip[df_tel_ip["Loja"] == id_int]
    telfix = df_tel_fixa[df_tel_fixa["Loja"] == id_int]
    telmov = df_tel_movel[df_tel_movel["CR"] == id_int]

    if not info.empty:
      inf = info.iloc[0]
      lnk = link.iloc[0] if not link.empty else {}
      tip = telip.iloc[0] if not telip.empty else {}
      tfx = telfix.iloc[0] if not telfix.empty else {}

      # Cabeçalho da Loja Encontrada
      st.markdown(
          f"""
            <div style="background-color: #111827; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 25px; border: 1px solid #374151;">
                <h2 style="color: #ffffff; margin: 0;">Loja {inf.get('IDLoja', '-')} - {inf.get('Nome Filial', '-')}</h2>
                <p style="margin: 5px 0 0 0; color: #9ca3af;">{inf.get('Logradouro', '-')}, {inf.get('Núm.', '-')} - {inf.get('Bairro', '-')}, {inf.get('Cidade', '-')}/{inf.get('UF', '-')} | CEP: {inf.get('CEP', '-')}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

      # Linha 1: Links e Conectividade vs Telefonia Fixa/IP
      col_a, col_b, col_c = st.columns([2, 1, 1])

      with col_a:
        st.markdown(
            f"""
                <div class="card">
                    <h3>📈 Links & Conectividade</h3>
                    <table style="width:100%; color: #d1d5db; font-size: 15px;">
                        <tr><td><b>Link 1 (Operadora):</b></td><td>{lnk.get('Operadora 1', '-')} ({lnk.get('Banda', '-')})</td></tr>
                        <tr><td><b>Tecnologia 1:</b></td><td>{lnk.get('Tipo', '-')}</td></tr>
                        <tr><td><b>Designação 1:</b></td><td>{lnk.get('Designação ', '-')}</td></tr>
                        <tr><td><b>Link 2 (Backup):</b></td><td>{lnk.get('Operadora 2', '-')} ({lnk.get('Banda.1', '-')})</td></tr>
                        <tr><td><b>Designação 2:</b></td><td>{lnk.get('Designação .1', '-')}</td></tr>
                        <tr><td><b>IP Loja / Loopback:</b></td><td>{lnk.get('IP Loja', '-')} / {lnk.get('IP Loopback', '-')}</td></tr>
                    </table>
                </div>
                """,
            unsafe_allow_html=True,
        )

      with col_b:
        st.markdown(
            f"""
                <div class="card card-green">
                    <h3>📞 Telefonia Fixa & IP</h3>
                    <p><b>Tel Fixo:</b> {tfx.get('Telefone Fixo', '-')}</p>
                    <p><b>Op. Fixo:</b> {tfx.get('Operadora', '-')}</p>
                    <p><b>Hunt Group:</b> {tip.get('Hunt Group', '-')}</p>
                    <p><b>Ramais Criados:</b> {tip.get('Ramais Criados', '-')}</p>
                    <p><b>Qtd APs Ativos:</b> {tip.get('Qtde aps ativos', '-')}</p>
                </div>
                """,
            unsafe_allow_html=True,
        )

      with col_c:
        st.markdown(
            f"""
                <div class="card card-purple">
                    <h3>🔐 Equipamento & Custos</h3>
                    <p><b>S/N Fortigate:</b><br><span style="color: #60a5fa; font-family: monospace; font-size: 18px;">{lnk.get('S/N Fortigate', '-')}</span></p>
                    <hr style="border-color: #374151;">
                    <p><b>Custo Total de Links:</b><br><span style="color: #34d399; font-size: 22px; font-weight: bold;">R$ {lnk.get('Custo Total de Links', 0):,.2f}</span></p>
                </div>
                """,
            unsafe_allow_html=True,
        )

      # Linha 2: Telefonia Móvel e Outros Detalhes
      st.markdown("### 📱 Detalhes de Telefonia Móvel")
      if not telmov.empty:
        st.dataframe(
            telmov[["Operadora", "Plano", "Conta", "Numero", "Valor"]],
            use_container_width=True,
        )
      else:
        st.info("Nenhum registro de Telefonia Móvel localizado para esta loja.")

    else:
      st.warning(
          "⚠️ Nenhuma loja encontrada com este ID. Verifique o número digitado."
      )

  except ValueError:
    st.error("Por favor, digite apenas números válidos para o ID da Loja.")
