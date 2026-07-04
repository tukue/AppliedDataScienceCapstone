"""Data loading and collection utilities."""

import requests
import pandas as pd
from src.logger import setup_logger
from src.config import SPACEX_API_URL, RAW_DATA_DIR

logger = setup_logger(__name__)


def fetch_spacex_launches(endpoint: str = "/launches") -> pd.DataFrame:
    """
    Fetch SpaceX launch data from official API.

    Args:
        endpoint: API endpoint to fetch from

    Returns:
        DataFrame with launch data
    """
    try:
        url = f"{SPACEX_API_URL}{endpoint}"
        logger.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)
        logger.info(f"Successfully fetched {len(df)} records")
        return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise


def fetch_spacex_rockets(endpoint: str = "/rockets") -> pd.DataFrame:
    """
    Fetch SpaceX rocket information.

    Args:
        endpoint: API endpoint to fetch from

    Returns:
        DataFrame with rocket data
    """
    return fetch_spacex_launches(endpoint)


def fetch_spacex_cores(endpoint: str = "/cores") -> pd.DataFrame:
    """
    Fetch SpaceX core/booster information.

    Args:
        endpoint: API endpoint to fetch from

    Returns:
        DataFrame with core data
    """
    return fetch_spacex_launches(endpoint)


def save_raw_data(df: pd.DataFrame, filename: str) -> None:
    """
    Save raw data to CSV file.

    Args:
        df: DataFrame to save
        filename: Output filename
    """
    output_path = RAW_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    logger.info(f"Data saved to {output_path}")


def load_raw_data(filename: str) -> pd.DataFrame:
    """
    Load raw data from CSV file.

    Args:
        filename: Input filename

    Returns:
        Loaded DataFrame
    """
    input_path = RAW_DATA_DIR / filename
    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} records from {input_path}")
    return df
