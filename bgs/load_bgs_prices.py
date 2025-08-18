import csv
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_prices(file_path):
    with open(file_path, "r", encoding="latin1") as file:
        reader = csv.reader(file)
        block = []
        index = []
        for i, row in enumerate(reader):
            if row[0] == "END":
                break
            if i == 1:
                begin = row.index("Quote date") + 1
                end = row.index("END")
                columns = row[begin:end]
            if i > 4:
                block.append(row[begin:end])
                index.append(int(row[0]))

    data = pd.DataFrame(block, columns=columns, index=index)
    data = data.map(convert_to_float)
    columns = [col for col in columns if col != ""]
    # logger.info(columns)

    return data[columns].T


def convert_to_float(x):
    if x:
        try:
            if x in ["missing", "Amalgamated", "Redeemed", "redeemed"]:
                return x
            else:
                return float(x)
        except:
            split_ = [n for n in x.split(" ") if n != ""]
            whole = split_[0]
            fraction = split_[1] if len(split_) > 1 else None
            if fraction:
                _ator = fraction.split("/")
                return float(whole) + float(_ator[0]) / float(_ator[1])
            else:
                return float(whole)
    else:
        return 0


data = load_prices("downloads/BGSPrices.csv")
