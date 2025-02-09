import unittest
import pandas as pd
from io import StringIO
from bgs import bgs_gilt_details

class TestCSVLoader(unittest.TestCase):

    def setUp(self):
        self.csv_data = """Worksheet name:,Index linked stocks
Sequence,Inst Code,Sedol,ISIN Code,%,Stock,Suffix,Special features,First year,Last year,Issue date,First coupon payable on date,Earliest redemption date,Latest redemption date,"A (B, C ...) stock merged on date",Actually redeemed or amalgamated,Frequency,Payment date 1,Payment date 2,Payment date 3,Payment date 4,First coupon,Last coupon,Col for I-L,Col for I-L,Col for I-L,Col for I-L,Col for I-L,Number of calls,Call payment 1,due on,Call payment 2,due on,Call payment 3,due on,Call payment 4,due on,END
Old-style,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
100,4HCV64,,,4.5,Conversion,,,,1964,15 Jan 1959,14 May 1959,,14 May 1964,,14 May 1964,2,14 May,14 Nov,,,1.470800,,,,,,,,,,,,,,,,END
New-style,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,END
200,2HEX6364,,,2.5,Exchequer,,,1963,1964,14 Nov 1954,,14 May 1963,14 May 1964,,14 May 1964,2,14 May,14 Nov,,,,,,,,,,,,,,,,,,,END
"""
        self.expected_df_old_style = pd.DataFrame({
            'Sequence': ['100'],
            'Inst Code': ['4HCV64'],
            'Sedol': [''],
            'ISIN Code': [''],
            '%': ['4.5'],
            'Stock': ['Conversion'],
            'Suffix': [''],
            'Special features': [''],
            'First year': ['1964'],
            'Last year': [''],
            'Issue date': ['15 Jan 1959'],
            'First coupon payable on date': ['14 May 1959'],
            'Earliest redemption date': [''],
            'Latest redemption date': ['14 May 1964'],
            'A (B, C ...) stock merged on date': [''],
            'Actually redeemed or amalgamated': ['14 May 1964'],
            'Frequency': ['2'],
            'Payment date 1': ['14 May'],
            'Payment date 2': ['14 Nov'],
            'Payment date 3': [''],
            'Payment date 4': [''],
            'First coupon': ['1.470800'],
            'Last coupon': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Number of calls': [''],
            'Call payment 1': [''],
            'due on': [''],
            'Call payment 2': [''],
            'due on': [''],
            'Call payment 3': [''],
            'due on': [''],
            'Call payment 4': [''],
            'due on': [''],
            'END': ['']
        })
        self.expected_df_old_style['Indexation Method'] = 'Eight month lag'

        self.expected_df_new_style = pd.DataFrame({
            'Sequence': ['200'],
            'Inst Code': ['2HEX6364'],
            'Sedol': [''],
            'ISIN Code': [''],
            '%': ['2.5'],
            'Stock': ['Exchequer'],
            'Suffix': [''],
            'Special features': [''],
            'First year': ['1963'],
            'Last year': ['1964'],
            'Issue date': ['14 Nov 1954'],
            'First coupon payable on date': [''],
            'Earliest redemption date': ['14 May 1963'],
            'Latest redemption date': ['14 May 1964'],
            'A (B, C ...) stock merged on date': [''],
            'Actually redeemed or amalgamated': ['14 May 1964'],
            'Frequency': ['2'],
            'Payment date 1': ['14 May'],
            'Payment date 2': ['14 Nov'],
            'Payment date 3': [''],
            'Payment date 4': [''],
            'First coupon': [''],
            'Last coupon': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Col for I-L': [''],
            'Number of calls': [''],
            'Call payment 1': [''],
            'due on': [''],
            'Call payment 2': [''],
            'due on': [''],
            'Call payment 3': [''],
            'due on': [''],
            'Call payment 4': [''],
            'due on': [''],
            'END': ['']
        })
        self.expected_df_new_style['Indexation Method'] = 'Three month lag'

    def test_load_csv_blocks(self):
        # Use StringIO to simulate a file object
        file_obj = StringIO(self.csv_data)
        dataframes = bgs_gilt_details.load_csv_blocks(file_obj)

        self.assertIn('Index linked stocks', dataframes)
        self.assertIsInstance(dataframes['Index linked stocks'], pd.DataFrame)

    def test_process_index_linked_stocks(self):
        # Use StringIO to simulate a file object
        file_obj = StringIO(self.csv_data)
        dataframes = bgs_gilt_details.load_csv_blocks(file_obj)
        index_linked_df = dataframes['Index linked stocks']
        processed_df = bgs_gilt_details.process_index_linked_stocks(index_linked_df)

        # Check if the 'Indexation Method' column is added correctly
        self.assertIn('Indexation Method', processed_df.columns)
        self.assertTrue((processed_df['Indexation Method'] == 'Eight month lag').any())
        self.assertTrue((processed_df['Indexation Method'] == 'Three month lag').any())

        # Check if the data is split and combined correctly
        pd.testing.assert_frame_equal(processed_df[processed_df['Indexation Method'] == 'Eight month lag'].reset_index(drop=True), self.expected_df_old_style)
        pd.testing.assert_frame_equal(processed_df[processed_df['Indexation Method'] == 'Three month lag'].reset_index(drop=True), self.expected_df_new_style)

if __name__ == '__main__':
    unittest.main()