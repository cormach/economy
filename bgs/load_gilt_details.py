import pandas as pd

import csv

def load_csv_blocks(file_obj):
    dataframes = {}
    current_block = []
    current_title = None
    collecting_data = False

    reader = csv.reader(file_obj)
    for row in reader:
        if "Worksheet name:" in row[0]:
            if current_block and current_title:
                # Save the previous block
                df = pd.DataFrame(current_block[1:], columns=current_block[0])
                dataframes[current_title] = df
                current_block = []
                collecting_data = False
            
            # Get the title from the same row
            current_title = row[1]
        elif "Sequence" in row[0]:
            # Start collecting data
            collecting_data = True
            current_block.append(row)
        elif collecting_data:
            if not any(row):
                # End of current block
                collecting_data = False
            else:
                current_block.append(row)

    # Save the last block
    if current_block and current_title:
        df = pd.DataFrame(current_block[1:], columns=current_block[0])
        dataframes[current_title] = df

    return dataframes

def process_index_linked_stocks(df):
    old_style_index = df[df.iloc[:, 0] == 'Old-style'].index[0]
    new_style_index = df[df.iloc[:, 0] == 'New-style'].index[0]

    old_style_df = df.iloc[old_style_index + 1:new_style_index].copy()
    new_style_df = df.iloc[new_style_index + 1:].copy()

    old_style_df['Indexation Method'] = 'Eight month lag'
    new_style_df['Indexation Method'] = 'Three month lag'

    # Ensure all columns are included in the combined DataFrame
    combined_df = pd.concat([old_style_df, new_style_df], ignore_index=True)
    
    return combined_df