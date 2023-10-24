import streamlit as st
import pandas as pd
from os.path import dirname, realpath
from datetime import datetime
import plotly.express as px

#----------------------** Reading dataset
if 'data' not in st.session_state or 'data_over' not in st.session_state:
    path = dirname(dirname(realpath(__file__)))
    df = pd.read_csv(path + '/assets/CLEAN_FIFA23_official_data.csv')
    df_overall_per_year = pd.read_csv(path + '/assets/FIFA_17_TO_23_OVERALL_LELIS.csv')

    #----------------------** Manipulation with Pandas
    df = df[df['Contract Valid Until'] >= datetime.today().year]
    df = df[df['Value(£)'] > 0]
    df['Name'] = df['Name'].apply(lambda x: x.replace('22\xa0', ''))    #Fix buggy names
    df['value_formatted'] = df['Value(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['wage_formatted'] = df['Wage(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['clause_formatted'] = df['Release Clause(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    st.session_state['data'] = df
    st.session_state['data_over'] = df_overall_per_year
else:
    df = st.session_state['data']
    df_overall_per_year = st.session_state['data_over']


#-------------------** Page Layout

st.set_page_config(
    layout='wide',
    page_title='Players'
)

clubs = st.sidebar.selectbox('Clube', df['Club'].value_counts().index, index=None, placeholder='Selecione um clube')
df_filtered = df[df['Club'] == clubs]
if clubs != None:
    player = st.sidebar.selectbox('Jogador', df_filtered['Name'].value_counts().index)
    df_filtered = df_filtered[df_filtered['Name'] == player]

    st.markdown(f'![Imagem do Jogador]({df_filtered["Photo"].values[0]})')

    player_name = df_filtered["Name"].values[0]
    player_nationality = df_filtered["Nationality"].values[0]
    player_flag = df_filtered["Flag"].values[0]
    st.markdown(f'# {player_name} ![{player_nationality}]({player_flag})')

    player_club = df_filtered["Club"].values[0]
    player_club_logo = df_filtered["Club Logo"].values[0]
    st.markdown(f'**Clube**: {player_club} ![{player_club}]({player_club_logo})')

    st.markdown(f'**Posição**: {df_filtered["Position"].values[0]}')

    info_row = st.columns(3)
    with info_row[0]: st.markdown(f'**Idade**: {df_filtered["Age"].values[0]}')
    with info_row[1]:
        height = df_filtered["Height(cm.)"].values[0] / 100
        st.markdown(f'**Altura**: {height} m')
    with info_row[2]:
        weight = df_filtered["Weight(lbs.)"].values[0] / 2.205
        st.markdown(f'**Peso**: {weight} kg')

    st.divider()

    st.subheader(f'Overall {df_filtered["Overall"].values[0]}')

    st.progress(int(df_filtered["Overall"].values[0]))

    value_row = st.columns(3)
    with value_row[0]:
        value = df_filtered['Value(£)'].values[0]
        value = '£ ' + '{:,.2f}'.format(df_filtered['Value(£)'].values[0]).replace(".","%").replace(",",".").replace("%",",")
        st.metric('Valor de mercado', value)
    with value_row[1]:
        value = df_filtered['Value(£)'].values[0]
        value = '£ ' + '{:,.2f}'.format(df_filtered['Wage(£)'].values[0]).replace(".","%").replace(",",".").replace("%",",")
        st.metric('Remuneração Semanal', value)
    with value_row[2]:
        value = df_filtered['Value(£)'].values[0]
        value = '£ ' + '{:,.2f}'.format(df_filtered['Release Clause(£)'].values[0]).replace(".","%").replace(",",".").replace("%",",")
        st.metric('Cláusula de Rescisão', value)

    df_overall_per_year_filtered = df_overall_per_year[df_overall_per_year['ID'] == df_filtered['ID'].values[0]].drop(columns=['Unnamed: 0'])
    if not df_overall_per_year_filtered.empty:
        line_chart = px.line(data_frame=df_overall_per_year_filtered,
                            x='Year', y='Overall', title='Overall a cada Ano', text='Overall',
                            labels={'Year': 'Ano'}, markers=True,
                            hover_data={
                                
                            })
        line_chart.update_traces(textposition='bottom center', textfont_size=13)
        st.plotly_chart(line_chart, True)


st.sidebar.divider()
st.sidebar.text('Desenvolvido por Lelis')