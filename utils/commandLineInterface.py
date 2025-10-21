import argparse


class CommandLineInterface:
    """Handles command line argument parsing for the stock data application."""
    
    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments and return the parsed namespace."""
        parser = argparse.ArgumentParser(description="Fetch Taiwan Stock Deal Info")
        parser.add_argument("stock_id", type=str, help="Stock ID (e.g 0050)")
        parser.add_argument("start_date", type=str, help="Start date (e.g 2021-09-13)")
        parser.add_argument("end_date", type=str, nargs="?", default=None, help="End date (YYYY-MM-DD, optional)")
        parser.add_argument("--output", type=str, default="stock_data.csv", help="Output CSV file name")
        return parser.parse_args()