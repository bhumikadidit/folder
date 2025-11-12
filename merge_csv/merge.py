import pandas as pd

df1 = pd.read_csv('kpi_1.csv')
df2 = pd.read_csv('kpi_2.csv')

df1['District_clean'] = df1['District'].str.lower().str.replace(' ', '')
df2['District_clean'] = df2['District'].str.lower().str.replace(' ', '')

merged_df = pd.merge(df1, df2, on='District_clean', how='outer', suffixes=('_1', '_2'))

merged_df['District'] = merged_df['District_1'].fillna(merged_df['District_2'])
merged_df = merged_df.drop(columns=['District_1', 'District_2', 'District_clean'])

merged_df[['KPI_1', 'KPI_2']] = merged_df[['KPI_1', 'KPI_2']].fillna(0)

print(merged_df)
merged_df.to_csv('merged_kpis_final.csv', index=False)