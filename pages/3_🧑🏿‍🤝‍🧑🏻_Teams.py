import streamlit as st
import pandas as pd
from os.path import dirname, realpath
from datetime import datetime

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
    df['Name'] = df['Name'].apply(lambda x: x.replace('22\xa0', ''))    #Fix buggy names
    df['value_formatted'] = df['Value(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['wage_formatted'] = df['Wage(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    df['clause_formatted'] = df['Release Clause(£)'].apply(lambda x: '£'+'{:,.2f}'.format(x).replace(".","%").replace(",",".").replace("%",","))
    st.session_state['data'] = df
else:
    df = st.session_state['data']


#-------------------** Page Layout

club = st.sidebar.selectbox('Clube', df['Club'].value_counts().index)
df_filtered = df[df['Club'] == club]

club_logo = df_filtered["Club Logo"].values[0]
st.markdown(f'# {club} ![Club Logo]({club_logo})')

titular = df_filtered[~df_filtered['Position'].isin(['SUB', 'RES'])]
st.subheader(f'Overall {round(titular["Overall"].mean())} (Time Titular)')

st.progress(round(titular["Overall"].mean()))

st.divider()

metric_row = st.columns([0.55, 0.72, 0.44, 0.4])

with metric_row[0]:
    wage_sum = '£ ' + '{:,.2f}'.format(df_filtered['Wage(£)'].sum()).replace(".","%").replace(",",".").replace("%",",")
    st.metric('Salário Total (Semanal)', wage_sum)

with metric_row[1]:
    value_sum = '£ ' + '{:,.2f}'.format(df_filtered['Value(£)'].sum()).replace(".","%").replace(",",".").replace("%",",")
    st.metric('Valor Total de Jogadores', value_sum)

with metric_row[2]:
    st.metric('Idade Média', round(df_filtered['Age'].mean()))

with metric_row[3]:
    st.metric('Jogadores Emprestados', df_filtered[~df['Loaned From'].isnull()].count()[0])

metric_row2 = st.columns([0.425, 0.55, 0.65])

with metric_row2[0]:
    best_player = df_filtered[df_filtered['Overall'] == df_filtered['Overall'].max()]
    st.metric('Melhor Jogador (Overall)', f'{best_player["Name"].values[0]}: {best_player["Overall"].values[0]}')

with metric_row2[1]:
    df_filtered['evolution_potential'] = df_filtered['Potential'] - df_filtered['Overall']
    most_potential = df_filtered[df_filtered['evolution_potential'] == df_filtered['evolution_potential'].max()]
    st.metric('Maior Potencial de Evolução (Overall 🠒 Potencial)', f'{most_potential["Name"].values[0]}: {most_potential["Overall"].values[0]} 🠒 {most_potential["Potential"].values[0]}')

with metric_row2[2]:
    mvp = df_filtered[df_filtered['Value(£)'] == df_filtered['Value(£)'].max()]
    mvp_value = '{:,.2f}'.format(mvp["Value(£)"].values[0]).replace(".","%").replace(",",".").replace("%",",")
    st.metric('Jogador mais caro', f'{mvp["Name"].values[0]}: £{mvp_value}')



metric_row3 = st.columns([0.55, 0.72, 0.85])

with metric_row3[0]:
    defense = df_filtered[df_filtered['Position'].isin(['GK', 'RB', 'LB', 'RWB', 'LWB', 'CB', 'SW'])]
    st.metric('Overall Médio de Defesores (Time Titular)', round(defense['Overall'].mean()))

with metric_row3[1]:
    mid = df_filtered[df_filtered['Position'].isin(['CDM', 'CM', 'CAM', 'RM', 'LM', 'RCM', 'LCM', 'RWM', 'LWM', 'ROM', 'LOM', 'OM'])]
    st.metric('Overall Médio de Meio-Campistas (Time Titular)', round(mid['Overall'].mean()))

with metric_row3[2]:
    attack = df_filtered[df_filtered['Position'].isin(['RW', 'LW', 'RF', 'LF', 'CF', 'ST', 'RS', 'LS'])]
    st.metric('Overall Médio de Atacantes (Time Titular)', round(attack['Overall'].mean()))



df_table = df_filtered[['Name', 'Age', 'Photo', 'Flag', 'Overall', 'value_formatted', 'wage_formatted', 'clause_formatted', 'Joined', 'Contract Valid Until',
                        'Height(cm.)', 'Weight(lbs.)', 'Loaned From']]


loaned_from_list = df_table[~df_table['Loaned From'].isnull()]['Loaned From'].values

loaned_clubs_logo = []
for club in loaned_from_list:
    loaned_clubs_logo.append(df[df['Club'] == club]['Club Logo'].values[0])

df_table['Loaned From (Logo)'] = ['Não Emprestado' for i in range(len(df_table))]

i = 0
for club in df_table['Loaned From']:
    if club in loaned_from_list:
        indice = df_table[df_table['Loaned From'] == club].index[0]
        df_table['Loaned From (Logo)'][indice] = loaned_clubs_logo[i]
        i += 1

df_table['Loaned From'] = df_table['Loaned From'].apply(lambda x: 'Não Emprestado' if type(x) == float else x)

st.dataframe(
    data=df_table.set_index('Name'),
    column_config={
        'Flag': st.column_config.ImageColumn('Country'),
        'Photo': st.column_config.ImageColumn(),
        'Overall': st.column_config.ProgressColumn(format='%i'),
        'value_formatted': st.column_config.TextColumn('Value(£)'),
        'wage_formatted': st.column_config.TextColumn('Wage(£)'),
        'clause_formatted': st.column_config.TextColumn('Release Clause(£)'),
        'Contract Valid Until': st.column_config.NumberColumn(format='%d'),
        'Loaned From (Logo)': st.column_config.ImageColumn('Loaner Logo', width='small')
    })

st.sidebar.divider()
st.sidebar.text('Desenvolvido por Lelis')