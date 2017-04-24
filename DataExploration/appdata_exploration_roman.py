import pandas as pd
import json
from pandas.io.json import json_normalize
import gmplot

#############################
# Parse jsons to dataframes #
#############################
def convertToDataframe(path):
    with open(path, 'r', encoding='utf8') as f:
        text = f.read()
    objects = text.split('\n')
    json_data = []
    for o in objects:
        try:
            json_data.append(json.loads(o))
        except:
            pass
    return json_normalize(json_data)

# Parse json events to dataframe
df_event = convertToDataframe("Data/fuorisalone_2016_anonymous_appdata/anon_db/event.json")

# Parse json locations of the events to dataframe
df_location = convertToDataframe("Data/fuorisalone_2016_anonymous_appdata/anon_db/location.json")

# Parse json user participations to events
df_participations = convertToDataframe("Data/fuorisalone_2016_anonymous_appdata/anon_db/events_analytic.json")

# Parse json user positions
df_user_positions = convertToDataframe("Data/fuorisalone_2016_anonymous_appdata/anon_db/position.json")
df_agenda = convertToDataframe("Data/fuorisalone_2016_anonymous_appdata/anon_db/agenda.json")
df_agenda_analytics = convertToDataframe("Data/fuorisalone_2016_anonymous_appdata/anon_db/agenda_analytics.json")



##################
# EXPLORE EVENTS #
##################
# Perform the join of the two dataframes
df_joined = pd.merge(df_event, df_location, left_on='location', right_on='id')

# Drop useless colums for the prediction
labels_to_drop = ['created_x', 'author', 'award', 'contatti.en', 'contatti.it', 
                  'descrizione.en', 'descrizione.it', 'event_image', 'intro.en', 
                  'intro.it', 'itineraries', 'modified_x', 'photos', 'titolo.en',
                  'titolo.it', 'updated_x', 'url_x', 'url_en', 'url_it', '_id.$oid_x',
                  '_id.$oid_y', 'created_y', 'modified_y', 'updated_y', 'url_y',
                  'location', 'menu_pos', 'sponsor_event', 'status_x', 'status_y',
                  'slug.en', 'slug.it', 'slug', 'designers']
df_joined.drop(labels_to_drop, axis = 1, inplace = True)

# Rename columns
df_joined = df_joined.rename(columns={'id_x': 'id_event', 'id_y': 'id_location'})

# Explode 'days' column into multiple lines
for i in range(1,len(df_joined)):
    row = df_joined.iloc[i]
    # Build the list of new lines to be added, the lines are equal to the row with
    # the exception for the 'days' column
    days = row[2]
    lines = [row.copy(deep=True) for k in range(len(days))]
    for j in range(len(days)):
        lines[j][2] = {'dataora_fine': days[j]['dataora_fine'], 
                     'dataora_inizio': days[j]['dataora_inizio']}
    df_joined = pd.concat([df_joined, pd.DataFrame(lines)]).reset_index(drop=True) 
df_joined = df_joined.iloc[1148:].reset_index(drop=True)

# Extract data, ora_inizio and ora_fine from days column, and categories
df_joined['data'] = df_joined['days'].map(lambda x: x['dataora_fine'].split()[0])
df_joined['ora_inizio'] = df_joined['days'].map(lambda x: x['dataora_inizio'].split()[1])
df_joined['ora_fine'] = df_joined['days'].map(lambda x: x['dataora_fine'].split()[1])
df_joined['categories'] = df_joined['categories'].map(lambda x: 
                            [c['nome']['it'] for c in x])
df_joined = df_joined.drop('days', axis=1)
df_joined = df_joined.drop('brands', axis=1)

# Plot events to map
def plotToMap(df, filename): 
    lat = [float(x) for x in df['latitude']]
    lng = [float(x) for x in df['longitude']]
    gmap = gmplot.GoogleMapPlotter(45.482291, 9.1875001, 13)
    gmap.scatter(lat, lng, "#000000", size = 10, marker = False)
    gmap.heatmap(lat, lng, radius=50, threshold=1, opacity=0.7)
    gmap.draw(filename)
    
plotToMap(df_joined, 'events_map.html')


# Assign events to geographical zones
import math
DEG_DIST_LAT = 111142
DEG_DIST_LON = 78100
df_events_zones = df_joined
df_events_zones['latitude'] = df_joined['latitude'].map(lambda x: float(x))
df_events_zones['longitude'] = df_joined['longitude'].map(lambda x: float(x))
zones = {"Brera" : {'latitude': 45.472879, 'longitude' : 9.185288, 'radius': 750}, 
         "Tortona":{'latitude': 45.452803, 'longitude' : 9.166398, 'radius': 750},
         "Quadrilatero":{'latitude': 45.466730, 'longitude' : 9.197431, 'radius': 500},
         "Lambrate":{'latitude': 45.484270, 'longitude' :  9.242877, 'radius': 750},
         }
def belong_to(latitude, longitude):
    for zone in zones.keys():
        if math.sqrt((abs(zones[zone]['latitude'] - latitude) * DEG_DIST_LAT)**2 + (abs(zones[zone]['longitude'] - longitude) * DEG_DIST_LON)**2) < zones[zone]['radius']:
            return zone
    return ''
df_events_zones['zone'] = pd.Series([belong_to(row['latitude'],row['longitude'] )for index, row in df_events_zones[['latitude', 'longitude']].iterrows()])
df_events_zones = df_events_zones[df_events_zones.zone != '']
plotToMap(df_events_zones, 'events_map_in_zones.html')



###################################################
# EXPLORE USER PARTICIPATIONS IN AGENDA ANALYTICS #
###################################################
df_participations['date'] = pd.to_datetime(df_participations['date'], unit = 'ms')