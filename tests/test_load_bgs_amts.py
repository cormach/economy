from bgs.load_bgs_amounts import load_bgs_amounts
from unittest.mock import mock_open, patch
import pandas as pd
from io import StringIO
import random
from pandas.testing import assert_frame_equal
import pytest


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {"index": ["Jun 2024", "Jul 2024"], "Sum of Conventionals": ["3", "225"]},
        index=[0, 1],
    )


def test_load_bgs_amounts(mock_df):
    mock_csv_content = f"""Top,,,,,
    Next,Month end:,Jun 2024,Jul 2024,END,
    Sequence,,,,,
    3, txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    4, txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    5, txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    6,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    7,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    Sum of Conventionals,,"3","225",END,
    Index-linked,,,,END,
    Old-style,,,,END,
    10,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    11,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    12,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    13,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    14,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    New-style,,,,END,
    15,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    16,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    17,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    18,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    19,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    ,,Sum of index-linked,'1',END,
    Calculated indexed nominal,,,,END,
    ,,,,END,
    Old-style,,,,END,
    20,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    21,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    22,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    23,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    24,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    25,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    New-style,,,,END,
    27,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    28,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    29,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    30,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    31,txt, {','.join([str(random.randint(1,10)) for x in range(2)])},END,
    END,,Sum of index-linked, indexed,'2',END,
    ,,Sum of total conventional and indexed-linked,,210,
    END,END,END,END,END,"""

    with patch("builtins.open", mock_open(read_data=mock_csv_content)):
        result = load_bgs_amounts("dummy_path.csv")

    assert isinstance(result, dict)
    assert "Conventionals" in result
    assert "Index-linked Old-style" in result
    assert "Index-linked New-style" in result
    assert "Calculated indexed nominal Old-style" in result
    assert "Calculated indexed nominal New-style" in result
    assert "Sum of Conventionals" in result
    assert "Sum of total conventional and indexed-linked" in result
    assert type(result["Sum of Conventionals"]) == pd.DataFrame

    assert_frame_equal(result["Sum of Conventionals"], mock_df, check_like=True)
