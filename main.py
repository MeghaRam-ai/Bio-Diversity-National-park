from dash import Dash
import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
app = Dash(__name__)
server = app.server   #heroku


about_dataset="This dataset is published by the National Park Service about the animal and plant species identified in individual national parks" \
              "and verified by evidence, observations, vouchers, or reports that document the presence of a species in a park. "

species = pd.read_csv('species.csv',dtype='str')
species = species[~species['Order'].isnull()]
species = species[~species['Family'].isnull()]
species = species[~species['Occurrence'].isnull()]
species = species[~species['Nativeness'].isnull()]
species_df = species[~species['Abundance'].isnull()]
parks_df = pd.read_csv('parks.csv', dtype={'Park Name': 'str', 'State': 'str', 'Acres': 'int'})

parks_df["Region"]=np.nan
parks_df["State_FullName"] = np.nan

parks_df["Region"]= np.where((parks_df["State"]=="SD")| (parks_df["State"]=="OH") | (parks_df["State"]=="MI") | (parks_df["State"]=="ND") | (parks_df["State"]=="MN"), "MidWest", parks_df["Region"])
parks_df["Region"]= np.where((parks_df["Region"]=="nan") & ((parks_df["State"]=="ME")), "Northeast", parks_df["Region"])
parks_df["Region"]= np.where((parks_df["Region"]=="nan") & ((parks_df["State"]=="TX")| (parks_df["State"]=="FL") | (parks_df["State"]=="SC")| (parks_df["State"]=="TN, NC") | (parks_df["State"]=="AR")| (parks_df["State"]=="KY")| (parks_df["State"]=="VA")), "South", parks_df["Region"])
parks_df["Region"]= np.where((parks_df["Region"]=="nan") & ((parks_df["State"]=="UT")| (parks_df["State"]=="CO") | (parks_df["State"]=="NM")| (parks_df["State"]=="CA") | (parks_df["State"]=="OR")| (parks_df["State"]=="AK")| (parks_df["State"]=="CA, NV")| (parks_df["State"]=="MT")| (parks_df["State"]=="NV")| (parks_df["State"]=="AZ")| (parks_df["State"]=="WY")| (parks_df["State"]=="HI")| (parks_df["State"]=="WA")| (parks_df["State"]=="WY, MT, ID")), "West",parks_df["Region"])


parks_df["State_FullName"] = np.where(parks_df["State"]=="ME", "Maine", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="UT", "Utah", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="SD", "South Dakota", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="TX", "Texas", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="FL", "Florida", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="CO", "Colorado", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="NM", "New Mexico", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="CA", "California", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="SC", "South Carolina", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="OR", "Oregon", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="OH", "Ohio", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="AK", "Alaska", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="CA, NV", "California/Nevada", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="MT", "Montana", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="NV", "Nevada", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="AZ", "Arizona", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="TN, NC", "Tennessee/North Carolina", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="WY", "Wyoming", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="HI", "Hawaii", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="AR", "Arkansas", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="MI", "Michigan", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="KY", "Kentucky", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="WA", "Washington", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="VA", "Virginia", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="ND", "North Dakota", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="MN", "Minnesota", parks_df["State_FullName"])
parks_df["State_FullName"] = np.where(parks_df["State"]=="WY, MT, ID", "Wyoming, Montana,Idaho", parks_df["State_FullName"])
all_data_df = pd.merge(left=parks_df, right=species_df, how='right')

NativeEffectiveness_df = pd.DataFrame(all_data_df[all_data_df["Nativeness"]=="Native"].groupby(["Region","Category","Nativeness","Occurrence","Abundance"]).size(),columns=["Count"])
NativeEffectiveness_df.reset_index(inplace=True)


NativeEffectivenessBirds_df = pd.DataFrame(all_data_df[all_data_df["Category"] =="Bird"].groupby(["Region","Category","Nativeness","Latitude","Longitude","Conservation Status"]).size(),columns=["Count"])
NativeEffectivenessBirds_df.reset_index(inplace=True)


birds = pd.DataFrame(all_data_df[all_data_df["Conservation Status"] =="Species of Concern"].groupby(["Region","Category","Nativeness","Latitude","Longitude"]).size(),columns=["Count"])
birds.reset_index(inplace=True)


agg1=species_df.groupby(['Park Name']).count()
Conservation_species_df = species_df[~species_df['Conservation Status'].isnull()]



fig1 = px.scatter(parks_df, x='Park Name',y='State', color='Acres',width=1300, height=800)

fig2 = px.scatter(parks_df, x="Latitude", y="Longitude",
                  color="Park Name", hover_name="Acres", size="Acres",
                 log_x=True, width=1300, height=600)

fig3 = px.scatter_mapbox(parks_df, lat="Latitude", lon="Longitude", color="Acres",
                         hover_name='Park Name', size="Acres", width=1100, height=600,zoom=2)
fig3.update_layout(mapbox_style="open-street-map")
# fig4 = px.sunburst(all_data_df, path=['Category','Abundance','Occurrence'], values='Acres',width=900, height=900)
fig4 = px.sunburst(NativeEffectiveness_df, path=['Region','Category','Abundance'], values='Count',width=900, height=900)


fig5 = px.bar(x=species_df['Category'].unique(), y=species_df['Category'].value_counts(), labels={'x':'Category', 'y':'count'})




famDesc ='Family: The scientific family the species belongs to'
fig7 = px.bar(x=agg1['Family'], y=species_df['Park Name'].unique())

occ_desc=' Occurrence: Whether or not the species presence in the park has been confirmed (one of "Present", "Not Confirmed", "Not Present (Historical)"'
fig9 = px.bar(x=agg1['Occurrence'], y=species_df['Park Name'].unique())


fig8 = px.histogram(species_df, x="Park Name", color="Category",width=1200, height=800)

fig10 = px.histogram(species_df, x="Family",color="Category",width=1000, height=500)



fig6 = px.histogram(Conservation_species_df, x="Category",color="Conservation Status",width=1300, height=500)


#
# d1b=Conservation_species_df.groupby(by="Conservation Status").count()
# print(d1b['Species ID'])
# p1=pd.DataFrame(list(d1b.index), columns = ["Conservation Status"])
# p2=pd.DataFrame(list(d1b['Species ID']),columns = ["count"])
# d_new= pd.concat((p1, p2), axis=1)
# fig7 = px.violin(d_new, y="count",color="Conservation Status", height=1000)
# #
#
# fig8 = px.scatter_ternary(NativeEffectivenessBirds_df, a="Latitude", b="Longitude", c="Count", hover_name="Count",
#     color="Count", size="Count",
#     color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"} )
# fig8 = px.box(NativeEffectivenessBirds_df, x="Region", y="Count")

fig7 = px.box(NativeEffectivenessBirds_df, x="Conservation Status", y="Count", color="Region",height=600)
fig7.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default



# fig8 = px/.line(NativeEffectivenessBirds_df, x='Latitude', y="Count")
fig8 = px.density_mapbox(birds, lat='Latitude', lon='Longitude', z='Count', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        mapbox_style="stamen-terrain")

#
# import plotly.graph_objects as go
# from ipywidgets import widgets
#
#
# lat = widgets.IntSlider(
#     value=1.0,
#     min=birds['Latitude'].min(),
#     max=birds['Latitude'].max(),
#     step=1.0,
#     description='Latitude:',
#     continuous_update=False
# )
#
# lon = widgets.IntSlider(
#     value=1.0,
#     min=birds['Longitude'].min(),
#     max=birds['Longitude'].max(),
#     step=1.0,
#     description='Longitude:',
#     continuous_update=False
# )
# container = widgets.HBox(children=[lat, lon])
# trace1 = go.Histogram(x=birds['Count'], opacity=0.75, name='Count of Birds')
#
# g = go.FigureWidget(data=[trace1],
#                     layout=go.Layout(
#                         title=dict(
#                             text='Number of birds has relationship with geo location?'
#                         )
#                     ))
#
#
# def response(change):
#     filter_list = [i and j for i, j in zip(birds['Latitude'] == lat.value, birds['Longitude'] == lon.value)]
#     temp_df = birds[filter_list]
#     x1 = temp_df['Count']
#     with g.batch_update():
#             g.data[0].x = x1
#             g.layout.barmode = 'overlay'
#             g.layout.xaxis.title = 'Delay in Minutes'
#             g.layout.yaxis.title = 'Number of Delays'
#
# lat.observe(response,names="value")
# lon.observe(response,names="value")
#
# vb=widgets.VBox([container,g])
#


app.layout = html.Div(children=[
    # All elements from the top of the page



    html.Div(children=[
        html.H1(children='Biodiversity in National Parks'),
        html.H2(children='Context'),
        html.H4(children=about_dataset),
        html.H2(children='Goal'),
        html.H4(children="To find out whether the bio diversity is preserved in National park? Are the animals and plants are really safe?"),
        html.H4(children="To increase the survival rate and save the lives of endangered and threatened species"),
        html.H2(children='Parks in Each State and - listing based on area'),
        dcc.Graph(
            id='graph1',
            figure=fig1
        ),
        html.H2(children='Listing of parks based on Latitude and Longitude'),
        dcc.Graph(
            id='graph2',

            figure=fig2
        ),
        html.H2(children='Listing of Parks on map , size according to area of park'),
        dcc.Graph(
            id='graph3',

            figure=fig3
        ),
        html.H2(children='Region->Category->Abundance based on count'),
        dcc.Graph(
            id='graph4',

            figure=fig4
        )
        ,
        html.H2(children='Total Count of different Family of species'),
        dcc.Graph(
            id='graph5',

            figure=fig5
        )
        ,

        html.H2(children='Count of Different family(scientific) of species Based on conservation status'),
        dcc.Graph(
            id='graph6',

            figure=fig6
        )
        ,
        html.H2(children='Birds?'),
        dcc.Graph(
            id='graph7',

            figure=fig7
        )
,
        html.H2(children='Birds with status-"Concerned Species"'),
        dcc.Graph(
            id='graph8',

            figure=fig8
        )
        # ,
        # html.H2(children='How many of them are really conserved ?'),
        # dcc.Graph(
        #     id='graph9',
        #     figure=g
        #
        # )

        # ,

        #
        # html.H4(children='Count Occurrence of species in each park '),
        # html.H5(children=occ_desc),
        # dcc.Graph(
        #     id='graph7',
        #
        #     figure=fig7
        # ),
        #
        # html.H2(children='Count Occurrence of species in each park '),
        # html.H4(children=occ_desc),
        # dcc.Graph(
        #     id='graph8',
        #
        #     figure=fig8
        # )
        # ,
        # html.H4(children='Categories of species in Family'),
        # dcc.Graph(
        #     id='graph9',
        #
        #     figure=fig9
        # )
        # ,
        #
        # html.H4(children='Categories of species in Family'),
        # dcc.Graph(
        #     id='graph9',
        #     figure=fig10
        # )
        # ,
        # html.H4(children='Count Occurrence of species in each park '),
        # html.H5(children=occ_desc),
        # dcc.Graph(
        #     id='graph10',
        #     figure=fig10
        # )
        # ,
        # html.H2(children='Species Conservation Status'),
        # dcc.Graph(
        #     id='graph11',


    ])


])



if __name__ == '__main__':
    app.run_server(debug=True)
