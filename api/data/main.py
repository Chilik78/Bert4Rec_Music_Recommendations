import pandas as pd

#лишие столбцы, неправильные данные, пустые строки, переименование столбцов

#первичная информация о датасете
df = pd.read_csv('dataset.csv',encoding='utf-8')
print(df.info())
print(df)

#удаление лишних столбцов
df.drop(['duration_ms','explicit','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature'], axis=1, inplace=True)
print(df.info())
print(df)

#Вывод информации по столбцам с повторами в строках
print(df.popularity.unique(),'\n Кол-во уникальных значений: ', df.popularity.nunique(dropna=True))
print(df.track_genre.unique(),'\n Кол-во уникальных значений: ', df.track_genre.nunique(dropna=True))

#Удаление повторов в строках 
cleaned_df = df.dropna()

print("Очищенный DataFrame:\n", cleaned_df)
df.to_csv('preprocessed.csv', index=False, header=True)

