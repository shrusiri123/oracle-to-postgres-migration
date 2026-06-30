pd.read\_sql(query, connection)  →  Run SQL, get DataFrame

len(df)                         →  COUNT(\*) 

df.columns                      →  column names

df.equals(other\_df)             →  compare two tables

df.compare(other\_df)            →  show differences

df.columns.str.lower()          →  lowercase all column names

df\['column\_name']               →  SELECT one column

df\[df\['city'] == 'Mumbai']      →  WHERE city = 'Mumbai'

