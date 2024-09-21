import pandas as pd

def normalize_columns(df:pd.DataFrame):
    new_cols = [col.strip().lower() for col in df.columns]
    new_cols[0] = 'id'
    df.columns = new_cols
    df[['userid', 'track', 'artist', 'genre']] = df[['userid', 'track', 'artist', 'genre']].astype('string')

def drop_extra_columns(df:pd.DataFrame):
    df.drop(columns=['time', 'day'], axis=1, inplace=True)
    
def drop_voids(df:pd.DataFrame):
    df.dropna(axis=0, inplace=True)

def preprocessing(csv_filename:str):
    df = pd.read_csv(csv_filename)
    df.info()
    normalize_columns(df)
    drop_extra_columns(df)
    drop_voids(df)
    df.info()
    df.to_csv('preprocessed.csv', index=False)


if __name__ == '__main__':
    filename = 'music_project.csv'
    preprocessing(filename)