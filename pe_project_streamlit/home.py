#!/usr/bin/env python
# coding: utf-8


import streamlit as st
import requests
import pandas as pd
import json
from pages import model

st.sidebar.markdown("Importation")

st.markdown("Importation via API")
file_upload = st.file_uploader('Upload your own penguin data') 



def get_access_token(url, params):
    url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/%2Fpartenaire"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response_token = requests.post(url,
                            headers=headers,
                            params=params,
                            timeout=25
                            )
    response_token.close()

    bytes_response_token = response_token.content.decode('utf8').replace("'", '"')
    json_response_token = json.loads(bytes_response_token)
    return(json_response_token.get("access_token"))

params = {
    "grant_type": "client_credentials",
    "client_id": "PAR_projetds_ab7f9c4312021e5eef9a6dd1598b31a6ff2359766f66e233994a2ebca72ddab9",
    "client_secret": "00b21ca69d191237497a1fcb2ad08c848a9304c4b4a80fea87cbf675de6b3a25",
    "scope": "api_infotravailv1"
}
access_token = get_access_token(url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/%2Fpartenaire", 
                                params=params)
st.write("Access token généré avec succès")


def get_list_of_bdd(url, access_token):

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response_liste_BDD = requests.get(url,headers=headers, timeout=25)

#     print(dir(response_liste_BDD))

    bytes_response_liste_BDD = response_liste_BDD.content.decode('utf8').replace("'", '"')
    # print(f"bytes_response_liste_BDD : {bytes_response_liste_BDD}")
    json_response_liste_BDD = json.loads(bytes_response_liste_BDD)
    # print(json_response_liste_BDD)
    print("\n")
    # print_dict_like_json_prettify(json_response_liste_BDD, 4)

    print(json_response_liste_BDD.get("result").keys())

    # print(len([dic for dic in json_response_liste_BDD.get("result").get("packages") if dic.get("type")=="dataset"]))
    list_dataset_dic = [dic for dic in json_response_liste_BDD.get("result").get("packages") if dic.get("type")=="dataset"]
    # [print(f"\n\n{print_dict_like_json_prettify(e,4)}") for e in list_dataset_dic if list(e) in ["id", "title", "notes"]]
    # [print(f"\n\n{list(e)}") for e in list_dataset_dic]

    #print([e for e in range(len(list_dataset_dic))])

    list_dataset_dic_ft=list()
    for e in range(len(list_dataset_dic)):
        list_dataset_dic_ft.append({your_key: list_dataset_dic[e][your_key] for your_key in ["id", "title", "notes"] })
    #     print("\n")
    #[print(f"{e}\n") for e in list_dataset_dic_ft]
    return(list_dataset_dic_ft)
    

list_bdd = get_list_of_bdd(url="https://api.emploi-store.fr/partenaire/infotravail/v1/organization_show?id=digidata",
                access_token=access_token)

st.write("Voici la liste des BDD \n :")
st.write(list_bdd)











import pandas as pd
def read_bdd(url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response_first_BDD = requests.get(url,headers=headers, timeout=25)

#     print(dir(response_first_BDD))
    # print(response_first_BDD.content)
    bytes_response_first_BDD = response_first_BDD.content
    # print(bytes_response_first_BDD)
    json_response_first_BDD = json.loads(bytes_response_first_BDD)
#     print_dict_like_json_prettify(json_response_first_BDD, 4)
    list_ressources = json_response_first_BDD.get("result").get("resources")
    # print(list_ressources)
    list_ressources_filter=list()
    for e in range(len(list_ressources)):
        list_ressources_filter.append({your_key: list_ressources[e][your_key] for your_key in ["id", "name", "description", 
                                                                                               "pe_source", "pe_version", 
                                                                                               "size"]}) , #"pe_status"
#     [print(f"{e}\n") for e in list_ressources_filter]
    return(list_ressources_filter)
    

identifiant_bdd = "80341a24-a451-49ec-b6b0-1b8756fe977d" 
url_bdd = f"https://api.emploi-store.fr/partenaire/infotravail/v1/package_show?id={identifiant_bdd}"
st.write("Voici la liste des ressources dans la BDD {} \n :".format(identifiant_bdd))
#list_ressources_filter = read_bdd(url_bdd, access_token)
#st.write(list_ressources_filter)

#list_dfs = [key for key,val in  locals().items() if "df_" in key]
#st.write("Voici le noms des {0} variables correspondants aux dfs créées : {1}".format(len(list_dfs),list_dfs))









def import_ressources(url, access_token):
    pd.set_option('display.max_columns', 500)
    # GET https://api.emploi-store.fr/partenaire/infotravail/v1/datastore_search_sql?sql=SELECT * FROM {identifiant_r} LIMIT 5 
    # WHERE \"CITY_NAME\" = \"NANTES\" 
    # WHERE \"DEPARTEMENT_NAME\" = \"LOIRE-ATLANTIQUE\" 
    # AND \"MAXIMUM_SALARY\" > 16000
    # cast(\"MAXIMUM_SALARY\" as float)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response_first_BDD = requests.get(url,headers=headers)

    #     print(dir(response_first_BDD))
    # print(response_first_BDD.content)
    bytes_response_first_BDD = response_first_BDD.content
    # print(bytes_response_first_BDD)
    json_response_first_BDD = json.loads(bytes_response_first_BDD)

    # print_dict_like_json_prettify(json_response_first_BDD, 4)

    json_response_first_BDD.get("result").get("fields")

    # df = pd.DataFrame.from_records(json_response_first_BDD.get("result").get("records"))
    # display(df)

    #     print(json_response_first_BDD.get("result").get("fields"))
    type_dict=dict()
    for elem in json_response_first_BDD.get("result").get("fields"):
        if elem.get("type")=="int4":
            type_dict[elem.get("id")]="int"
        if elem.get("type")=="text":
            type_dict[elem.get("id")]="object"
            
    df = pd.DataFrame.from_dict(json_response_first_BDD.get("result").get("records")).astype(type_dict)
    df = df.drop(["_full_text"], axis=1, errors="ignore").set_index("_id")
    return(df)
            
            
identifiant_r = "e49af0f2-8d00-4a54-9124-2f4107efa810" 
nb_elem_ressources = "500"
offset = "1"
url_ressources = f'https://api.emploi-store.fr/partenaire/infotravail/v1/datastore_search_sql?sql=SELECT * FROM \"{identifiant_r}\" WHERE \"DEPARTEMENT_NAME\" = \'LOIRE-ATLANTIQUE\' AND \"MAXIMUM_SALARY\" <> \'\' LIMIT {nb_elem_ressources}'

df = import_ressources(url_ressources, access_token)
st.subheader("Voici la ressource {} : \n ".format(identifiant_r))

st.dataframe(df.head(5))


st.write(model.describe_df(df, graph=True))






#if submit : 
#    st.write("Yo")
#    st.write(print("yo"))



#st.write(penguins_df.head())