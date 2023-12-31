from . import ROOT_DIR
from ....PANDAS.basic import load

df = load(f'{ROOT_DIR}/import/df_fum_candidateimgs.csv')

r = df['[34]']#.apply(lambda x: x.replace('_clahe', ''))
print((r.drop_duplicates()))
# print(df)