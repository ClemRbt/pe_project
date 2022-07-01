#!/usr/bin/env python
# coding: utf-8

 
import streamlit as st
import sys
import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd 
import pickle 
from sklearn.metrics import accuracy_score 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split
from pages import model 
st.title('Etude Pole emploi') 
st.subheader('By Clement ROBERT')

print(f"Python version : {sys.version}")
st.write("Requete d'un jeu de données sur API PE puis eda et modelisation !") 


url_app = r"streamlit run pe_project_streamlit/home.py".replace('\\', '/')
print(f"Run app : {url_app}")

