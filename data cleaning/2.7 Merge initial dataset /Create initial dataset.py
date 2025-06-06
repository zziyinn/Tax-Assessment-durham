#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd


# In[ ]:


# read data
block_groups = pd.read_csv('2024_10_All_Durham_BlockGroups_with_race_neighborhoods.csv')
sales_info = pd.read_excel('qualified-residential-sales-info-2021-2024.xlsx')


# In[ ]:


# ====== Step 1: Preprocessing and column mapping ======
# Block group data column mapping
bg_mapping = {
    'REID': 'REID',
    'PIN': 'PIN',
    'PIN_EXT': 'PIN_EXT',
    'LOCATION_ADDR': 'LOCATION_ADDR',
    'LAND_CLASS': 'LAND_CLASS',
    'TOTAL_PROP_VALUE': 'TOTAL_PROP_VALUE',
    'VCS': 'VCS',
    'NEIGHBORHOOD': 'name_2',
    'gid': 'gid', 
    'race_asian_per': 'PERCENT_ASIAN',
    'race_black_per': 'PERCENT_BLACK',
    'race_hispanic_per': 'PERCENT_HISPANIC',
    'race_white_per': 'PERCENT_WHITE'
}

# Sales data column mapping
sales_mapping = {
    'REID': 'REID',
    'PIN': 'PIN',
    'PIN_EXT': 'PIN_EXT',
    'PRICE': 'PRICE',
    'SALE_DATE': 'SALE_DATE',
    'VCS': 'VCS',
    'LOCATION_ADDR': 'LOCATION_ADDR'
}


# In[ ]:


# ====== Step 2: Data Cleaning and Renaming ======
# Process block group data
bg_selected = block_groups[bg_mapping.keys()].rename(columns=bg_mapping)
bg_selected['Source'] = '2024_10_All_Durham_BlockGroups'

# Processing of sales data (including de-weighting)
sales_clean = sales_info.drop_duplicates(subset=['REID'])
sales_selected = sales_clean[sales_mapping.keys()].rename(columns=sales_mapping)
sales_selected['Source'] = 'qualified-residential-sales'


# In[ ]:


# ====== Step 3: Data Merge ======
# Use left joins to retain all block group data
merged = pd.merge(
    bg_selected,
    sales_selected,
    on='REID',
    how='left',
    suffixes=('_block', '_sales')
)


# In[ ]:


# ====== Step 4: Final Data Structure Adjustment ======
# Define the final output format
final_output = pd.DataFrame({
    'Source Name': [
        *['BlockGroups']*len(bg_mapping),
        *['SalesInfo']*len(sales_mapping)
    ],
    'Variable (our name)': [
        *bg_mapping.values(),
        *sales_mapping.values()
    ],
    'Source': [
        *[f"{bg_selected['Source'].iloc[0]}"]*len(bg_mapping),
        *[f"{sales_selected['Source'].iloc[0]}"]*len(sales_mapping)
    ]
})


# In[ ]:


# ====== Step 5: Data validation and saving ======
# Check the merge results
print(f"Number of records after consolidation: {len(merged)}")
print("top 5 records:")
print(merged.head())

# Save
merged.to_csv('Durham_BlockGroups_with_Sales_Merged.csv', index=False)
final_output.to_csv('Data_Dictionary.csv', index=False)

print("completed! Generate two files：")
print("- Durham_BlockGroups_with_Sales_Merged.csv")
print("- Data_Dictionary.csv")


# In[ ]:




