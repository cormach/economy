import pandas as pd
import csv

def load_bgs_amounts(file_path, encoding='latin1'):
    dataframes = {}
    current_block = []
    current_title = None
    indexer = []
    index_linked = False
    linker_type=None
    collecting_data=False

    with open(file_path, 'r', encoding=encoding) as file:
        reader = csv.reader(file)
        
        for i, row in enumerate(reader):
            if i==1:
                begin = row.index("Month end:")+1
                end = row.index("END")
                columns = row[begin:end]
            if "Sequence" in row[0]:
                current_title="Conventionals"
                current_block = []
                indexer = []
                collecting_data=True
                continue
            if "Index-linked" in row[0]:
                current_title="Index-linked"
                index_linked=True
                continue
            if "Calculated indexed nominal" in row[0]:
                current_title="Calculated indexed nominal"
                index_linked=True
                continue
            if "Old-style" in row[0]:
                linker_type="Old-style"
                collecting_data=True
                current_block = []
                indexer = []
                continue


            if row[0] is None:
                collecting_data=False
            try:
                int(row[0])
                collecting_data=True
            except:
                collecting_data=False

            if collecting_data:
                current_block.append(row[begin:end])
                indexer.append(row[0])
            else:
                if current_block==[]:
                    pass
                else:
                    print(current_title, len(current_block))
                    if linker_type:
                        dataframes[current_title+f" {linker_type}"] = pd.DataFrame(current_block, columns=columns, index=indexer)
                    else:
                        dataframes[current_title] = pd.DataFrame(current_block, columns=columns, index=indexer)
                    current_block = []

            if "New-style" in row[0]:
                linker_type="New-style"
                collecting_data=True
                current_block = []
                indexer = []
                continue            

            if "Sum of Conventionals" in row[0]:

                dataframes["Sum of Conventionals"] = pd.DataFrame(dict(zip(row[begin:end],columns)), index=[0])
                collecting_data=False
            if "Sum of total conventional and indexed-linked" in row[2]:

                dataframes["Sum of total conventional and indexed-linked"] = pd.DataFrame( dict(zip(row[begin:end],columns)), index=[0])
                collecting_data=False           
    return dataframes


if __name__=="__main__":
    file_path = '/workspaces/economy/downloads/BGSAmounts.csv'
    dataframes = load_bgs_amounts(file_path)
