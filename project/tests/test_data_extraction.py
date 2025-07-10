import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_extraction import DataExtractor

class TestDataExtractor:

    @pytest.fixture
    def extractor(self):
        return DataExtractor()

    def test_clean_data(self, extractor):
        """Test data cleaning functionality."""
        df = pd.DataFrame({
            'id': [1, 2, 2, 3, 4],
            'name': ['  John  ', 'Jane', 'Jane', '  Bob  ', 'Alice'],
            'value': [10.5, None, 20.0, 15.0, None],
            'category': ['A', 'B', 'B', 'C', 'A']
        })

        cleaned_df = extractor.clean_data(df)

        assert not cleaned_df.isnull().any().any(), "Null values still exist"
        assert cleaned_df.duplicated().sum() == 0, "Duplicates were not removed"
        assert all(cleaned_df['name'].str.startswith(' ') == False)
        assert all(cleaned_df['name'].str.endswith(' ') == False)