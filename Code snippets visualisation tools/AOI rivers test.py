import pandas as pd
import plotly

def get_figure(df, cat_cols=[],value_cols='', title=''):
    colorPalette = ['#FF0000','#FFFFFF','#0000CD'] #defining possible colors (red, white, blue)
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp = list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp

    colorList = [] #linking color to cat_col
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum

    #create pairs from DataFrame (one pair consists of two subsequent values of a row (so for example AOIA.1 in interval 1 and AOIA.2 in interval 2))
    #source is the previous interval and target the 'current' interval you are comparing
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i], cat_cols[i+1], value_cols]]
            sourceTargetDf.columns = ['source', 'target','frequency']
        else:
            tempDf = df[[cat_cols[i], cat_cols[i+1], value_cols]]
            tempDf.columns = ['source', 'target','frequency']
            sourceTargetDf = pd.concat([sourceTargetDf, tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source', 'target']).agg({'frequency':'sum'}).reset_index()

    #add index to the pairs
    sourceTargetDf['sourceIndex'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetIndex'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

    #create figure
    data = dict(type='sankey',
                node= dict(pad = 15, thickness = 20,line = dict(color='black', width=0.5),
                label = labelList,
                color = colorList),
                link = dict(source = sourceTargetDf['sourceIndex'],
                            target = sourceTargetDf['targetIndex'],
                            value = sourceTargetDf['frequency']))

    layout = dict(title = title, font = dict(size=10))
    fig = dict(data=[data], layout=layout)
    return fig

df = pd.DataFrame({'t1': ['AOIA.1','AOIA.1','AOIA.1','AOIA.1','AOIB.1','AOIB.1','AOIC.1'],
                   't2': ['AOIA.2','AOIA.2','AOIB.2','AOIB.2','AOIB.2','AOIC.2','AOIC.2'],
                   't3': ['AOIA.3','AOIA.3','AOIA.3','AOIA.3','AOIB.3','AOIC.3','AOIC.3'],
                   'frequency': [1,1,2,2,1,2,1]})

fig = get_figure(df, cat_cols=['t1','t2','t3'], value_cols='frequency',
                 title='Test AOI Diagram')

plotly.offline.plot(fig, validate=False)
    
