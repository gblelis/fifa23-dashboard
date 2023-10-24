import streamlit as st
from os.path import dirname, realpath
import pandas as pd
from datetime import datetime

st.set_page_config(
    layout='centered',
    page_title='Home'
)

#----------------------** Reading dataset
if 'data' not in st.session_state:
    path = dirname(realpath(__file__))
    df = pd.read_csv(path + '/assets/CLEAN_FIFA23_official_data.csv')

    #----------------------** Manipulation with Pandas
    df = df[df['Contract Valid Until'] >= datetime.today().year]
    df = df[df['Value(£)'] > 0]
    df['Name'] = df['Name'].apply(lambda x: x.replace('22\xa0', ''))    #Fix buggy names
    df['value_formatted'] = df['Value(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['wage_formatted'] = df['Wage(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['clause_formatted'] = df['Release Clause(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    st.session_state['data'] = df

st.sidebar.text('Desenvolvido por Lelis')

st.title('FIFA 23 - DATASET OFICIAL! ⚽', False)

st.link_button('Acesse os dados no Kaggle', 'https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data/')

st.write('O conjunto de dados de jogadores do futebol de 2017 a 2023 fornece informações abrangentes sobre jogadores de futebol profissionais.' +
        ' O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos do jogador, características físicas, estatísticas de jogo, detalhes do contrato' +
        ' e afiliações de clubes.')

st.markdown('Com **mais de 17000 registros**, este conjunto de dados oferece um recurso valioso para analistas de futebol, ' +
            'pesquisadores e entusiastas interessados em explorar vários aspectos do mundo do futebol, pois permite estudar atributos' +
            ' de jogadores, métricas de desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e desenvolvimento do jogador ao longo do tempo.')