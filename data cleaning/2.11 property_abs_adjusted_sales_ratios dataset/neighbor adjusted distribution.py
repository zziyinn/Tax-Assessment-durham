#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd

def process_sales_data(file_path):
    """Main function: Process sales data and calculate key metrics"""
    
    # 1. Read data
    df = pd.read_csv(file_path)
    
    # 2. Process latest sales records
    df_latest = df.copy()
    df_latest['SALE_DATE'] = df_latest['SALE_DATE'].replace('', pd.NA)
    
    # Filter data
    df_latest = df_latest[
        df_latest['SALE_DATE'].notna() &
        df_latest['TOTAL_PROP_VALUE'].notna() &
        df_latest['name_2'].notna() &
        (df_latest['name_2'] != '') &
        (df_latest['name_2'].astype(str).str.endswith('NA') == False)  # Modified line
    ]
    
    # Process dates and keep only the latest records
    df_latest['SALE_DATE'] = pd.to_datetime(df_latest['SALE_DATE'])
    df_latest = (df_latest.sort_values('SALE_DATE')
                .groupby('REID')
                .last()
                .reset_index())
    
    # 3. Calculate yearly median prices and adjustment factors
    df_latest['year'] = df_latest['SALE_DATE'].dt.year
    yearly_median = df_latest.groupby('year')['PRICE'].median().reset_index(name='MED_PRICE_BY_YEAR')
    
    # Get 2024 median price and calculate adjustment factors
    max_year_med_price = yearly_median.loc[yearly_median['year'] == 2024, 'MED_PRICE_BY_YEAR'].iloc[0]
    yearly_median['MAX_YEAR_MED_PRICE'] = max_year_med_price
    yearly_median['adjustment_factor'] = 1 + (
        (yearly_median['MAX_YEAR_MED_PRICE'] - yearly_median['MED_PRICE_BY_YEAR']) / 
        yearly_median['MED_PRICE_BY_YEAR']
    )
    
    # 4. Calculate adjusted prices and ratios
    df_adjusted = df_latest.merge(yearly_median[['year', 'adjustment_factor']], on='year')
    df_adjusted['ADJ_PRICE'] = df_adjusted['PRICE'] * df_adjusted['adjustment_factor']
    df_adjusted['ADJ_SALES_RATIO'] = df_adjusted['TOTAL_PROP_VALUE'] / df_adjusted['ADJ_PRICE']
    
    # 5. Calculate unadjusted sales ratios
    df_display_ratios = df_latest.copy()
    df_display_ratios['SALES_RATIO'] = df_display_ratios['TOTAL_PROP_VALUE'] / df_display_ratios['PRICE']
    
    # 6. Calculate median adjusted sales ratio for each neighborhood
    neighborhood_medians = df_adjusted.groupby('name_2')['ADJ_SALES_RATIO'].median().reset_index()
    neighborhood_medians.columns = ['name_2', 'N_MED_ADJ_SALES_RATIO']
    
    # 7. Calculate absolute sales ratio difference for individual properties
    final_df = df_adjusted.merge(neighborhood_medians, on='name_2')
    final_df['N_ABS_ADJ_SALES_RATIO'] = (
        final_df['ADJ_SALES_RATIO'] - final_df['N_MED_ADJ_SALES_RATIO']
    )
    
    # 8. Prepare output data: REID and absolute sales ratio
    result_df = final_df[['REID', 'N_ABS_ADJ_SALES_RATIO']]
    
    # 9. Save results
    output_filename = f'property_abs_adjusted_sales_ratios.csv'
    result_df.to_csv(output_filename, index=False)
    
    print("\nData preview:")
    print(result_df.head())
    
    return result_df

if __name__ == "__main__":
    file_path = "Durham_BlockGroups_with_Sales_Merged.csv"
    result = process_sales_data(file_path)


# In[ ]:




