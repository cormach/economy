import pandas as pd
import builtins

import csv


def load_csv_blocks(file_path, encoding="latin1"):
    dataframes = {}
    current_block = []
    current_title = None
    indexer = []
    index_linked = False
    linker_type = None
    collecting_data = False

    with open(file_path, "r", encoding=encoding) as file:
        reader = csv.reader(file, quotechar='"', delimiter=",")
        begin = 1
        for i, row in enumerate(reader):

            if row[0] is None:
                collecting_data = False
            try:
                int(row[0])
                collecting_data = True
            except:
                collecting_data = False
            print(f"count={i}, row={row[0]}, collecting={collecting_data}, il={index_linked}, new/old={linker_type}")
            if collecting_data:
                print('collecting data')
                current_block.append(row[begin:end])
                indexer.append(row[0])
                print(current_block)
            else:
                if current_block == []:
                    print('empty block')
                else:
                    match collecting_data:
                        case True:
                            pass
                        case False:

                            print('block', current_block)
                            if linker_type:
                                dataframes[current_title + f" {linker_type}"] = pd.DataFrame(
                                    current_block, columns=columns, index=indexer
                                )
                            else:
                                dataframes[current_title] = pd.DataFrame(
                                    current_block, columns=columns, index=indexer
                            )
                            current_block = []
                            indexer = []
            print(len(dataframes))
            print(dataframes.keys())


            match row[0]:
                case "Conventional stocks":
                    current_title = "Conventionals"

                case "Index linked stocks":
                    current_title = "Index-Linked"
                    index_linked = True

                case "Old-style":
                    print('old style')
                    collecting_data = True
                    linker_type = "Old-style"

                case "New-style":
                    print('new-style')
                    collecting_data = True
                    linker_type = "New-style"


                case "Sequence":
                    end = row.index("END")
                    columns = row[begin:end]
                case "END":
                    collecting_data = False





    return dataframes


def process_index_linked_stocks(df):
    old_style_index = df[df.iloc[:, 0] == "Old-style"].index[0]
    new_style_index = df[df.iloc[:, 0] == "New-style"].index[0]

    old_style_df = df.iloc[old_style_index + 1 : new_style_index].copy()
    new_style_df = df.iloc[new_style_index + 1 :].copy()

    old_style_df["Indexation Method"] = "Eight month lag"
    new_style_df["Indexation Method"] = "Three month lag"

    # Ensure all columns are included in the combined DataFrame
    combined_df = pd.concat([old_style_df, new_style_df], ignore_index=True)

    return combined_df
