import pandas as pd

def save_to_csv(data: pd.DataFrame, fileName: str):
    """Save DataFrame to a CSV file.

    :param data: DataFrame to be saved
    :param fileName: Name of the output CSV file
    """
    data.to_csv(fileName, index=False)
    print(f"Data saved to {fileName}")
