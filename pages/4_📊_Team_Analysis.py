import streamlit as st
import pandas as pd
from os.path import dirname, realpath
from datetime import datetime
import plotly.express as px

st.set_page_config(
    layout='wide'
)


#----------------------** Reading dataset
if 'data' not in st.session_state:
    path = dirname(dirname(realpath(__file__)))
    df = pd.read_csv(path + '/assets/CLEAN_FIFA23_official_data.csv')

    #----------------------** Manipulation with Pandas
    df = df[df['Contract Valid Until'] >= datetime.today().year]
    df = df[df['Value(£)'] > 0]
    df['International Reputation'] = df['International Reputation'].apply(lambda x: int(x))
    df['Name'] = df['Name'].apply(lambda x: x.replace('22\xa0', ''))    #Fix buggy names
    df['value_formatted'] = df['Value(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['wage_formatted'] = df['Wage(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['clause_formatted'] = df['Release Clause(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    st.session_state['data'] = df
else:
    df = st.session_state['data']

st.sidebar.text('Desenvolvido por Lelis')

st.title('Análise Gráfica dos Times', False)

overall_per_nationality = df[df['International Reputation'] >= 3][['Nationality', 'Overall']].groupby(['Nationality']).mean().sort_values('Overall').reset_index().tail(15)
overall_per_nationality_graph = px.bar(data_frame=overall_per_nationality,
                                       x='Overall', y='Nationality',
                                       title='Overall Médio por Nacionalidade (Reputação Internacional > 3)',
                                       labels={'Nationality': 'Nacionalidade'}, text_auto=True,
                                       range_x=[overall_per_nationality.min()[1]-2, overall_per_nationality.max()[1]+2])
overall_per_nationality_graph.update_traces(dict(textangle=0, textposition='outside', textfont_size=12))

clause_per_club = df[['Club', 'Release Clause(£)']].groupby('Club').sum().sort_values('Release Clause(£)').reset_index().tail(15)
clause_per_club_graph = px.bar(data_frame=clause_per_club,
                               x='Release Clause(£)', y='Club',
                               title='Cláusula de Rescisão Média por Clube',
                               labels={'Club': 'Clube', 'Release Clause(£)': 'Cláusula de Rescisão'}, text_auto=True,
                               range_x=[clause_per_club.min()[1] / 1.25, clause_per_club.max()[1] * 1.15])
clause_per_club_graph.update_traces(dict(textangle=0, textposition='outside', textfont_size=12))

value_per_club = df[['Club', 'Value(£)']].groupby('Club').sum().sort_values('Value(£)').reset_index().tail(15)
value_per_club_graph = px.bar(data_frame=value_per_club,
                               x='Value(£)', y='Club',
                               title='Valor Total de Jogadores por Clube',
                               labels={'Club': 'Clube', 'Value(£)': 'Valor Total'}, text_auto=True,
                               range_x=[value_per_club.min()[1] / 1.25, value_per_club.max()[1] * 1.15])
value_per_club_graph.update_traces(dict(textangle=0, textposition='outside', textfont_size=12))

player_per_loaner = pd.DataFrame(df['Loaned From'].value_counts()).sort_values('count').reset_index().tail(15)
player_per_loaner_graph = px.bar(data_frame=player_per_loaner,
                                 x='count', y='Loaned From',
                                 title='Quantidade de Jogadores Emprestados por Times que Emprestam',
                                 labels={'count': 'Quantidade de Jogadores Emprestados', 'Loaned From': 'Times (Emprestador)'}, text_auto=True)
player_per_loaner_graph.update_traces(dict(textangle=0, textposition='outside', textfont_size=12))

graph_row1 = st.columns(2)

with graph_row1[0]: st.plotly_chart(overall_per_nationality_graph, True)
with graph_row1[1]: st.plotly_chart(clause_per_club_graph, True)

#df

graph_row2 = st.columns(2)

with graph_row2[0]: st.plotly_chart(value_per_club_graph, True)
with graph_row2[1]: st.plotly_chart(player_per_loaner_graph, True)