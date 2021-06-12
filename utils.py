import matplotlib.pyplot as plt
import re
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')


def exercici_1(path):
    """Mostra el nombre de occurrències de la paraula Huffington Post i
       urls acabades en .pdf o .pdf/.
       Parameters:
           path: Ruta del fitxer font que conté les dades de covid_approval_polls.csv.
    """
    with open(path, "r") as file1:
        file1 = file1.read()
        # Contamos el numero de occurrencias de Huffington Post
        counter1 = file1.count('Huffington Post')
        # Contamos el numero de occurrencias de urls terminadas en .pdf o .pdf/
        counter2 = re.findall(r"(https?://.*\.pdf/?$)", file1, flags=re.MULTILINE)
        print('The pattern Huffington_Post appears', counter1, "times")
        print('The pattern url_pdf appears', len(counter2), "times")


def exercici_2(path, path2, path3):
    """Retorna el df approval_polls, concern_polls, pollster_ratings filtrat amb gent no banejada
       i en mostra les seves dimensions.
        Parameters:
        path: Ruta del fitxer font que conté les dades de covid_approval_polls.csv.
        path2: Ruta del fitxer font que conté les dades de covid_concern_polls.csv
        path3: Ruta del fitxer font que conté les dades de pollster_ratings.xlsx.
    """
    # Creació dels df a partir dels fitxers font
    df1 = pd.read_csv(path)
    df2 = pd.read_csv(path2)
    df3 = pd.read_excel(path3)
    # Filtratge de dataframe
    newdf1 = df1[df1["tracking"] == False]
    newdf2 = df2[df2["tracking"] == False]
    newdf3 = df3[df3["Banned by 538"] == "no"]
    # Creació de approval_polls i concern_polls
    approval_polls = newdf1[newdf1['pollster'].isin(set(newdf3['Pollster']))]
    concern_polls = newdf2[newdf2['pollster'].isin(set(newdf3['Pollster']))]
    print("Les dimensions del dataset approval_polls són", approval_polls.shape)
    print("Les dimensions del dataset concern_polls són", concern_polls.shape)
    return approval_polls, concern_polls, newdf3


def exercici_3(df):
    """Mostra un gràfic dels partits amb el nombre de persones que aproven (approve) i el nombre de persones que
       desaproven (disapprove), per a les preguntes que contenen les paraules Trump i coronavirus en el text.
       Parameters:
       df: Paràmetre d'entrada tipus dataframe, approval_polls.
    """
    # Filtrem dataset per atribut text que contingui paraula Trump i coronavirus
    approval_polls = df[(df['text'].str.contains("Trump", case=False)) &
                        (df['text'].str.contains("coronavirus", case=False))].copy()
    # Realitzem càlculs
    approval_polls["n_approve"] = (approval_polls["approve"] / 100) * approval_polls["sample_size"]
    approval_polls["n_disapprove"] = (approval_polls["disapprove"] / 100) * approval_polls["sample_size"]

    # Agrupem per partit
    resultats = approval_polls.groupby(by=["party"]).sum()
    # Muntem el dataframe que s'usarà per plotejar
    approve = resultats['n_approve']
    disapprove = resultats['n_disapprove']
    plotdata = pd.DataFrame({"approve": approve,
                             "disapprove": disapprove}, index=["D", "I", "R", "all"])
    # Plotegem
    plotdata.plot(kind='bar', color=['green', 'red'])
    plt.title("Approve/Disapprove by party")
    plt.xlabel("Party")
    plt.ylabel("Count")
    print("Veure gràfic Approve/Disapprove by party")
    plt.show()


def exercici_4(dt, ds):
    """Mostra el nombre de entrevistats per pantalla.
       Mostra el nombre de entrevistats 'very' i 'not_at_all' preocupats per l'economia i també un gràfic.
       Mostra el % de entrevistats 'very' i 'not_at_all' preocupats per infected i també un gràfic.
       Mostra el nombre d'entrevistats per grau de pollster i també un gràfic
       Parameters:
           dt: Paràmetre d'entrada tipus dataframe, concern_polls.
           ds: Paràmetre d'entrada tipus dataframe, pollster_ratings amb filtratge not banned.
    """
    # 4.1
    print("El número de entrevistats és:", dt['sample_size'].sum())
    # 4.2
    datados = dt[dt['subject'] == "concern-economy"].copy()
    datados["n_very"] = (datados["very"] / 100) * datados["sample_size"]
    datados["n_not_at_all"] = (datados["not_at_all"] / 100) * datados["sample_size"]
    uno = datados['n_very'].sum()
    dos = datados['n_not_at_all'].sum()
    plotdatados = pd.DataFrame({"values": [uno, dos]}, index=["very", "not_at_all"])
    # Plotegem
    plotdatados.plot(kind='bar')
    plt.title("Grau de preocupacio - Economia")
    plt.xlabel("Grau de preocupacio")
    plt.ylabel("Count")
    print("El número de entrevistats molt preocupats per l'economia és:", uno)
    print("El número de entrevistats no gaire preocupats per l'economia és:", dos)
    plt.show()
    # 4.3
    datatres = dt[dt['subject'] == "concern-infected"].copy()
    datatres["n_very"] = (datatres["very"] / 100) * datatres["sample_size"]
    datatres["n_not_at_all"] = (datatres["not_at_all"] / 100) * datatres["sample_size"]
    pervery = ((datatres["n_very"].sum()) / datatres["sample_size"].sum()) * 100
    pernot = ((datatres["n_not_at_all"].sum()) / datatres["sample_size"].sum()) * 100
    plotdatatres = pd.DataFrame({"values": [pervery, pernot]}, index=["very", "not_at_all"])
    # Plotegem
    plotdatatres.plot(kind='bar')
    plt.title("Grau de preocupacio - Infected")
    plt.xlabel("Grau de preocupacio")
    plt.ylabel("%")
    print("El % de entrevistats molt preocupats per infected és:", pervery)
    print("El % de entrevistats  no gaire preocupats per infected és:", pernot)
    plt.show()
    # 4.4
    # Fem els canvis en el dataset per deixar les notes que interessen
    ds['538 Grade'] = ds['538 Grade'].replace(
        {"A-": "A", "A+": "A", "A/B": "B", "B-": "B", "B+": "B", "B/C": "C",
         "C-": "C", "D-": "D"})
    # Renombrem el nom de la columna per poder fer un join posterior
    ds = ds.rename(columns={'Pollster': 'pollster'})
    # Fem un left join
    merged_df = dt.merge(ds, on='pollster', how='left')
    # Agrupem per nota
    merge = merged_df.groupby(['538 Grade'])['sample_size'].sum()
    print("El nombre d'entrevistats per nota és:")
    print(merge)
    merge.plot(kind='bar')
    plt.title('Entrevistats per nota')
    plt.xlabel('Nota')
    plt.ylabel('Count')
    plt.show()
    return merged_df

def exercici_5(dz):
    """Mostra un gràfic amb el nombre de persones segons nivell de preocupació després del 2020-09-01.
       Mostra un gràfic amb el nombre de persones segons nivell de preocupació abans del 2020-09-01.
       Mostra un gràfic amb el percentatge de persones segons nivell de preocupació després del 2020-09-01.
       Mostra un gràfic amb el percentatge de persones segons nivell de preocupació abans del 2020-09-01.
       Parameters:
           dz: Paràmetre d'entrada tipus dataframe.
    """
    # Reemplacem les calificacions per valors
    dz['538 Grade'] = dz['538 Grade'].replace({"A": 1, "B": 0.5, "C": 0, "D": -0.5})
    # Afegim nova columna credibilitat
    dz['credibilitat'] = dz['538 Grade'] + dz['Predictive    Plus-Minus']
    # Ens quedem amb els registres que compleixen amb la condició i creem dos datasets
    merged_df_abans = dz.loc[(dz['credibilitat'] >= 1.5) & (dz['end_date'] < '2020-09-01')]
    merged_df_despres = dz.loc[(dz['credibilitat'] >= 1.5) & (dz['end_date'] > '2020-09-01')]
    # Fem els càlculs
    # Abans
    very_abans = (((merged_df_abans['very'] * merged_df_abans['sample_size']) / 100).sum())
    somewhat_abans = (((merged_df_abans['somewhat'] * merged_df_abans['sample_size']) / 100).sum())
    not_very_abans = (((merged_df_abans['not_very'] * merged_df_abans['sample_size']) / 100).sum())
    not_at_all_abans = (((merged_df_abans['not_at_all'] * merged_df_abans['sample_size']) / 100).sum())
    # Després
    very_despres = (((merged_df_despres['very'] * merged_df_despres['sample_size']) / 100).sum())
    somewhat_despres = (((merged_df_despres['somewhat'] * merged_df_despres['sample_size']) / 100).sum())
    not_very_despres = (((merged_df_despres['not_very'] * merged_df_despres['sample_size']) / 100).sum())
    not_at_all_despres = (((merged_df_despres['not_at_all'] * merged_df_despres['sample_size']) / 100).sum())
    # Muntem dataframe i plotegem
    data = {"Abans": [very_abans, somewhat_abans, not_very_abans, not_at_all_abans],
            "Despres": [very_despres, somewhat_despres, not_very_despres, not_at_all_despres]}
    plotdatacinc = pd.DataFrame(data=data, index=["very", "somewhat", "not_very", "not_at_all"])
    plotdatacinc.plot(kind='bar')
    plt.title("Nombre de entrevistats per nivell de preocupació abans i després de 2020-09-01")
    plt.xlabel("Grau de preocupacio")
    plt.ylabel("Count")
    print("El nombre de persones per nivell de preocupació és:")
    print(plotdatacinc)
    plt.show(block=True)
    # Percentatges
    # Abans
    per_very_abans = ((very_abans).sum() / merged_df_abans['sample_size'].sum()) * 100
    per_somewhat_abans = ((somewhat_abans).sum() / merged_df_abans['sample_size'].sum()) * 100
    per_not_very_abans = ((not_very_abans).sum() / merged_df_abans['sample_size'].sum()) * 100
    per_not_at_all_abans = ((not_at_all_abans).sum() / merged_df_abans['sample_size'].sum()) * 100
    # Despres
    per_very_despres = ((very_despres).sum() / merged_df_despres['sample_size'].sum()) * 100
    per_somewhat_despres = ((somewhat_despres).sum() / merged_df_despres['sample_size'].sum()) * 100
    per_not_very_despres = ((not_very_despres).sum() / merged_df_despres['sample_size'].sum()) * 100
    per_not_at_all_despres = ((not_at_all_despres).sum() / merged_df_despres['sample_size'].sum()) * 100
    # Muntem dataframe i plotegem
    datados = {"%Abans": [per_very_abans, per_somewhat_abans, per_not_very_abans, per_not_at_all_abans],
               "%Despres": [per_very_despres, per_somewhat_despres, per_not_very_despres, per_not_at_all_despres]}
    plotdatasis = pd.DataFrame(data=datados, index=["very", "somewhat", "not_very", "not_at_all"])
    plotdatasis.plot(kind='bar')
    plt.title("% Entrevistats per nivell de preocupació despres de 2020-09-01")
    plt.xlabel("Grau de preocupacio")
    plt.ylabel("Count")
    print("El percentatge de persones per nivell de preocupació és:")
    print(plotdatasis)
    plt.show(block=True)