import pandas as pd
import json
from pandas.io.json import json_normalize

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

# Perform the join of the two dataframes
df_joined = pd.merge(df_event, df_location, left_on='location', right_on='id')

# Drop useless colums for the prediction
#pd.to_datetime(df_joined['created_x'], unit = 'ms')
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