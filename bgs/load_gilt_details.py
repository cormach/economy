import pandas as pd
import builtins
from collections import Counter
import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv_blocks(file_path, encoding="latin1"):
    dataframes = {}
    current_block = []
    current_title = None
    index_linked = False
    linker_type = None
    collecting_data = False
    columns = []

    with open(file_path, "r", encoding=encoding) as file:
        reader = csv.reader(file, quotechar='"', delimiter=",")
        begin = 0
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

            else:
                if current_block == []:
                    pass
                else:
                    match collecting_data:
                        case True:
                            pass
                        case False:
                            if linker_type:
                                dataframes[current_title + f" {linker_type}"] = (
                                    pd.DataFrame(
                                        current_block,
                                        columns=columns,
                                    )
                                )
                            else:
                                dataframes[current_title] = pd.DataFrame(
                                    current_block,
                                    columns=columns,
                                )
                            current_block = []

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
                
                case "Strips":
                    collecting_data = True
                    current_title="Strips"
                    index_linked = False
                    linker_type = None

                case "Sequence":
                    end = row.index("END")
                    columns = row[begin:end]
                    c = Counter(columns)

                    fill = {}
                    for col, count in c.items():
                        if count > 1:
                            fill[col] = iter(range(count))

                    non_duplicate_columns = []
                    for col in columns:
                        increment = None
                        if c[col] > 1:
                            increment = fill[col].__next__()
                        non_duplicate_columns.append(
                            f"{col} {increment + 1}" if increment is not None else col
                        )
                    columns = non_duplicate_columns

                case "END":
                    collecting_data = False
                    continue
    # incredibly the BGS has a data error on the id in the details
    dataframes["Conventionals"] = dataframes["Conventionals"].replace("32112", "32110")
    try:
        assert (dataframes["Conventionals"]["Sequence"].astype(float) < 50000).all()
        assert (
            dataframes["Index-Linked New-style"]["Sequence"].astype(float) < 60000
        ).all()
        assert (
            dataframes["Index-Linked Old-style"]["Sequence"].astype(float) < 55200
        ).all()
    except AssertionError:
        logger.error("Assertion failed")
        logger.error(
            f"Conventionals Shape Unchanged: {(dataframes['Conventionals']['Sequence'].astype(float) < 50000).all()}"
        )
        logger.error(
            f"Index-Linked New-style Shape Unchanged: {(dataframes['Index-Linked New-style']['Sequence'].astype(float) < 60000).all()}"
        )
        logger.error(
            f"Index-Linked Old-style Shape Unchanged: {(dataframes['Index-Linked Old-style']['Sequence'].astype(float) < 55200).all()}"
        )

    return dataframes
