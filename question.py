import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import os
import base64
from multiprocessing.managers import BaseManager
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches
import io
from matplotlib import animation, rc 
import networkx as nx
import folium
import folium.plugins
from IPython.core.display import display, HTML
import codecs
from subprocess import check_output

terror_csv = pd.read_csv(r"C:\Users\ofaru\Desktop\GitHub\World_Terrorism_Analysis\gtd_data.csv",encoding="ISO-8859-1") 

terror_csv.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country', 'city':'City', 'latitude':'Latitude', 'longitude':'Longitude', 'attacktype1_txt':'AttackType', 'nkill':'Death', 'nwound':'Injured', 'gname':'Attacker','targtype1_txt':'TargetType','weaptype1_txt':'WeaponType', 'weapsubtype1_txt':'WeaponSubType', 'weapdetail':'WeaponDetail'},inplace=True)

terror_turkey=terror_csv[terror_csv["Country"]=="Turkey"]
terror_turkey_fol=terror_turkey.copy()
terror_turkey_fol.dropna(subset=["Latitude","Longitude"],inplace=True)
location_tr=terror_turkey_fol[["Latitude","Longitude"]][:5000]
city_tr=terror_turkey_fol["City"][:5000]
Death_tr=terror_turkey_fol["Death"][:5000]
Injured_tr=terror_turkey_fol["Injured"][:5000]
target_tr=terror_turkey_fol["TargetType"][:5000]

fig = plt.figure(figsize = (7,4))
def animate(Year):
    ax = plt.axes()
    ax.clear()
    ax.set_title('Terrorism In Turkey\n'+ str(Year))
    m5 = Basemap(projection='lcc',resolution='l' ,width=1800000, height=900000 ,lat_0=38.9637, lon_0=35.2433)
    lat_gif=list(terror_turkey[terror_turkey['Year']==Year].Latitude)
    long_gif=list(terror_turkey[terror_turkey['Year']==Year].Longitude)
    x_gif,y_gif=m5(long_gif,lat_gif)
    m5.scatter(x_gif, y_gif,s=[Death+Injured for Death,Injured in zip(terror_turkey[terror_turkey['Year']==Year].Death,terror_turkey[terror_turkey['Year']==Year].Injured)],color = 'r')
    m5.drawcoastlines()
    m5.drawcountries()
    m5.fillcontinents(color='coral',lake_color='aqua', zorder = 1,alpha=0.4)
    m5.drawmapboundary(fill_color='aqua')
ani = animation.FuncAnimation(fig,animate, list(terror_turkey.Year.unique()), interval = 1500) 

ani.save('animation_tr.gif', writer='imagemagick', fps=1)
plt.close(1)
filename = 'animation_tr.gif'
video = io.open(filename, 'r+b').read()
encoded = base64.b64encode(video)
HTML(data='''<img src="data:image/gif;base64,{0}" type="gif" />'''.format(encoded.decode('ascii')))