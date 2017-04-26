import pandas as pd

APP_DATA_PATH = 'Data/fuorisalone_2016_anonymous_appdata/anon_db/'

def getTimeslots(start, end):
    h1 = int(start.split(':')[0])
    h2 = int(end.split(':')[0])
    m1 = int(h1 / 6)
    m2 = int(h2 / 6) if h2 != 0 else 3
    if h1 > h2:
        res = [str(i) for i in range(m1, 4)]
        res += [str(i) for i in range(int(h2/6) + 1)]
    else:
        res = [str(i) for i in range(m1, m2 + 1)]
    res = list(set(res))
    return ','.join(sorted(res))

def writeDataframeToCSV(d, path):
    d.to_csv(path, index = False)

df = pd.read_csv(APP_DATA_PATH + 'event.csv', encoding = 'latin1')
df = df.drop(['id_location', 'indirizzo', 'nome', 'num_events', ], axis = 1)

new_col = [getTimeslots(row['ora_inizio'], row['ora_fine']) for index, row in df.iterrows()]
df['timeslot'] = pd.Series(new_col)

df.drop(['data', 'ora_inizio', 'ora_fine'], axis = 1, inplace = True)
df = df.drop_duplicates()

l = len(df)
for i in range(len(df)):
    row = df.iloc[i]
    # Build the list of new lines to be added, the lines are equal to the row with
    # the exception for the 'days' column
    slot_list = row['timeslot'].split(',')
    lines = [row.copy(deep=True) for k in range(len(slot_list))]
    for j in range(len(slot_list)):
        lines[j]['timeslot'] = slot_list[j]
    df = pd.concat([df, pd.DataFrame(lines)])
df = df.iloc[:].reset_index(drop=True)
df = df.drop_duplicates()

writeDataframeToCSV(df, APP_DATA_PATH + 'events_with_timeslots.csv')