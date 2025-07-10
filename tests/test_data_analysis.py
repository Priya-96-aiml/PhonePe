import pytest
import pandas as pd
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_analysis import DataAnalyzer
from src.data_extraction import DataExtractor
from config.database_config import DatabaseConfig

class TestDataAnalyzer:
    """Test cases for DataAnalyzer class."""

    @pytest.fixture
    def analyzer_with_data(self):
        """Create analyzer with test data loaded into temp DB."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name

        temp_config = DatabaseConfig(temp_db)
        temp_config.execute_script('sql/schema.sql')

        extractor = DataExtractor()
        extractor.db_config = temp_config

        sample_data = extractor.generate_sample_data(
            num_customers=20, num_products=10, num_transactions=50
        )
        extractor.load_data_to_database(sample_data)

        analyzer = DataAnalyzer()
        analyzer.db_config = temp_config

        yield analyzer, temp_db

        if os.path.exists(temp_db):
            os.unlink(temp_db)

    def test_get_data_from_query(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        result = analyzer.get_data_from_query("SELECT COUNT(*) as count FROM customers")
        assert isinstance(result, pd.DataFrame)
        assert 'count' in result.columns
        assert result['count'].iloc[0] > 0

    def test_sales_performance_analysis(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        results = analyzer.sales_performance_analysis()
        assert 'total_metrics' in results
        assert results['total_metrics']['total_transactions'] > 0

    def test_customer_analysis(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        results = analyzer.customer_analysis()
        assert 'segment_analysis' in results
        assert isinstance(results['segment_analysis'], pd.DataFrame)

    def test_product_analysis(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        results = analyzer.product_analysis()
        assert 'top_products' in results

    def test_channel_analysis(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        results = analyzer.channel_analysis()
        assert 'channel_performance' in results

    def test_discount_analysis(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        results = analyzer.discount_analysis()
        assert 'discount_impact' in results

    def test_generate_insights(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        insights = analyzer.generate_insights()
        assert 'sales_insights' in insights
        assert len(insights['sales_insights']) > 0

    def test_create_visualizations(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        visualizations = analyzer.create_visualizations()
        assert isinstance(visualizations, dict)
        assert len(visualizations) > 0

    def test_query_error_handling(self, analyzer_with_data):
        analyzer, _ = analyzer_with_data
        with pytest.raises(Exception):
            analyzer.get_data_from_query("SELECT * FROM non_existent_table")

    def test_empty_data_handling(self):
        """Test handling of empty database with only schema, no data."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name

        try:
            temp_config = DatabaseConfig(temp_db)
            temp_config.execute_script('sql/schema_only.sql')  # 👈 schema-only version

            analyzer = DataAnalyzer()
            analyzer.db_config = temp_config

            result = analyzer.get_data_from_query("SELECT COUNT(*) as count FROM customers")
            assert isinstance(result, pd.DataFrame)
            assert result['count'].iloc[0] == 0

        finally:
            if os.path.exists(temp_db):
                os.remove(temp_db)

if __name__ == "__main__":
    pytest.main([__file__])
