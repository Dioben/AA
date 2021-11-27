import plotly.express as px
import pandas as pd

df = pd.read_csv("results.csv",header=0)

#calculate time ratio
ratios = df.groupby(["nodes","edges"]).agg({"time":{"max","min"}})
ratios = ratios.reset_index()
ratios.columns = ['nodes','edges',"max","min"]

ratios['time ratio']= ratios.apply(lambda row: row['max']/row['min'],axis=1)

#calculate solution cost ratio
costratios = df.groupby(["nodes","edges"]).agg({"solution cost":{"max","min"}})
costratios = costratios.reset_index()
costratios.columns = ['nodes','edges',"max","min"]

costratios['cost ratio']= costratios.apply(lambda row: row['max']/row['min'],axis=1)

solution3dscatter = px.scatter_3d(df, x='nodes', y='edges', z='solutions seen',
              color='solution method', title="Solutions Seen/ Nodes and Edges")
solution3dscatter.show()

adds3dscatter = px.scatter_3d(df, x='nodes', y='edges', z='adds',
              color='solution method', title="Adds Seen/ Nodes and Edges")
adds3dscatter.show()

time3dscatter  = px.scatter_3d(df, x='nodes', y='edges', z='time',
              color='solution method', title="Time / Nodes and Edges")
time3dscatter.show()

timeratioscatter = px.scatter_3d(ratios, x='nodes', y='edges', z='time ratio',title="Solutions Time Ratio/ Nodes and Edges")
timeratioscatter.show()

costratioscatter = px.scatter_3d(costratios, x='nodes', y='edges', z='cost ratio',title="Solutions Cost Ratio/ Nodes and Edges")
costratioscatter.show()

costboxplot = px.box(costratios,y="cost ratio")
costboxplot.show()
