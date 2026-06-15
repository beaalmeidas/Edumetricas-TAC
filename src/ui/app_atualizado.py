import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


st.set_page_config(
    page_title="Edumetricas",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    .metric-card {
        background: #F8FAFF;
        border: 1px solid #E2E8F8;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-card .label {
        font-size: 18px;
        font-weight: 600;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #334155;
        margin-bottom: 6px;
    }
    .metric-card .value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #1E3A6E;
    }
    .metric-card .sub {
        font-size: 16px;
        color: #475569; 
        margin-top: 4px;
    }
    .badge-aprovado    { background:#DCFCE7; color:#166534; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-recuperacao { background:#FEF9C3; color:#854D0E; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-reprovado   { background:#FEE2E2; color:#991B1B; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 25px;
        font-weight: 700;
        color: #1E3A6E;
        border-left: 4px solid #3B6FE0;
        padding-left: 12px;
        margin: 28px 0 16px;
    }
    [data-testid="stSidebar"] { background: #1E3A6E; }
    [data-testid="stSidebar"] * { color: #E2EAFF !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label { color: #CBD5F0 !important; font-size:13px; }
    [data-testid="stSidebarNav"] a { color: #CBD5F0 !important; } [data-testid="stAppViewContainer"] {
        background: #F9FAFB;
    }

    div[data-baseweb="tab-list"] button[data-baseweb="tab"] p {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1E293B !important;
        padding: 10px 20px !important;
    }

    div[data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #1E3A6E !important;
    }

    h1 {
        color: #0F172A !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #334155 !important;
    }

    div[data-testid="stSelectbox"] div:has(select[id*="disc_saeb"]) + label,
    div[data-testid="stSelectbox"] label:has(+ div select[id*="disc_saeb"]) {
        font-size: 20px !important;
        color: #000000 !important;
        font-weight: 700;
    }
            
    div[data-testid="stSelectbox"][key="disc_aba2"] label {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }
            
    div[data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #0F172A !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #64748B !important;
    }

    div[data-testid="stRadio"] label span {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    /* Cartão de perfil de professor */
    .prof-card {
        background: #F8FAFF;
        border: 1px solid #E2E8F8;
        border-radius: 14px;
        padding: 20px 24px;
    }
    .prof-card .prof-id {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #1E3A6E;
    }
    .prof-card .prof-disc {
        font-size: 14px;
        color: #64748B;
        margin-top: 2px;
    }
    .prof-card .prof-stat {
        margin-top: 14px;
        font-size: 13px;
        color: #334155;
    }
    .prof-card .prof-stat b {
        font-size: 22px;
        font-family: 'Space Grotesk', sans-serif;
        color: #0F172A;
    }

    /* Cartão de perfil do aluno */
    .aluno-header {
        background: linear-gradient(135deg, #1E3A6E 0%, #3B6FE0 100%);
        border-radius: 16px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
    }
    .aluno-header .aluno-nome {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .aluno-header .aluno-sub {
        font-size: 16px;
        opacity: 0.85;
    }
    .aluno-header .aluno-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        margin-top: 10px;
    }
    .badge-green  { background: #DCFCE7; color: #166534; }
    .badge-red    { background: #FEE2E2; color: #991B1B; }
    .badge-yellow { background: #FEF9C3; color: #854D0E; }

    .mini-stat {
        background: #F8FAFF;
        border: 1px solid #E2E8F8;
        border-radius: 10px;
        padding: 14px 18px;
        text-align: center;
    }
    .mini-stat .ms-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .06em;
        color: #64748B;
        margin-bottom: 4px;
    }
    .mini-stat .ms-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)


# CONSTANTES ----------------------------------
CORES_FAIXAS = {
    'Insuficiente': '#EF4444',
    'Básico':       '#F97316',
    'Adequado':     '#3B82F6',
    'Avançado':     '#22C55E',
}
FAIXAS_ORDEM = ['Insuficiente', 'Básico', 'Adequado', 'Avançado']
BIMESTRES    = ['1º Bim', '2º Bim', '3º Bim', '4º Bim']
COLS_MEDIA   = ['media_b1','media_b2','media_b3','media_b4']
COLS_FREQ    = ['frequencia_b1','frequencia_b2','frequencia_b3','frequencia_b4']
LIMITE_APROV = 7.0
UF_ESCOLA    = 'PB'

DISC_SAEB = {
    'Matemática': 'MT',
    'Linguagens': 'LP',
}

CORES_PROF = [
    '#3B6FE0','#F97316','#22C55E','#EF4444','#A855F7',
    '#14B8A6','#F59E0B','#EC4899','#6366F1','#10B981','#F43F5E','#0EA5E9'
]


# CARREGAMENTO DE DADOS -----------------------
@st.cache_data
def carregar_dados():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    BASE = os.path.join(BASE_DIR, 'data', 'internal')
    EXT  = os.path.join(BASE_DIR, 'data', 'external')

    df = pd.read_csv(os.path.join(BASE, 'output', 'consolidado.csv'), dtype={'id_aluno': str})
    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], dayfirst=True, errors='coerce')

    saeb_br = pd.read_csv(os.path.join(EXT, 'br_inep_saeb_brasil.csv'))
    saeb_uf = pd.read_csv(os.path.join(EXT, 'br_inep_saeb_uf.csv'))
    enem    = pd.read_csv(os.path.join(EXT, 'enem_2024_amostra.csv'))

    saeb_br = saeb_br[(saeb_br['ano'] >= 2013) & (saeb_br['serie'] == 12)].copy()
    saeb_uf = saeb_uf[
        (saeb_uf['ano'] >= 2013) &
        (saeb_uf['serie'] == 12) &
        (saeb_uf['sigla_uf'] == UF_ESCOLA)
    ].copy()

    enem_map = {
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
    }
    enem = enem[list(enem_map.keys())].dropna().rename(columns=enem_map)
    for c in enem.columns:
        enem[c] = enem[c] / 100  # normaliza 0-1000 → 0-10

    return df, saeb_br, saeb_uf, enem


df_full, saeb_br, saeb_uf, enem = carregar_dados()


# SIDEBAR -------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="font-size:35px; font-weight:700; margin-bottom:10px; margin-top:-40px; text-align:center;">
        Edumetricas
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("# Filtros")

    series_opts  = ['Todas'] + sorted(df_full['serie'].unique().tolist())
    serie_sel    = st.selectbox("Série", series_opts)

    turmas_disp  = sorted(df_full[
        df_full['serie'] == serie_sel if serie_sel != 'Todas' else df_full['serie'].notna()
    ]['turma'].unique().tolist())
    turma_opts   = ['Todas'] + turmas_disp
    turma_sel    = st.selectbox("Turma", turma_opts)

    disc_opts    = ['Todas'] + sorted(df_full['disciplina'].unique().tolist())
    disc_sel     = st.selectbox("Disciplina", disc_opts)

    faixa_opts   = ['Todas'] + FAIXAS_ORDEM
    faixa_sel    = st.selectbox("Faixa de desempenho", faixa_opts)

    st.markdown("---")


# FILTROS -------------------------------------
df = df_full.copy()
if serie_sel  != 'Todas': df = df[df['serie']            == serie_sel]
if turma_sel  != 'Todas': df = df[df['turma']            == turma_sel]
if disc_sel   != 'Todas': df = df[df['disciplina']       == disc_sel]
if faixa_sel  != 'Todas': df = df[df['faixa_desempenho'] == faixa_sel]


# NAVBAR --------------------------------------
aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "Visão geral",
    "Desempenho por matéria",
    "Evolução bimestral",
    "Estatísticas nacionais",
    "Análise de professores",
    "Perfil do aluno",
])


# ABA 1: VISAO GERAL --------------------------
with aba1:
    st.markdown("# Visão geral do conjunto")
    filtro_desc = " · ".join(filter(lambda x: x != 'Todas', [serie_sel, turma_sel, disc_sel])) or "Escola completa"
    st.markdown(f"""
        <div style="font-size:20px; color:#334155; margin-bottom:30px; margin-top:-15px;">
            Filtro ativo: <b>{filtro_desc}</b> | {df['id_aluno'].nunique()} alunos · {len(df)} registros
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    n_alunos    = df['id_aluno'].nunique()
    media_geral = df['media_anual'].mean()
    freq_media  = df['frequencia_anual'].mean() * 100
    em_risco    = df[df['media_anual'] < LIMITE_APROV]['id_aluno'].nunique()
    pct_aprov   = (df['situacao'] == 'Aprovado').mean() * 100

    for col, label, val, sub in zip(
        [col1, col2, col3, col4, col5],
        ['Alunos', 'Média Geral', 'Freq. Média', 'Em Risco', 'Tx. Aprovação'],
        [n_alunos, f"{media_geral:.2f}", f"{freq_media:.1f}%", em_risco, f"{pct_aprov:.1f}%"],
        ['registros únicos', 'escala 0–10', 'presença anual', 'alunos', 'no ano letivo']
    ):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{val}</div>
            <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<br />')

    st.markdown('<div class="section-title">Desempenho por faixa e Médias por série e disciplina</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.8], vertical_alignment="top")

    with c1:
        faixas = df['faixa_desempenho'].value_counts().reindex(FAIXAS_ORDEM).fillna(0)
        fig_pizza = px.pie(
            values=faixas.values,
            names=faixas.index,
            color=faixas.index,
            color_discrete_map=CORES_FAIXAS,
            hole=0.5,
        )
        fig_pizza.update_traces(textposition='inside', textinfo='percent+label', textfont_size=20)
        fig_pizza.update_layout(legend=dict(font=dict(size=14)), margin=dict(t=20, b=10, l=20, r=20), height=420)
        st.plotly_chart(fig_pizza, width='stretch')

    with c2:
        media_heatmap = (
            df.groupby(['serie','disciplina'])['media_anual']
            .mean().round(2).unstack()
        )
        fig_heat = px.imshow(
            media_heatmap, text_auto=True,
            color_continuous_scale='RdYlGn', zmin=0, zmax=10,
            labels=dict(x='Disciplina', y='Série', color='Média'), height=420,
        )
        fig_heat.update_layout(margin=dict(t=10, b=10), font=dict(size=16))
        fig_heat.update_xaxes(tickfont=dict(size=14), title_font=dict(size=16))
        fig_heat.update_yaxes(tickfont=dict(size=14), title_font=dict(size=16))
        fig_heat.update_coloraxes(colorbar_tickfont=dict(size=14), colorbar_title_font=dict(size=16))
        st.plotly_chart(fig_heat, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">Situação dos alunos</div>', unsafe_allow_html=True)
    sit = df.groupby(['disciplina','situacao']).size().reset_index(name='n')
    fig_sit = px.bar(
        sit, x='n', y='disciplina', color='situacao',
        color_discrete_map={
            'Aprovado': '#22C55E',
            'Recuperação': '#F59E0B',
            'Reprovado (nota)': '#EF4444',
            'Reprovado (falta)': '#F97316',
        },
        orientation='h', height=300,
        labels={'n': 'Alunos', 'disciplina': '', 'situacao': 'Situação'},
    )
    fig_sit.update_layout(margin=dict(t=10,b=10), legend=dict(orientation='h', y=-0.3))
    st.plotly_chart(fig_sit, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">Alunos em risco</div>', unsafe_allow_html=True)
    df_risco = df[
        df['media_anual'] < LIMITE_APROV
    ][['nome','serie','turma','disciplina','media_anual','frequencia_anual','situacao']]\
        .sort_values('media_anual').drop_duplicates()

    st.dataframe(
        df_risco.rename(columns={
            'nome': 'Aluno', 'serie': 'Série', 'turma': 'Turma',
            'disciplina': 'Disciplina', 'media_anual': 'Média',
            'frequencia_anual': 'Frequência', 'situacao': 'Situação'
        }).style.format({'Média': '{:.2f}', 'Frequência': '{:.1%}'}),
        width='stretch', height=280
    )


# ABA 2: DESEMPENHO POR MATERIA ---------------
with aba2:
    st.markdown("# Desempenho por matéria")

    st.markdown("""
        <div style="font-size:18px; color:#000; margin-bottom:-25px">
        Selecione a disciplina:
        </div>
    """, unsafe_allow_html=True)

    disc_aba2 = st.selectbox("", sorted(df_full['disciplina'].unique()), key='disc_aba2')
    df2 = df[df['disciplina'] == disc_aba2]

    c1, c2, c3 = st.columns(3)
    media_val = f"{df2['media_anual'].mean():.2f}"
    freq_val  = f"{df2['frequencia_anual'].mean()*100:.1f}%"
    ativ_val  = f"{df2['taxa_atividades_anual'].mean()*100:.1f}%"

    c1.markdown(f"""
        <div style="background: #F8FAFF; border: 1px solid #E2E8F8; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 16px; font-weight: 600; color: #000000; margin-bottom: 8px; text-transform: uppercase; letter-spacing: .05em;">Média da disciplina</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 36px; font-weight: 700; color: #000000;">{media_val}</div>
        </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
        <div style="background: #F8FAFF; border: 1px solid #E2E8F8; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 16px; font-weight: 600; color: #000000; margin-bottom: 8px; text-transform: uppercase; letter-spacing: .05em;">Frequência média no ano</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 36px; font-weight: 700; color: #000000;">{freq_val}</div>
        </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
        <div style="background: #F8FAFF; border: 1px solid #E2E8F8; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 16px; font-weight: 600; color: #000000; margin-bottom: 8px; text-transform: uppercase; letter-spacing: .05em;">Taxa de atividades realizadas</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 36px; font-weight: 700; color: #000000;">{ativ_val}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<br />')

    st.markdown('<div class="section-title">Distribuição das notas</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig_hist = px.histogram(
            df2, x='media_anual', nbins=25,
            color_discrete_sequence=['#3B6FE0'],
            labels={'media_anual': 'Média Anual', 'count': 'Alunos'},
            title='Histograma de médias'
        )
        fig_hist.add_vline(x=LIMITE_APROV, line_dash='dash', line_color='red',
                            annotation_text='Mínimo aprovação')
        fig_hist.update_layout(height=320, margin=dict(t=40,b=10))
        st.plotly_chart(fig_hist, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">Notas por prova e bimestre</div>', unsafe_allow_html=True)
    provas_cols = {
        'P1 — 1º Bim': 'nota_p1_b1', 'P2 — 1º Bim': 'nota_p2_b1',
        'P1 — 2º Bim': 'nota_p1_b2', 'P2 — 2º Bim': 'nota_p2_b2',
        'P1 — 3º Bim': 'nota_p1_b3', 'P2 — 3º Bim': 'nota_p2_b3',
        'P1 — 4º Bim': 'nota_p1_b4', 'P2 — 4º Bim': 'nota_p2_b4',
    }
    medias_provas = {k: df2[v].mean() for k, v in provas_cols.items()}
    fig_provas = go.Figure(go.Bar(
        x=list(medias_provas.keys()),
        y=list(medias_provas.values()),
        marker_color=['#3B6FE0','#60A5FA'] * 4,
        text=[f'{v:.2f}' for v in medias_provas.values()],
        textposition='outside',
    ))
    fig_provas.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                          annotation_text='Mínimo aprovação')
    fig_provas.update_layout(height=320, margin=dict(t=10,b=10), yaxis=dict(range=[0,11]))
    st.plotly_chart(fig_provas, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">Desempenho por turma</div>', unsafe_allow_html=True)
    media_turma = df2.groupby('turma')['media_anual'].mean().round(2).reset_index()
    fig_turma = px.bar(
        media_turma.sort_values('turma'), x='turma', y='media_anual',
        color='media_anual', color_continuous_scale='RdYlGn', range_color=[0, 10],
        text='media_anual', labels={'turma': 'Turma', 'media_anual': 'Média'},
    )
    fig_turma.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red')
    fig_turma.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_turma.update_layout(height=320, margin=dict(t=10,b=10),
                             coloraxis_showscale=False, yaxis=dict(range=[0,11]))
    st.plotly_chart(fig_turma, width='stretch')


# ABA 3: EVOLUÇÃO BIMESTRAL -------------------
with aba3:
    st.markdown("# Evolução bimestral")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<p style="font-size: 18px; color: #000000; margin-bottom: 10px;">Agrupar por:</p>', unsafe_allow_html=True)
        agrup = st.selectbox(
            "Agrupar por", ['Escola toda', 'Série', 'Turma', 'Disciplina'],
            key='agrup_bim', label_visibility="collapsed"
        )
    with c2:
        st.markdown('<p style="font-size: 18px; color: #000000; margin-bottom: 10px;">Métrica:</p>', unsafe_allow_html=True)
        metrica = st.selectbox(
            "Métrica", ['Média das notas', 'Frequência'],
            key='metrica_bim', label_visibility="collapsed"
        )

    cols_bim = COLS_MEDIA if metrica == 'Média das notas' else COLS_FREQ
    ylabel   = 'Média' if metrica == 'Média das notas' else 'Frequência'
    mult     = 1 if metrica == 'Média das notas' else 100

    def build_evolucao(df_in, group_col=None):
        if group_col:
            grp = df_in.groupby(group_col)[cols_bim].mean() * mult
            grp.columns = BIMESTRES
            grp = grp.reset_index().melt(id_vars=group_col, var_name='Bimestre', value_name=ylabel)
            grp = grp.rename(columns={group_col: 'Grupo'})
        else:
            grp = df_in[cols_bim].mean() * mult
            grp.index = BIMESTRES
            grp = grp.reset_index()
            grp.columns = ['Bimestre', ylabel]
            grp['Grupo'] = 'Escola'
        return grp

    if agrup == 'Escola toda':
        ev = build_evolucao(df)
    elif agrup == 'Série':
        ev = build_evolucao(df, 'serie')
    elif agrup == 'Turma':
        ev = build_evolucao(df, 'turma')
    else:
        ev = build_evolucao(df, 'disciplina')

    fig_ev = px.line(ev, x='Bimestre', y=ylabel, color='Grupo', markers=True,
                     labels={ylabel: ylabel, 'Bimestre': ''})
    if metrica == 'Média das notas':
        fig_ev.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                          annotation_text='Mínimo aprovação')
    fig_ev.update_traces(line=dict(width=2.5), marker=dict(size=8))
    fig_ev.update_layout(height=420, margin=dict(t=20,b=10))
    st.plotly_chart(fig_ev, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">Variação entre bimestres</div>', unsafe_allow_html=True)

    if agrup == 'Escola toda':
        pivot = ev.set_index('Bimestre')[ylabel].to_frame().T
        pivot.index = ['Escola']
    else:
        pivot = ev.pivot(index='Grupo', columns='Bimestre', values=ylabel)[BIMESTRES]

    pivot['Dif. 1° → 2°']  = (pivot['2º Bim'] - pivot['1º Bim']).round(2)
    pivot['Dif.  2° → 3°'] = (pivot['3º Bim'] - pivot['2º Bim']).round(2)
    pivot['Dif. 3° → 4°']  = (pivot['4º Bim'] - pivot['3º Bim']).round(2)

    def color_delta(val):
        if isinstance(val, float):
            color = '#22C55E' if val > 0 else ('#EF4444' if val < 0 else '#64748B')
            return f'color: {color}; font-weight: 600'
        return ''

    st.dataframe(
        pivot.round(2).style.map(color_delta, subset=['Dif. 1° → 2°', 'Dif.  2° → 3°', 'Dif. 3° → 4°']),
        width='stretch'
    )

    st.markdown('<br />')

    st.markdown('<div class="section-title">Comparar duas turmas</div>', unsafe_allow_html=True)
    turmas_disp_all = sorted(df_full['turma'].unique().tolist())
    ca, cb = st.columns(2)
    ca.markdown('<p style="font-size: 18px; color: #000000; margin-bottom: 10px;">Turma 1:</p>', unsafe_allow_html=True)
    turma_a = ca.selectbox("Turma 1", turmas_disp_all, key='ta', label_visibility="collapsed")
    cb.markdown('<p style="font-size: 18px; color: #000000; margin-bottom: 10px;">Turma 2:</p>', unsafe_allow_html=True)
    turma_b = cb.selectbox("Turma 2", turmas_disp_all, index=1, key='tb', label_visibility="collapsed")

    def media_bim_turma(turma):
        sub = df_full[df_full['turma'] == turma]
        return sub[cols_bim].mean() * mult

    df_comp = pd.DataFrame({
        turma_a: media_bim_turma(turma_a).values,
        turma_b: media_bim_turma(turma_b).values,
    }, index=BIMESTRES)

    fig_comp = go.Figure()
    for col, cor in zip([turma_a, turma_b], ['#3B6FE0','#F97316']):
        fig_comp.add_trace(go.Scatter(
            x=df_comp.index, y=df_comp[col],
            name=col, mode='lines+markers',
            line=dict(width=2.5, color=cor), marker=dict(size=8),
        ))
    if metrica == 'Média das notas':
        fig_comp.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red')
    fig_comp.update_layout(height=340, margin=dict(t=10,b=10), yaxis_title=ylabel)
    st.plotly_chart(fig_comp, width='stretch')


# ABA 4: ESTATÍSTICAS NACIONAIS ---------------
with aba4:
    st.markdown("# Estatísticas nacionais")
    st.caption(f"Dados SAEB: 3º ano do ensino médio · UF da escola: **{UF_ESCOLA}**")

    st.markdown('<div style="margin-bottom:-5px;"class="section-title">SAEB — Evolução histórica (2013–2023)</div>',
                unsafe_allow_html=True)

    disc_saeb = st.selectbox("Disciplina SAEB", list(DISC_SAEB.keys()), key='disc_saeb')
    cod_saeb  = DISC_SAEB[disc_saeb]
    rede_ref  = 'total - federal, estadual, municipal e privada'

    br_hist = saeb_br[
        (saeb_br['disciplina'] == cod_saeb) & (saeb_br['rede'] == rede_ref)
    ][['ano','media']].rename(columns={'media': 'Brasil'})

    uf_hist = saeb_uf[
        (saeb_uf['disciplina'] == cod_saeb) & (saeb_uf['rede'] == rede_ref)
    ][['ano','media']].rename(columns={'media': UF_ESCOLA})

    hist = br_hist.merge(uf_hist, on='ano', how='outer').sort_values('ano')

    fig_saeb = go.Figure()
    for col, cor, dash in [('Brasil','#3B6FE0','solid'), (UF_ESCOLA,'#F97316','dot')]:
        if col in hist.columns:
            fig_saeb.add_trace(go.Scatter(
                x=hist['ano'], y=hist[col], name=col, mode='lines+markers',
                line=dict(width=2.5, color=cor, dash=dash), marker=dict(size=7),
            ))
    fig_saeb.update_layout(
        height=340, margin=dict(t=10,b=10),
        xaxis_title='Ano', yaxis_title='Proficiência média (escala SAEB)',
        legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig_saeb, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">SAEB — Distribuição de níveis (2023)</div>', unsafe_allow_html=True)

    nivel_cols = [f'nivel_{i}' for i in range(11)]

    def get_niveis(df_saeb, disc, uf=None):
        sub = df_saeb[
            (df_saeb['disciplina'] == disc) &
            (df_saeb['rede'] == rede_ref) &
            (df_saeb['ano'] == 2023)
        ]
        if uf:
            sub = sub[sub['sigla_uf'] == uf]
        if sub.empty:
            return [0] * 11
        row = sub.iloc[0]
        return [float(row.get(c, 0) or 0) for c in nivel_cols]

    niveis_br = get_niveis(saeb_br, cod_saeb)
    niveis_uf = get_niveis(saeb_uf, cod_saeb)

    disc_key_map = {'Matemática': 'matematica', 'Linguagens': 'linguagens'}
    dk = disc_key_map.get(disc_saeb)
    if dk:
        sub_escola = df_full[df_full['disciplina_key'] == dk]
        nivel_escola_counts = sub_escola['nivel_saeb_est'].value_counts(normalize=True) * 100
        niveis_esc = [float(nivel_escola_counts.get(i, 0)) for i in range(11)]
    else:
        niveis_esc = [0] * 11

    x = list(range(11))
    fig_niv = go.Figure()
    for vals, nome, cor in [
        (niveis_br,  'Brasil',   '#3B6FE0'),
        (niveis_uf,  UF_ESCOLA,  '#F97316'),
        (niveis_esc, 'Escola',   '#22C55E'),
    ]:
        fig_niv.add_trace(go.Bar(x=x, y=vals, name=nome, marker_color=cor, opacity=0.8))

    fig_niv.update_layout(
        barmode='group', height=340, margin=dict(t=10,b=10),
        xaxis_title='Nível de proficiência', yaxis_title='% de alunos',
        legend=dict(orientation='h', y=-0.2),
        xaxis=dict(tickvals=x, ticktext=[str(i) for i in x])
    )
    st.plotly_chart(fig_niv, width='stretch')

    st.markdown('<br />')

    st.markdown('<div class="section-title">ENEM — Escola vs Nacional</div>', unsafe_allow_html=True)
    st.caption("Notas ENEM normalizadas para escala 0–10 (÷ 100) para comparação direta.")

    disc_enem_opts = [d for d in enem.columns if d in df_full['disciplina'].unique()]
    disc_enem = st.selectbox("Disciplina ENEM", disc_enem_opts, key='disc_enem')

    disc_key_enem = {
        'Matemática':          'matematica',
        'Linguagens':          'linguagens',
        'Ciências da Natureza':'ciencias_natureza',
        'Ciências Humanas':    'ciencias_humanas',
    }
    dk_enem     = disc_key_enem.get(disc_enem)
    escola_vals = df_full[df_full['disciplina_key'] == dk_enem]['media_anual'] if dk_enem else pd.Series()
    enem_vals   = enem[disc_enem].dropna()

    fig_enem = go.Figure()
    fig_enem.add_trace(go.Histogram(
        x=escola_vals, name='Escola', marker_color='#3B6FE0', opacity=0.7,
        xbins=dict(size=0.5), histnorm='percent'
    ))
    fig_enem.add_trace(go.Histogram(
        x=enem_vals, name='ENEM 2024', marker_color='#F97316', opacity=0.7,
        xbins=dict(size=0.5), histnorm='percent'
    ))
    fig_enem.add_vline(x=escola_vals.mean(), line_dash='dash', line_color='#3B6FE0',
                        annotation_text=f'Escola: {escola_vals.mean():.2f}')
    fig_enem.add_vline(x=enem_vals.mean(), line_dash='dash', line_color='#F97316',
                        annotation_text=f'ENEM: {enem_vals.mean():.2f}')
    fig_enem.update_layout(
        barmode='overlay', height=380, margin=dict(t=10,b=10),
        xaxis_title='Nota (0–10)', yaxis_title='% de alunos',
        legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig_enem, width='stretch')

    st.markdown('<div class="section-title">Resumo comparativo</div>', unsafe_allow_html=True)
    comp_rows = []
    for disc_label, dk in disc_key_enem.items():
        if disc_label not in enem.columns:
            continue
        escola_m = df_full[df_full['disciplina_key'] == dk]['media_anual'].mean()
        enem_m   = enem[disc_label].mean()
        diff     = escola_m - enem_m
        comp_rows.append({
            'Disciplina': disc_label,
            'Média Escola': round(escola_m, 2),
            'Média ENEM (norm.)': round(enem_m, 2),
            'Diferença': round(diff, 2),
            'Posição': '⬆ Acima' if diff > 0 else ('⬇ Abaixo' if diff < 0 else '= Igual'),
        })

    df_comp_tab = pd.DataFrame(comp_rows)

    def format_diff(val):
        if val > 0: return f"🟢 {val}"
        elif val < 0: return f"🔴 {val}"
        return f"⚪ {val}"

    df_comp_tab['Diferença'] = df_comp_tab['Diferença'].apply(format_diff)
    st.dataframe(df_comp_tab, width='stretch', hide_index=True)


# ABA 5: ANÁLISE DE PROFESSORES ---------------
with aba5:
    st.markdown("# Análise de professores")
    st.markdown("""
        <div style="font-size:17px; color:#475569; margin-bottom:24px; margin-top:-12px;">
        Visão comparativa do desempenho de cada docente — média das turmas, taxa de aprovação e evolução bimestral.
        </div>
    """, unsafe_allow_html=True)

    # Filtro de disciplina para esta aba
    disc_prof_opts = ['Todas'] + sorted(df_full['disciplina'].unique().tolist())
    col_filt1, col_filt2 = st.columns([1, 3])
    with col_filt1:
        disc_prof_sel = st.selectbox("Filtrar por disciplina", disc_prof_opts, key='disc_prof')

    df_prof_base = df_full.copy()
    if disc_prof_sel != 'Todas':
        df_prof_base = df_prof_base[df_prof_base['disciplina'] == disc_prof_sel]

    # Tabela resumo por professor
    resumo_prof = df_prof_base.groupby('id_professor').agg(
        Disciplina      = ('disciplina', 'first'),
        Turmas          = ('turma', lambda x: ', '.join(sorted(x.unique()))),
        Alunos          = ('id_aluno', 'nunique'),
        Média_Geral     = ('media_anual', 'mean'),
        Taxa_Aprovação  = ('situacao', lambda x: (x == 'Aprovado').mean()),
        Média_B1        = ('media_b1', 'mean'),
        Média_B2        = ('media_b2', 'mean'),
        Média_B3        = ('media_b3', 'mean'),
        Média_B4        = ('media_b4', 'mean'),
    ).reset_index().rename(columns={'id_professor': 'Professor'})

    resumo_prof['Média_Geral']    = resumo_prof['Média_Geral'].round(2)
    resumo_prof['Taxa_Aprovação'] = resumo_prof['Taxa_Aprovação'].round(3)

    # ── Ranking visual ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Ranking de desempenho</div>', unsafe_allow_html=True)

    fig_rank = px.bar(
        resumo_prof.sort_values('Média_Geral', ascending=True),
        x='Média_Geral', y='Professor',
        color='Média_Geral',
        color_continuous_scale='RdYlGn',
        range_color=[0, 10],
        text='Média_Geral',
        orientation='h',
        hover_data={'Disciplina': True, 'Taxa_Aprovação': ':.1%', 'Alunos': True},
        labels={'Média_Geral': 'Média Geral', 'Professor': ''},
        height=420,
    )
    fig_rank.add_vline(x=LIMITE_APROV, line_dash='dash', line_color='red',
                        annotation_text='Mínimo aprovação')
    fig_rank.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_rank.update_layout(
        margin=dict(t=10, b=10), coloraxis_showscale=False,
        xaxis=dict(range=[0, 11])
    )
    st.plotly_chart(fig_rank, width='stretch')

    # ── Taxa de aprovação por professor ─────────────────────────────────────
    st.markdown('<div class="section-title">Taxa de aprovação por professor</div>', unsafe_allow_html=True)

    fig_aprov = px.bar(
        resumo_prof.sort_values('Taxa_Aprovação', ascending=True),
        x='Taxa_Aprovação', y='Professor',
        color='Taxa_Aprovação',
        color_continuous_scale='RdYlGn',
        range_color=[0, 1],
        text='Taxa_Aprovação',
        orientation='h',
        hover_data={'Disciplina': True, 'Alunos': True},
        labels={'Taxa_Aprovação': 'Taxa de Aprovação', 'Professor': ''},
        height=420,
    )
    fig_aprov.update_traces(texttemplate='%{text:.1%}', textposition='outside')
    fig_aprov.update_layout(
        margin=dict(t=10, b=10), coloraxis_showscale=False,
        xaxis=dict(range=[0, 1.15], tickformat='.0%')
    )
    st.plotly_chart(fig_aprov, width='stretch')

    # ── Heatmap professor × turma ───────────────────────────────────────────
    st.markdown('<div class="section-title">Média por professor e turma</div>', unsafe_allow_html=True)
    st.caption("Cada célula mostra a média anual dos alunos daquela turma com aquele professor.")

    heat_data = df_full.groupby(['id_professor','turma'])['media_anual'].mean().round(2).unstack()

    fig_heat_pt = px.imshow(
        heat_data,
        text_auto=True,
        color_continuous_scale='RdYlGn',
        zmin=0, zmax=10,
        labels=dict(x='Turma', y='Professor', color='Média'),
        height=460,
    )
    fig_heat_pt.update_layout(margin=dict(t=10, b=10), font=dict(size=13))
    fig_heat_pt.update_xaxes(tickfont=dict(size=13))
    fig_heat_pt.update_yaxes(tickfont=dict(size=13))
    st.plotly_chart(fig_heat_pt, width='stretch')

    # ── Evolução bimestral por professor ────────────────────────────────────
    st.markdown('<div class="section-title">Evolução bimestral por professor</div>', unsafe_allow_html=True)

    bim_cols_prof = ['Média_B1','Média_B2','Média_B3','Média_B4']
    ev_prof = resumo_prof.melt(
        id_vars='Professor', value_vars=bim_cols_prof,
        var_name='Bimestre', value_name='Média'
    )
    ev_prof['Bimestre'] = ev_prof['Bimestre'].map({
        'Média_B1': '1º Bim', 'Média_B2': '2º Bim',
        'Média_B3': '3º Bim', 'Média_B4': '4º Bim'
    })

    # Mapeia cor fixa a cada professor
    profs_sorted = sorted(resumo_prof['Professor'].unique())
    cor_map_prof = {p: CORES_PROF[i % len(CORES_PROF)] for i, p in enumerate(profs_sorted)}

    fig_ev_prof = go.Figure()
    for _, row_p in resumo_prof.iterrows():
        prof = row_p['Professor']
        sub  = ev_prof[ev_prof['Professor'] == prof]
        fig_ev_prof.add_trace(go.Scatter(
            x=sub['Bimestre'], y=sub['Média'],
            name=f"{prof} ({row_p['Disciplina'][:4]}…)" if len(row_p['Disciplina']) > 4 else f"{prof} ({row_p['Disciplina']})",
            mode='lines+markers',
            line=dict(width=2.5, color=cor_map_prof[prof]),
            marker=dict(size=8),
        ))
    fig_ev_prof.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                           annotation_text='Mínimo aprovação')
    fig_ev_prof.update_layout(
        height=420, margin=dict(t=10, b=10),
        yaxis=dict(range=[0, 11], title='Média'),
        legend=dict(orientation='h', y=-0.25, font=dict(size=12)),
    )
    st.plotly_chart(fig_ev_prof, width='stretch')

    # ── Tabela detalhada ────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Tabela detalhada</div>', unsafe_allow_html=True)

    tabela_exib = resumo_prof[[
        'Professor','Disciplina','Turmas','Alunos',
        'Média_Geral','Taxa_Aprovação','Média_B1','Média_B2','Média_B3','Média_B4'
    ]].rename(columns={
        'Média_Geral': 'Média Geral', 'Taxa_Aprovação': 'Tx. Aprovação',
        'Média_B1': '1º Bim', 'Média_B2': '2º Bim',
        'Média_B3': '3º Bim', 'Média_B4': '4º Bim',
    }).sort_values('Média Geral', ascending=False)

    def cor_media(val):
        if not isinstance(val, float): return ''
        if val >= 8:   return 'color: #166534; font-weight: 700'
        if val >= 7:   return 'color: #1d4ed8; font-weight: 600'
        if val >= 5:   return 'color: #92400e'
        return 'color: #991B1B; font-weight: 700'

    st.dataframe(
        tabela_exib.style
            .format({'Média Geral': '{:.2f}', 'Tx. Aprovação': '{:.1%}',
                     '1º Bim': '{:.2f}', '2º Bim': '{:.2f}',
                     '3º Bim': '{:.2f}', '4º Bim': '{:.2f}'})
            .map(cor_media, subset=['Média Geral','1º Bim','2º Bim','3º Bim','4º Bim']),
        width='stretch', hide_index=True
    )

    # ── Comparar dois professores ────────────────────────────────────────────
    st.markdown('<div class="section-title">Comparar dois professores</div>', unsafe_allow_html=True)

    profs_lista = sorted(df_full['id_professor'].unique().tolist())
    cp1, cp2 = st.columns(2)
    prof_a = cp1.selectbox("Professor A", profs_lista, key='prof_a')
    prof_b = cp2.selectbox("Professor B", profs_lista, index=min(1, len(profs_lista)-1), key='prof_b')

    def dados_bim_prof(prof_id):
        sub = df_full[df_full['id_professor'] == prof_id]
        return sub[['media_b1','media_b2','media_b3','media_b4']].mean().values

    df_cmp_prof = pd.DataFrame({
        prof_a: dados_bim_prof(prof_a),
        prof_b: dados_bim_prof(prof_b),
    }, index=BIMESTRES)

    # Informações complementares
    def info_prof(prof_id):
        sub = df_full[df_full['id_professor'] == prof_id]
        return {
            'disciplina': sub['disciplina'].iloc[0],
            'turmas': ', '.join(sorted(sub['turma'].unique())),
            'media': sub['media_anual'].mean(),
            'aprovacao': (sub['situacao'] == 'Aprovado').mean(),
        }

    ia, ib = info_prof(prof_a), info_prof(prof_b)

    m1, m2 = st.columns(2)
    for col, prof_id, info, cor in [(m1, prof_a, ia, '#3B6FE0'), (m2, prof_b, ib, '#F97316')]:
        col.markdown(f"""
        <div style="background:#F8FAFF; border:2px solid {cor}; border-radius:12px; padding:16px 20px;">
            <div style="font-size:20px; font-weight:700; color:{cor};">{prof_id}</div>
            <div style="font-size:13px; color:#64748B; margin-top:2px;">{info['disciplina']} · {info['turmas']}</div>
            <div style="margin-top:12px; display:flex; gap:24px;">
                <div>
                    <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Média Geral</div>
                    <div style="font-size:26px; font-weight:700; color:#0F172A;">{info['media']:.2f}</div>
                </div>
                <div>
                    <div style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Tx. Aprovação</div>
                    <div style="font-size:26px; font-weight:700; color:#0F172A;">{info['aprovacao']:.1%}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br />')
    fig_cmp_prof = go.Figure()
    for col, cor in [(prof_a, '#3B6FE0'), (prof_b, '#F97316')]:
        fig_cmp_prof.add_trace(go.Scatter(
            x=df_cmp_prof.index, y=df_cmp_prof[col],
            name=col, mode='lines+markers',
            line=dict(width=2.5, color=cor), marker=dict(size=9),
        ))
    fig_cmp_prof.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                             annotation_text='Mínimo aprovação')
    fig_cmp_prof.update_layout(
        height=340, margin=dict(t=10, b=10),
        yaxis=dict(range=[0, 11], title='Média'), xaxis_title=''
    )
    st.plotly_chart(fig_cmp_prof, width='stretch')

    # Distribuição de faixas dos alunos de cada professor comparado
    st.markdown('<div class="section-title">Distribuição de faixas de desempenho</div>', unsafe_allow_html=True)
    faixas_cmp = []
    for prof_id in [prof_a, prof_b]:
        sub = df_full[df_full['id_professor'] == prof_id]
        counts = sub['faixa_desempenho'].value_counts(normalize=True).reindex(FAIXAS_ORDEM).fillna(0) * 100
        for faixa, pct in counts.items():
            faixas_cmp.append({'Professor': prof_id, 'Faixa': faixa, '%': round(pct, 1)})

    df_faixas_cmp = pd.DataFrame(faixas_cmp)
    fig_faixas_cmp = px.bar(
        df_faixas_cmp, x='Professor', y='%', color='Faixa',
        color_discrete_map=CORES_FAIXAS,
        category_orders={'Faixa': FAIXAS_ORDEM},
        barmode='stack', text='%', height=360,
        labels={'%': '% de alunos'},
    )
    fig_faixas_cmp.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
    fig_faixas_cmp.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig_faixas_cmp, width='stretch')


# ABA 6: PERFIL DO ALUNO ----------------------
with aba6:
    st.markdown("# Perfil do aluno")
    st.markdown("""
        <div style="font-size:17px; color:#475569; margin-bottom:24px; margin-top:-12px;">
        Busque um aluno pelo nome ou matrícula para ver seu desempenho detalhado em todas as disciplinas.
        </div>
    """, unsafe_allow_html=True)

    # ── Barra de busca ──────────────────────────────────────────────────────
    nomes_unicos = sorted(df_full['nome'].unique().tolist())

    busca_col, _ = st.columns([2, 2])
    with busca_col:
        aluno_sel = st.selectbox(
            "🔍  Buscar aluno (nome ou matrícula)",
            options=[''] + nomes_unicos,
            key='busca_aluno',
            placeholder="Digite o nome do aluno...",
        )

    if not aluno_sel:
        st.info("Selecione um aluno acima para ver o perfil completo.")
        st.stop()

    # Dados do aluno selecionado (todas as disciplinas)
    df_aluno = df_full[df_full['nome'] == aluno_sel].copy()

    if df_aluno.empty:
        st.warning("Aluno não encontrado.")
        st.stop()

    # Dados demográficos (iguais em todas as linhas)
    info = df_aluno.iloc[0]
    matricula       = info['matricula']
    turma_aluno     = info['turma']
    serie_aluno     = info['serie']
    genero_aluno    = 'Masculino' if info['genero'] == 'M' else 'Feminino'
    nascimento      = pd.to_datetime(info['data_nascimento']).strftime('%d/%m/%Y') if pd.notna(info['data_nascimento']) else '—'

    # Média geral (média das médias anuais por disciplina)
    media_geral_aluno   = df_aluno['media_anual'].mean()
    freq_media_aluno    = df_aluno['frequencia_anual'].mean()
    ativ_media_aluno    = df_aluno['taxa_atividades_anual'].mean()
    n_aprovado          = (df_aluno['situacao'] == 'Aprovado').sum()
    n_total_disc        = len(df_aluno)
    situacao_geral      = 'Aprovado' if n_aprovado == n_total_disc else (
                          'Parcialmente aprovado' if n_aprovado > 0 else 'Reprovado')

    badge_class = 'badge-green' if situacao_geral == 'Aprovado' else (
                  'badge-yellow' if situacao_geral == 'Parcialmente aprovado' else 'badge-red')

    # ── Cabeçalho do aluno ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="aluno-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div>
                <div class="aluno-nome">{aluno_sel}</div>
                <div class="aluno-sub">Matrícula {matricula} · {serie_aluno} – Turma {turma_aluno} · {genero_aluno} · Nasc. {nascimento}</div>
                <span class="aluno-badge {badge_class}" style="margin-top:10px; display:inline-block;">
                    {situacao_geral} em {n_aprovado}/{n_total_disc} disciplinas
                </span>
            </div>
            <div style="display:flex; gap:32px; flex-wrap:wrap;">
                <div style="text-align:center;">
                    <div style="font-size:11px; opacity:.7; text-transform:uppercase; letter-spacing:.05em;">Média Geral</div>
                    <div style="font-size:38px; font-weight:700; font-family:'Space Grotesk',sans-serif;">{media_geral_aluno:.2f}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:11px; opacity:.7; text-transform:uppercase; letter-spacing:.05em;">Frequência</div>
                    <div style="font-size:38px; font-weight:700; font-family:'Space Grotesk',sans-serif;">{freq_media_aluno:.1%}</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:11px; opacity:.7; text-transform:uppercase; letter-spacing:.05em;">Atividades</div>
                    <div style="font-size:38px; font-weight:700; font-family:'Space Grotesk',sans-serif;">{ativ_media_aluno:.1%}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Situação por disciplina ──────────────────────────────────────────────
    st.markdown('<div class="section-title">Situação por disciplina</div>', unsafe_allow_html=True)

    disc_cols = st.columns(len(df_aluno))
    for i, (_, row_d) in enumerate(df_aluno.sort_values('disciplina').iterrows()):
        disc_nome  = row_d['disciplina']
        media_disc = row_d['media_anual']
        sit_disc   = row_d['situacao']
        faixa_disc = row_d['faixa_desempenho']
        prof_disc  = row_d['id_professor']

        if sit_disc == 'Aprovado':
            bg, fg, emoji = '#DCFCE7', '#166534', '✅'
        elif 'falta' in sit_disc.lower():
            bg, fg, emoji = '#FEF9C3', '#854D0E', '⚠️'
        else:
            bg, fg, emoji = '#FEE2E2', '#991B1B', '❌'

        disc_cols[i].markdown(f"""
        <div style="background:{bg}; border-radius:12px; padding:16px 14px; text-align:center;">
            <div style="font-size:13px; font-weight:700; color:{fg}; text-transform:uppercase; letter-spacing:.04em;">{disc_nome}</div>
            <div style="font-size:32px; font-weight:700; color:#0F172A; font-family:'Space Grotesk',sans-serif; margin:8px 0;">{media_disc:.2f}</div>
            <div style="font-size:12px; color:#475569;">{faixa_disc}</div>
            <div style="font-size:12px; color:#64748B; margin-top:4px;">Prof. {prof_disc}</div>
            <div style="font-size:18px; margin-top:6px;">{emoji} {sit_disc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br />')

    # ── Radar de desempenho ──────────────────────────────────────────────────
    st.markdown('<div class="section-title">Radar de desempenho por disciplina</div>', unsafe_allow_html=True)

    c_radar, c_evolucao = st.columns([1, 1.6])

    with c_radar:
        disciplinas_radar = df_aluno.sort_values('disciplina')['disciplina'].tolist()
        medias_radar      = df_aluno.sort_values('disciplina')['media_anual'].tolist()
        # Fecha o polígono
        disciplinas_radar_fechado = disciplinas_radar + [disciplinas_radar[0]]
        medias_radar_fechado      = medias_radar + [medias_radar[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=medias_radar_fechado,
            theta=disciplinas_radar_fechado,
            fill='toself',
            fillcolor='rgba(59, 111, 224, 0.2)',
            line=dict(color='#3B6FE0', width=2.5),
            marker=dict(size=8),
            name=aluno_sel,
        ))

        # Linha de referência de aprovação
        fig_radar.add_trace(go.Scatterpolar(
            r=[LIMITE_APROV] * (len(disciplinas_radar) + 1),
            theta=disciplinas_radar_fechado,
            mode='lines',
            line=dict(color='red', dash='dash', width=1.5),
            name='Mínimo aprovação',
        ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=11))),
            showlegend=True,
            height=380,
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation='h', y=-0.1),
        )
        st.plotly_chart(fig_radar, width='stretch')

    with c_evolucao:
        # Evolução bimestral por disciplina
        ev_aluno_rows = []
        for _, row_d in df_aluno.iterrows():
            for bim_label, col_m in zip(BIMESTRES, COLS_MEDIA):
                ev_aluno_rows.append({
                    'Disciplina': row_d['disciplina'],
                    'Bimestre':   bim_label,
                    'Média':      row_d[col_m],
                })
        df_ev_aluno = pd.DataFrame(ev_aluno_rows)

        fig_ev_aluno = px.line(
            df_ev_aluno, x='Bimestre', y='Média', color='Disciplina',
            markers=True,
            color_discrete_sequence=CORES_PROF,
            title='Evolução bimestral por disciplina',
        )
        fig_ev_aluno.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                                annotation_text='Mínimo')
        fig_ev_aluno.update_traces(line=dict(width=2.5), marker=dict(size=8))
        fig_ev_aluno.update_layout(
            height=380, margin=dict(t=40, b=10),
            yaxis=dict(range=[0, 11]),
            legend=dict(font=dict(size=12)),
        )
        st.plotly_chart(fig_ev_aluno, width='stretch')

    # ── Detalhamento de provas ───────────────────────────────────────────────
    st.markdown('<div class="section-title">Notas por prova e bimestre</div>', unsafe_allow_html=True)

    disc_detalhe_sel = st.selectbox(
        "Selecione a disciplina para ver as notas individuais:",
        sorted(df_aluno['disciplina'].unique()),
        key='disc_detalhe_aluno'
    )
    row_disc = df_aluno[df_aluno['disciplina'] == disc_detalhe_sel].iloc[0]

    provas_map = {
        'P1 — 1º Bim': 'nota_p1_b1', 'P2 — 1º Bim': 'nota_p2_b1',
        'P1 — 2º Bim': 'nota_p1_b2', 'P2 — 2º Bim': 'nota_p2_b2',
        'P1 — 3º Bim': 'nota_p1_b3', 'P2 — 3º Bim': 'nota_p2_b3',
        'P1 — 4º Bim': 'nota_p1_b4', 'P2 — 4º Bim': 'nota_p2_b4',
    }
    notas_aluno  = [row_disc[col] for col in provas_map.values()]
    rotulos      = list(provas_map.keys())
    cores_provas = ['#3B6FE0' if n >= LIMITE_APROV else '#EF4444' for n in notas_aluno]

    fig_provas_aluno = go.Figure(go.Bar(
        x=rotulos, y=notas_aluno,
        marker_color=cores_provas,
        text=[f'{n:.1f}' for n in notas_aluno],
        textposition='outside',
    ))
    fig_provas_aluno.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                                annotation_text='Mínimo aprovação')
    fig_provas_aluno.update_layout(
        height=320, margin=dict(t=10, b=10),
        yaxis=dict(range=[0, 11], title='Nota'),
    )
    st.plotly_chart(fig_provas_aluno, width='stretch')

    # Mini-cards de atividades e faltas por bimestre
    st.markdown('<div class="section-title">Atividades e frequência por bimestre</div>', unsafe_allow_html=True)

    cols_mini = st.columns(4)
    for i, (bim_label, b) in enumerate(zip(BIMESTRES, ['b1','b2','b3','b4'])):
        entregues = int(row_disc[f'ativs_entregues_{b}'])
        total_a   = int(row_disc[f'ativs_total_{b}'])
        faltas    = int(row_disc[f'faltas_{b}'])
        aulas     = int(row_disc['aulas_bimestre'])
        taxa_a    = entregues / total_a if total_a > 0 else 0
        freq_b    = 1 - (faltas / aulas) if aulas > 0 else 0
        media_b   = row_disc[f'media_{b}']
        cor_m     = '#166534' if media_b >= LIMITE_APROV else '#991B1B'

        cols_mini[i].markdown(f"""
        <div style="background:#F8FAFF; border:1px solid #E2E8F8; border-radius:12px; padding:16px 14px; text-align:center;">
            <div style="font-size:14px; font-weight:700; color:#1E3A6E; margin-bottom:10px;">{bim_label}</div>
            <div style="font-size:26px; font-weight:700; color:{cor_m}; font-family:'Space Grotesk',sans-serif;">{media_b:.2f}</div>
            <div style="font-size:11px; color:#64748B; margin-top:2px;">média do bimestre</div>
            <hr style="border:none; border-top:1px solid #E2E8F8; margin:10px 0;">
            <div style="font-size:12px; color:#475569;">📋 Atividades: <b>{entregues}/{total_a}</b> ({taxa_a:.0%})</div>
            <div style="font-size:12px; color:#475569; margin-top:4px;">📅 Faltas: <b>{faltas}</b> / {aulas} aulas ({freq_b:.0%} presença)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br />')

    # ── Comparação com a turma ───────────────────────────────────────────────
    st.markdown('<div class="section-title">Comparação com a turma e escola</div>', unsafe_allow_html=True)
    st.caption(f"Turma {turma_aluno} · {serie_aluno}")

    comp_rows_aluno = []
    for _, row_d in df_aluno.iterrows():
        disc = row_d['disciplina']
        dk   = row_d['disciplina_key']

        media_turma_disc  = df_full[(df_full['turma'] == turma_aluno) & (df_full['disciplina'] == disc)]['media_anual'].mean()
        media_escola_disc = df_full[df_full['disciplina'] == disc]['media_anual'].mean()
        media_aluno_disc  = row_d['media_anual']

        comp_rows_aluno.append({
            'Disciplina':        disc,
            'Aluno':             round(media_aluno_disc, 2),
            f'Turma {turma_aluno}': round(media_turma_disc, 2),
            'Escola':            round(media_escola_disc, 2),
        })

    df_comp_aluno = pd.DataFrame(comp_rows_aluno)

    fig_comp_aluno = go.Figure()
    cores_comp = {'Aluno': '#3B6FE0', f'Turma {turma_aluno}': '#F97316', 'Escola': '#94A3B8'}
    for col_name, cor in cores_comp.items():
        fig_comp_aluno.add_trace(go.Bar(
            x=df_comp_aluno['Disciplina'],
            y=df_comp_aluno[col_name],
            name=col_name,
            marker_color=cor,
            text=[f'{v:.2f}' for v in df_comp_aluno[col_name]],
            textposition='outside',
        ))

    fig_comp_aluno.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                              annotation_text='Mínimo aprovação')
    fig_comp_aluno.update_layout(
        barmode='group', height=360, margin=dict(t=10, b=10),
        yaxis=dict(range=[0, 12], title='Média'),
        legend=dict(orientation='h', y=-0.2),
    )
    st.plotly_chart(fig_comp_aluno, width='stretch')
