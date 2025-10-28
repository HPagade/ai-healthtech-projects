"""
Helper functions for data handling and formatting
"""

import json
import pandas as pd
from pathlib import Path
from typing import Any, Optional
import streamlit as st


def load_data(file_path: str, file_type: str = 'csv') -> Optional[pd.DataFrame]:
    """
    Load data from file

    Args:
        file_path: Path to the data file
        file_type: Type of file ('csv', 'json', 'excel')

    Returns:
        DataFrame or None if file doesn't exist
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None

        if file_type == 'csv':
            return pd.read_csv(file_path)
        elif file_type == 'json':
            return pd.read_json(file_path)
        elif file_type == 'excel':
            return pd.read_excel(file_path)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def save_data(df: pd.DataFrame, file_path: str, file_type: str = 'csv') -> bool:
    """
    Save DataFrame to file

    Args:
        df: DataFrame to save
        file_path: Path to save the file
        file_type: Type of file ('csv', 'json', 'excel')

    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_type == 'csv':
            df.to_csv(file_path, index=False)
        elif file_type == 'json':
            df.to_json(file_path, orient='records', indent=2)
        elif file_type == 'excel':
            df.to_excel(file_path, index=False)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return False

        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False


def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency with symbol"""
    if currency == 'USD':
        if amount >= 1_000_000_000:
            return f"${amount / 1_000_000_000:.2f}B"
        elif amount >= 1_000_000:
            return f"${amount / 1_000_000:.2f}M"
        elif amount >= 1_000:
            return f"${amount / 1_000:.2f}K"
        else:
            return f"${amount:.2f}"
    return f"{amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage value"""
    return f"{value:.{decimals}f}%"


def format_number(value: float, decimals: int = 0) -> str:
    """Format large numbers with K, M, B suffixes"""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return f"{value:.{decimals}f}"


def check_api_key(key_name: str = 'OPENAI_API_KEY') -> Optional[str]:
    """
    Check for API key in Streamlit secrets or environment

    Args:
        key_name: Name of the API key

    Returns:
        API key string or None
    """
    # Check Streamlit secrets first
    if hasattr(st, 'secrets') and key_name in st.secrets:
        return st.secrets[key_name]

    # Check environment variables
    import os
    return os.environ.get(key_name)


def create_download_button(data: Any, filename: str, label: str = "Download", file_type: str = 'csv'):
    """
    Create a download button for data

    Args:
        data: Data to download (DataFrame, dict, or string)
        filename: Name of the file to download
        label: Button label
        file_type: Type of file ('csv', 'json', 'txt')
    """
    if isinstance(data, pd.DataFrame):
        if file_type == 'csv':
            csv = data.to_csv(index=False)
            st.download_button(
                label=label,
                data=csv,
                file_name=filename,
                mime='text/csv'
            )
        elif file_type == 'json':
            json_str = data.to_json(orient='records', indent=2)
            st.download_button(
                label=label,
                data=json_str,
                file_name=filename,
                mime='application/json'
            )
    elif isinstance(data, dict):
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label=label,
            data=json_str,
            file_name=filename,
            mime='application/json'
        )
    elif isinstance(data, str):
        st.download_button(
            label=label,
            data=data,
            file_name=filename,
            mime='text/plain'
        )


def validate_dataframe(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validate that DataFrame has required columns

    Args:
        df: DataFrame to validate
        required_columns: List of required column names

    Returns:
        True if valid, False otherwise
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return False
    return True


@st.cache_data(ttl=3600)
def cached_load_data(file_path: str, file_type: str = 'csv') -> Optional[pd.DataFrame]:
    """
    Cached version of load_data for better performance
    Cache expires after 1 hour (3600 seconds)
    """
    return load_data(file_path, file_type)
