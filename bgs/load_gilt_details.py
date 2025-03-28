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
            if collecting_data:
                current_block.append(row[begin:end])
                indexer.append(row[0])
            else:
                if current_block == []:
                else:
                    match collecting_data:
                        case True:
                            pass
                        case False:
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

            match row[0]:
                case "Conventional stocks":
                    current_title = "Conventionals"

                case "Index linked stocks":
                    current_title = "Index-Linked"
                    index_linked = True

                case "Old-style":
                    collecting_data = True
                    linker_type = "Old-style"

                case "New-style":
                    collecting_data = True
                    linker_type = "New-style"


                case "Sequence":
                    end = row.index("END")
                    columns = row[begin:end]
                case "END":
                    collecting_data = False





    return dataframes
