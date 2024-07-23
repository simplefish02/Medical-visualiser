import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# read the file
df = pd.read_csv('medical_examination.csv', index_col=0)

# create overweight column and set the value
df['overweight'] = df['weight'] / (df['height']/100)**2
df.loc[df['overweight'] <= 25, 'overweight'] = 0
df.loc[df['overweight'] > 25, 'overweight'] = 1

# set glucose and cholesterol values
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1


def draw_cat_plot():
    
    cardio_df = df[['cardio','active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']]
    
    df_cat = pd.melt(cardio_df, id_vars=['cardio'], var_name='variable', value_name='value')
    
    fig = sns.catplot(x='variable', hue='value', col='cardio', data=df_cat, kind='count')
    fig.set_axis_labels('variable', 'total')
    fig=fig.fig
    fig.savefig('catplot.png')
    return fig


def draw_heat_map():
    # 11
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))].reset_index()

    matrix = df_heat.corr()
    # Create a mask using numpy's triu function
    mask = np.triu(np.ones_like(matrix, dtype=bool))
    fig, ax = plt.subplots()

    sns.heatmap(matrix, square=True, annot=True, mask=mask, fmt='.1f')
    fig.savefig('heatmap.png')
    return fig