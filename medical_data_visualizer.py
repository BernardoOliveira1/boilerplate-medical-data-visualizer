import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2 dividing their weight in kilograms by the square of their height in meters
df['overweight'] = (
    df['weight']/(df['height']*df['height']/10000) > 25).astype(int)

# 3 Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1
df['cholesterol'] = np.where(df['cholesterol'] <= 1, 0, 1)
df['gluc'] = np.where(df['gluc'] <= 1, 0, 1)


# 4
def draw_cat_plot():
    # Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
    # 5
    df_cat = pd.melt(df, id_vars="cardio", value_vars=[
                     "active", "alco", "cholesterol", "gluc", "overweight", "smoke"])

    # 6 Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(
        ['cardio', 'variable', 'value']).size().reset_index()
    df_cat = df_cat.rename(columns={0: 'total'})

    # 7 Convert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import : sns.catplot()

    chart = sns.catplot(data=df_cat, x="variable",
                        y="total", hue="value", kind="bar", col="cardio")
    # 8
    fig = chart.figure

    # 9
    fig.savefig('catplot.png')
    return fig


# 10 Draw the Heat Map in the draw_heat_map function
def draw_heat_map():

    # 11 Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
    # height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
    # height is more than the 97.5th percentile
    # weight is less than the 2.5th percentile
    # weight is more than the 97.5th percentile
    df_heat = df[((df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) &
                  (df['height'] <= df['height'].quantile(0.975)) &
                  (df['weight'] >= df['weight'].quantile(0.025)) &
                  (df['weight'] <= df['weight'].quantile(0.975)))].copy()
    # 12 Calculate the correlation matrix and store it in the corr variable
    corr = df_heat.corr()

    # 13 Generate a mask for the upper triangle and store it in the mask variable
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14 Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(16, 9))

    # 15 Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap()

    sns.heatmap(corr, cmap='coolwarm', square=True,   mask=mask,
                linewidths=0.5, annot=True, fmt="0.1f")

    # 16 Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
