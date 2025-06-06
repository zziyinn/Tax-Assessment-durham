#!/usr/bin/env python
# coding: utf-8

# In[2]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd

# read data
df = pd.read_csv("2024_10_All_Durham_BlockGroups_with_race_neighborhoods.csv")


# In[3]:


# Calculate the racial mean for the VCS group
vcs_grouped = df.groupby("VCS")[["race_asian_per", "race_black_per", "race_hispanic_per", "race_white_per"]].mean().reset_index()
vcs_grouped.rename(columns={
    "race_asian_per": "VCS_PERCENT_ASIAN",
    "race_black_per": "VCS_PERCENT_BLACK",
    "race_hispanic_per": "VCS_PERCENT_HISPANIC",
    "race_white_per": "VCS_PERCENT_WHITE"
}, inplace=True)

# Calculate the racial mean for the Neighborhood group.
neighborhood_grouped = df.groupby("name_2")[["race_asian_per", "race_black_per", "race_hispanic_per", "race_white_per"]].mean().reset_index()
neighborhood_grouped.rename(columns={
    "race_asian_per": "N_PERCENT_ASIAN",
    "race_black_per": "N_PERCENT_BLACK",
    "race_hispanic_per": "N_PERCENT_HISPANIC",
    "race_white_per": "N_PERCENT_WHITE"
}, inplace=True)


# In[4]:


# Merge race data from VCS groups to raw data
df_vcs = df.merge(vcs_grouped, on="VCS", how="left")

# Merge race data from Neighborhood  groups to raw data
df_neighborhood = df.merge(neighborhood_grouped, on="name_2", how="left")

# Save VCS dataset
df_vcs_final = df_vcs[["VCS", "VCS_PERCENT_ASIAN", "VCS_PERCENT_BLACK", "VCS_PERCENT_HISPANIC", "VCS_PERCENT_WHITE"]].drop_duplicates()
df_vcs_final.to_csv("VCS_grouped_race_data.csv", index=False)

# Save Neighborhood data
df_neighborhood_final = df_neighborhood[["name_2", "N_PERCENT_ASIAN", "N_PERCENT_BLACK", "N_PERCENT_HISPANIC", "N_PERCENT_WHITE"]].drop_duplicates()
df_neighborhood_final.to_csv("Neighborhood_grouped_race_data.csv", index=False)

print("saved")


# In[ ]:




