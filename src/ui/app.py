import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Edumetricas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
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
        font-size: 12px;
        font-weight: 600;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 6px;
    }
    .metric-card .value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #1E3A6E;
    }
    .metric-card .sub {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 4px;
    }
    .badge-aprovado    { background:#DCFCE7; color:#166534; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-recuperacao { background:#FEF9C3; color:#854D0E; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-reprovado   { background:#FEE2E2; color:#991B1B; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
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
    [data-testid="stSidebarNav"] a { color: #CBD5F0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
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
LIMITE_FREQ  = 0.75
UF_ESCOLA    = 'PB'

DISC_SAEB = {
    'Matemática': 'MT',
    'Linguagens': 'LP',
}

# ─────────────────────────────────────────────
# CARREGAMENTO DE DADOS
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# SIDEBAR — filtros globais
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Edumetricas")
    st.markdown("---")
    st.markdown("### Filtros")

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
    genero_sel   = st.multiselect("Gênero", ['F','M'], default=['F','M'])

# Aplicar filtros
df = df_full.copy()
if serie_sel  != 'Todas': df = df[df['serie']            == serie_sel]
if turma_sel  != 'Todas': df = df[df['turma']            == turma_sel]
if disc_sel   != 'Todas': df = df[df['disciplina']       == disc_sel]
if faixa_sel  != 'Todas': df = df[df['faixa_desempenho'] == faixa_sel]
if genero_sel:            df = df[df['genero'].isin(genero_sel)]

# ─────────────────────────────────────────────
# ABAS
# ─────────────────────────────────────────────
aba1, aba2, aba3, aba4 = st.tabs([
    "🏫 Visão Geral",
    "📚 Desempenho por Matéria",
    "📈 Evolução Bimestral",
    "🌐 Comparativo Nacional",
])

# ══════════════════════════════════════════════
# ABA 1 — VISÃO GERAL
# ══════════════════════════════════════════════
with aba1:
    st.markdown("# Visão Geral da Escola")
    filtro_desc = " · ".join(filter(lambda x: x != 'Todas', [serie_sel, turma_sel, disc_sel])) or "Escola completa"
    st.caption(f"Filtro ativo: **{filtro_desc}**  —  {df['id_aluno'].nunique()} alunos · {len(df)} registros")

    # ── KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    n_alunos   = df['id_aluno'].nunique()
    media_geral = df['media_anual'].mean()
    freq_media  = df['frequencia_anual'].mean() * 100
    em_risco    = df[
        (df['media_anual'] < LIMITE_APROV) | (df['frequencia_anual'] < LIMITE_FREQ)
    ]['id_aluno'].nunique()
    pct_aprov   = (df['situacao'] == 'Aprovado').mean() * 100

    for col, label, val, sub in zip(
        [col1, col2, col3, col4, col5],
        ['Alunos', 'Média Geral', 'Frequência Média', 'Em Risco', 'Taxa Aprovação'],
        [n_alunos, f"{media_geral:.2f}", f"{freq_media:.1f}%", em_risco, f"{pct_aprov:.1f}%"],
        ['registros únicos', 'escala 0–10', 'presença anual', 'nota ou frequência', 'no ano letivo']
    ):
        col.markdown(f"""
        <div class="metric-card">
          <div class="label">{label}</div>
          <div class="value">{val}</div>
          <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Faixas de Desempenho</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])

    with c1:
        faixas = df['faixa_desempenho'].value_counts().reindex(FAIXAS_ORDEM).fillna(0)
        fig_pizza = px.pie(
            values=faixas.values,
            names=faixas.index,
            color=faixas.index,
            color_discrete_map=CORES_FAIXAS,
            hole=0.45,
        )
        fig_pizza.update_traces(textposition='outside', textinfo='percent+label')
        fig_pizza.update_layout(showlegend=False, margin=dict(t=20,b=20,l=20,r=20), height=300)
        st.plotly_chart(fig_pizza, use_container_width=True)

    with c2:
        faixas_disc = (
            df.groupby(['disciplina','faixa_desempenho'])
            .size().reset_index(name='n')
        )
        faixas_disc_pct = faixas_disc.copy()
        total_disc = faixas_disc.groupby('disciplina')['n'].transform('sum')
        faixas_disc_pct['pct'] = (faixas_disc_pct['n'] / total_disc * 100).round(1)
        faixas_disc_pct['faixa_desempenho'] = pd.Categorical(
            faixas_disc_pct['faixa_desempenho'], FAIXAS_ORDEM
        )
        faixas_disc_pct = faixas_disc_pct.sort_values('faixa_desempenho')

        fig_bar = px.bar(
            faixas_disc_pct, x='disciplina', y='pct',
            color='faixa_desempenho',
            color_discrete_map=CORES_FAIXAS,
            category_orders={'faixa_desempenho': FAIXAS_ORDEM},
            labels={'pct': '%', 'disciplina': '', 'faixa_desempenho': 'Faixa'},
            barmode='stack', height=300,
        )
        fig_bar.update_layout(margin=dict(t=20,b=20), legend=dict(orientation='h', y=-0.25))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="section-title">Médias por Série e Disciplina</div>', unsafe_allow_html=True)
    media_heatmap = (
        df.groupby(['serie','disciplina'])['media_anual']
        .mean().round(2).unstack()
    )
    fig_heat = px.imshow(
        media_heatmap,
        text_auto=True,
        color_continuous_scale='RdYlGn',
        zmin=0, zmax=10,
        labels=dict(x='Disciplina', y='Série', color='Média'),
        height=220,
    )
    fig_heat.update_layout(margin=dict(t=10,b=10))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="section-title">Situação dos Alunos</div>', unsafe_allow_html=True)
    sit = df.groupby(['disciplina','situacao']).size().reset_index(name='n')
    fig_sit = px.bar(
        sit, x='n', y='disciplina', color='situacao',
        color_discrete_map={
            'Aprovado': '#22C55E',
            'Recuperação': '#F59E0B',
            'Reprovado (nota)': '#EF4444',
            'Reprovado (frequência)': '#F97316',
            'Reprovado (nota e frequência)': '#991B1B',
        },
        orientation='h', height=300,
        labels={'n': 'Alunos', 'disciplina': '', 'situacao': 'Situação'},
    )
    fig_sit.update_layout(margin=dict(t=10,b=10), legend=dict(orientation='h', y=-0.3))
    st.plotly_chart(fig_sit, use_container_width=True)

    st.markdown('<div class="section-title">Alunos em Risco</div>', unsafe_allow_html=True)
    df_risco = df[
        (df['media_anual'] < LIMITE_APROV) | (df['frequencia_anual'] < LIMITE_FREQ)
    ][['nome','serie','turma','disciplina','media_anual','frequencia_anual','situacao']]\
     .sort_values('media_anual').drop_duplicates()

    st.dataframe(
        df_risco.rename(columns={
            'nome': 'Aluno', 'serie': 'Série', 'turma': 'Turma',
            'disciplina': 'Disciplina', 'media_anual': 'Média',
            'frequencia_anual': 'Frequência', 'situacao': 'Situação'
        }).style.format({'Média': '{:.2f}', 'Frequência': '{:.1%}'}),
        use_container_width=True, height=280
    )


# ══════════════════════════════════════════════
# ABA 2 — DESEMPENHO POR MATÉRIA
# ══════════════════════════════════════════════
with aba2:
    st.markdown("# Desempenho por Matéria")

    disc_aba2 = st.selectbox(
        "Selecione a disciplina",
        sorted(df_full['disciplina'].unique()),
        key='disc_aba2'
    )
    df2 = df[df['disciplina'] == disc_aba2] if disc_sel == 'Todas' else df[df['disciplina'] == disc_aba2]
    if disc_sel != 'Todas':
        df2 = df[df['disciplina'] == disc_aba2]
    else:
        df2 = df[df['disciplina'] == disc_aba2]

    c1, c2, c3 = st.columns(3)
    c1.metric("Média da Disciplina", f"{df2['media_anual'].mean():.2f}")
    c2.metric("Frequência Média",    f"{df2['frequencia_anual'].mean()*100:.1f}%")
    c3.metric("Taxa de Atividades",  f"{df2['taxa_atividades_anual'].mean()*100:.1f}%")

    st.markdown('<div class="section-title">Distribuição das Notas</div>', unsafe_allow_html=True)
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
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        fig_box = px.box(
            df2, x='serie', y='media_anual',
            color='serie',
            labels={'media_anual': 'Média Anual', 'serie': 'Série'},
            title='Boxplot por série'
        )
        fig_box.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red')
        fig_box.update_layout(height=320, margin=dict(t=40,b=10), showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="section-title">Notas por Prova e Bimestre</div>', unsafe_allow_html=True)
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
    fig_provas.update_layout(height=320, margin=dict(t=10,b=10),
                              yaxis=dict(range=[0,11]))
    st.plotly_chart(fig_provas, use_container_width=True)

    st.markdown('<div class="section-title">Desempenho por Turma</div>', unsafe_allow_html=True)
    media_turma = (
        df2.groupby('turma')['media_anual'].mean().round(2).reset_index()
    )
    fig_turma = px.bar(
        media_turma.sort_values('turma'), x='turma', y='media_anual',
        color='media_anual',
        color_continuous_scale='RdYlGn',
        range_color=[0, 10],
        text='media_anual',
        labels={'turma': 'Turma', 'media_anual': 'Média'},
    )
    fig_turma.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red')
    fig_turma.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_turma.update_layout(height=320, margin=dict(t=10,b=10),
                             coloraxis_showscale=False, yaxis=dict(range=[0,11]))
    st.plotly_chart(fig_turma, use_container_width=True)

    st.markdown('<div class="section-title">Relação Frequência × Nota</div>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        df2, x='frequencia_anual', y='media_anual',
        color='faixa_desempenho',
        color_discrete_map=CORES_FAIXAS,
        hover_data=['nome','turma','serie'],
        labels={
            'frequencia_anual': 'Frequência Anual',
            'media_anual': 'Média Anual',
            'faixa_desempenho': 'Faixa',
        },
        opacity=0.65,
    )
    fig_scatter.add_hline(y=LIMITE_APROV,  line_dash='dash', line_color='red',   annotation_text='Mínimo nota')
    fig_scatter.add_vline(x=LIMITE_FREQ,   line_dash='dash', line_color='orange', annotation_text='Mínimo frequência')
    fig_scatter.update_layout(height=380, margin=dict(t=10,b=10))
    st.plotly_chart(fig_scatter, use_container_width=True)


# ══════════════════════════════════════════════
# ABA 3 — EVOLUÇÃO BIMESTRAL
# ══════════════════════════════════════════════
with aba3:
    st.markdown("# Evolução Bimestral")

    c1, c2 = st.columns(2)
    with c1:
        agrup = st.radio(
            "Agrupar por",
            ['Escola toda', 'Série', 'Turma', 'Disciplina'],
            horizontal=True, key='agrup_bim'
        )
    with c2:
        metrica = st.radio(
            "Métrica",
            ['Média das notas', 'Frequência'],
            horizontal=True, key='metrica_bim'
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

    fig_ev = px.line(
        ev, x='Bimestre', y=ylabel, color='Grupo',
        markers=True,
        labels={ylabel: ylabel, 'Bimestre': ''},
    )
    if metrica == 'Média das notas':
        fig_ev.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red',
                         annotation_text='Mínimo aprovação')
    else:
        fig_ev.add_hline(y=LIMITE_FREQ*100, line_dash='dash', line_color='orange',
                         annotation_text='75% mínimo')
    fig_ev.update_traces(line=dict(width=2.5), marker=dict(size=8))
    fig_ev.update_layout(height=420, margin=dict(t=20,b=10))
    st.plotly_chart(fig_ev, use_container_width=True)

    # Tabela de variação entre bimestres
    st.markdown('<div class="section-title">Variação entre Bimestres</div>', unsafe_allow_html=True)

    if agrup == 'Escola toda':
        pivot = ev.set_index('Bimestre')[ylabel].to_frame().T
        pivot.index = ['Escola']
    else:
        pivot = ev.pivot(index='Grupo', columns='Bimestre', values=ylabel)[BIMESTRES]

    pivot['Δ 1→2'] = (pivot['2º Bim'] - pivot['1º Bim']).round(2)
    pivot['Δ 2→3'] = (pivot['3º Bim'] - pivot['2º Bim']).round(2)
    pivot['Δ 3→4'] = (pivot['4º Bim'] - pivot['3º Bim']).round(2)

    def color_delta(val):
        if isinstance(val, float):
            color = '#22C55E' if val > 0 else ('#EF4444' if val < 0 else '#64748B')
            return f'color: {color}; font-weight: 600'
        return ''

    st.dataframe(
        pivot.round(2).style.map(color_delta, subset=['Δ 1→2','Δ 2→3','Δ 3→4']),
        use_container_width=True
    )

    # Comparação entre duas turmas
    st.markdown('<div class="section-title">Comparar duas turmas</div>', unsafe_allow_html=True)
    turmas_disp_all = sorted(df_full['turma'].unique().tolist())
    ca, cb = st.columns(2)
    turma_a = ca.selectbox("Turma A", turmas_disp_all, key='ta')
    turma_b = cb.selectbox("Turma B", turmas_disp_all, index=1, key='tb')

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
            line=dict(width=2.5, color=cor),
            marker=dict(size=8),
        ))
    if metrica == 'Média das notas':
        fig_comp.add_hline(y=LIMITE_APROV, line_dash='dash', line_color='red')
    fig_comp.update_layout(height=340, margin=dict(t=10,b=10),
                            yaxis_title=ylabel)
    st.plotly_chart(fig_comp, use_container_width=True)


# ══════════════════════════════════════════════
# ABA 4 — COMPARATIVO NACIONAL
# ══════════════════════════════════════════════
with aba4:
    st.markdown("# Comparativo Nacional — SAEB & ENEM")
    st.caption(f"Dados SAEB: 3º ano do Ensino Médio · UF da escola: **{UF_ESCOLA}**")

    # ── SAEB
    st.markdown('<div class="section-title">SAEB — Evolução histórica (2013–2023)</div>',
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
                x=hist['ano'], y=hist[col],
                name=col, mode='lines+markers',
                line=dict(width=2.5, color=cor, dash=dash),
                marker=dict(size=7),
            ))
    fig_saeb.update_layout(
        height=340, margin=dict(t=10,b=10),
        xaxis_title='Ano',
        yaxis_title='Proficiência média (escala SAEB)',
        legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig_saeb, use_container_width=True)

    # Distribuição de níveis SAEB
    st.markdown('<div class="section-title">SAEB — Distribuição de níveis (2023)</div>',
                unsafe_allow_html=True)

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

    niveis_br  = get_niveis(saeb_br, cod_saeb)
    niveis_uf  = get_niveis(saeb_uf, cod_saeb)

    # Níveis estimados da escola (proxy via nota)
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
        xaxis_title='Nível de proficiência',
        yaxis_title='% de alunos',
        legend=dict(orientation='h', y=-0.2),
        xaxis=dict(tickvals=x, ticktext=[str(i) for i in x])
    )
    st.plotly_chart(fig_niv, use_container_width=True)

    # ── ENEM
    st.markdown('<div class="section-title">ENEM 2024 — Escola vs Nacional</div>',
                unsafe_allow_html=True)
    st.caption("Notas ENEM normalizadas para escala 0–10 (÷ 100) para comparação direta.")

    disc_enem_opts = [d for d in enem.columns if d in df_full['disciplina'].unique()]
    disc_enem = st.selectbox("Disciplina ENEM", disc_enem_opts, key='disc_enem')

    disc_key_enem = {
        'Matemática': 'matematica',
        'Linguagens': 'linguagens',
        'Ciências da Natureza': 'ciencias_natureza',
        'Ciências Humanas': 'ciencias_humanas',
    }
    dk_enem = disc_key_enem.get(disc_enem)
    escola_vals = df_full[df_full['disciplina_key'] == dk_enem]['media_anual'] if dk_enem else pd.Series()
    enem_vals   = enem[disc_enem].dropna()

    fig_enem = go.Figure()
    fig_enem.add_trace(go.Histogram(
        x=escola_vals, name='Escola',
        marker_color='#3B6FE0', opacity=0.7,
        xbins=dict(size=0.5), histnorm='percent'
    ))
    fig_enem.add_trace(go.Histogram(
        x=enem_vals, name='ENEM 2024',
        marker_color='#F97316', opacity=0.7,
        xbins=dict(size=0.5), histnorm='percent'
    ))
    fig_enem.add_vline(x=escola_vals.mean(), line_dash='dash', line_color='#3B6FE0',
                       annotation_text=f'Escola: {escola_vals.mean():.2f}')
    fig_enem.add_vline(x=enem_vals.mean(), line_dash='dash', line_color='#F97316',
                       annotation_text=f'ENEM: {enem_vals.mean():.2f}')
    fig_enem.update_layout(
        barmode='overlay', height=380, margin=dict(t=10,b=10),
        xaxis_title='Nota (0–10)',
        yaxis_title='% de alunos',
        legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig_enem, use_container_width=True)

    # Resumo comparativo
    st.markdown('<div class="section-title">Resumo Comparativo</div>', unsafe_allow_html=True)
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

    def color_diff(val):
        if isinstance(val, float):
            return f"color: {'#22C55E' if val > 0 else '#EF4444'}; font-weight:600"
        return ''

    def format_diff(val):
        if val > 0:
            return f"🟢 {val}"
        elif val < 0:
            return f"🔴 {val}"
        return f"⚪ {val}"

    df_comp_tab['Diferença'] = df_comp_tab['Diferença'].apply(format_diff)

    st.dataframe(
        df_comp_tab,
        use_container_width=True,
        hide_index=True
    )
