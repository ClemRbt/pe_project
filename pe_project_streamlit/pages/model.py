#!/usr/bin/env python
# coding: utf-8

import streamlit as st

st.sidebar.markdown("Model")

st.markdown("Modelisation")



from matplotlib import pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer


def describe_df(df, verbose=False, graph=False): 
    st.write("Dimensions du df : {}".format(df.shape))
    #if verbose ==True:
        #[st.write("Colonnes {0} : {1}".format(col:-<25,typ)) for col, typ in zip(df.columns, df.dtypes.tolist())]
    st.write("Répartition des types de colonnes :\n")
    st.write(df.dtypes.value_counts().astype(str))
    if graph == True:
        st.write("Répartion des types : \n :")
        fig, ax = plt.subplots()
        st.pyplot(df.dtypes.value_counts().plot.pie(autopct='%1.0f%%'))
        #plt.show()


def convert_columns_to_int(df):
    list_col_convert_to_int = []
    for col in df.columns:
        if (sum(df[col].astype(str).str.isnumeric())> 1 and "code" not in col.lower() and "name" not in col.lower()
        and len(df[~(df[col]=="")][col])>1 and len(df[~(df[col].astype(str)=="None")][col])>1):
            df[col] = df[col].replace("", np.nan).astype(float)
            list_col_convert_to_int.append(col)
    print(f"Colonnes converties en int : \n {list_col_convert_to_int}\n")
    return(df)

def convert_col_to_object(df):
    list_col_convert_to_obj = []
    for col in df.columns:
        if  "_code" in col.lower() or "flag" in col.lower() :
            df[col] = df[col].astype(object)
            list_col_convert_to_obj.append(col)
    print(f"Colonnes converties en object : \n {list_col_convert_to_obj}\n")
    return(df)


def drop_col_with_less_threshold_variance(df, threshold, liste_exclude_col=[], verbose=False):
    liste_col_low_variance = []
    for col in df.select_dtypes(include=[np.number]):
        if verbose==True:
            print(f"Variance {col:-<25} : {round(df[col].dropna().var(),2)}")
        if df[col].var()<= threshold and col not in liste_exclude_col :
            liste_col_low_variance.append(col)
    df.drop(liste_col_low_variance, axis=1, inplace=True)
    print(f"Colonnes avec moins de {threshold} de variance suprimées en excluant {liste_exclude_col}: \
    \n {liste_col_low_variance} \n")
    return(df)

def drop_col_with_more_threshold_nan(df, pct_threshold, liste_exclude_col=[], verbose=False):
    missing_rate = (df.isna().sum()/df.shape[0]).sort_values(ascending=False)
    series_ft = missing_rate[missing_rate>pct_threshold]
    if verbose==True:
        print(series_ft)
    liste_col_more_nan = [col for col in series_ft.index.tolist() if col not in liste_exclude_col]
    df.drop(liste_col_more_nan, axis=1, inplace=True)
    print(f"\nColonnes avec plus de {pct_threshold*100} % de nan supprimées: \n {liste_col_more_nan} \n")
    return(df)


