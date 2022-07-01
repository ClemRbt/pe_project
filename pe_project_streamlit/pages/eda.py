#!/usr/bin/env python
# coding: utf-8


import streamlit as st

st.sidebar.markdown("EDA")

st.markdown("Analyse exploratoire")

st.dataframe(df.head(5))

