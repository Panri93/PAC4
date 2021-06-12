import utils
import pandas as pd

# Introduïm els diferents path per les diferents fonts de dades
path = "/home/datasci/PycharmProjects/PAC4/data/covid_approval_polls.csv"
path2 = "/home/datasci/PycharmProjects/PAC4/data/covid_concern_polls.csv"
path3 = "/home/datasci/PycharmProjects/PAC4/data/pollster_ratings.xlsx"
# Cridem la funció del Exercici_1
print("================= RESULTATS DEL EXERCICI 1 =================")
utils.exercici_1(path)
# Cridem la funció del Exercici_2
print("================= RESULTATS DEL EXERCICI 2 =================")
approval_polls, concern_polls, pollster_ratings = utils.exercici_2(path, path2, path3)
# Cridem la funció del Exercici_3
print("================= RESULTATS DEL EXERCICI 3 =================")
utils.exercici_3(df=approval_polls)
# Cridem la funció del Exercici_4
print("================= RESULTATS DEL EXERCICI 4 =================")
merged_df = utils.exercici_4(dt=concern_polls, ds=pollster_ratings)
# Cridem la funció del Exercici_5
print("================= RESULTATS DEL EXERCICI 5 =================")
utils.exercici_5(dz=merged_df)



