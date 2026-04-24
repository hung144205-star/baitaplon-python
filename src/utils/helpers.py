#!/usr/bin/env python3
"""
Helpers - General utility functions
"""
import os
import json
import uuid
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


def generate_code(prefix: str = "", length: int = 8, 
                  include_date: bool = True, separator: str = "") -> str:
    """
    Generate unique code
    
    Args:
        prefix: Code prefix (e.g., "KH", "HD")
        length: Length of random part
        include_date: Include current date in code
        separator: Separator between parts
    
    Returns:
        Generated code string
    """
    parts = []
    
    if prefix:
        parts.append(prefix.upper())
    
    if include_date:
        parts.append(datetime.now().strftime("%Y%m%d"))
    
    # Generate random part
    import random
    import string
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    parts.append(random_part)
    
    return separator.join(parts)


def generate_id() -> str:
    """
    Generate UUID
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def get_project_root() -> Path:
    """
    Get project root directory
    
    Returns:
        Path object
    """
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """
    Get data directory
    
    Returns:
        Path to data directory
    """
    return get_project_root() / 'data'


def get_backup_dir() -> Path:
    """
    Get backup directory
    
    Returns:
        Path to backup directory
    """
    return get_data_dir() / 'backups'


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if not
    
    Args:
        path: Directory path
    
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def backup_file(source_path: Union[str, Path], 
                backup_dir: Union[str, Path] = None,
                keep_days: int = 30) -> Path:
    """
    Backup file with timestamp
    
    Args:
        source_path: Source file path
        backup_dir: Backup directory (default: data/backups)
        keep_days: Days to keep backups
    
    Returns:
        Backup file path
    """
    source_path = Path(source_path)
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    # Get backup directory
    if backup_dir is None:
        backup_dir = get_backup_dir()
    else:
        backup_dir = Path(backup_dir)
    
    ensure_directory(backup_dir)
    
    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{source_path.stem}_{timestamp}{source_path.suffix}"
    backup_path = backup_dir / backup_filename
    
    # Copy file
    import shutil
    shutil.copy2(source_path, backup_path)
    
    # Clean old backups
    cleanup_old_backups(backup_dir, source_path.stem, keep_days)
    
    return backup_path


def cleanup_old_backups(backup_dir: Union[str, Path], 
                        prefix: str = None,
                        keep_days: int = 30):
    """
    Clean up old backup files
    
    Args:
        backup_dir: Backup directory
        prefix: File prefix to match
        keep_days: Days to keep
    """
    backup_dir = Path(backup_dir)
    
    if not backup_dir.exists():
        return
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    
    for file in backup_dir.glob(f"{prefix}*" if prefix else "*"):
        if file.is_file():
            file_time = datetime.fromtimestamp(file.stat().st_mtime)
            if file_time < cutoff_date:
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Error deleting {file}: {e}")


def load_json_file(file_path: Union[str, Path], 
                   default: Any = None) -> Any:
    """
    Load JSON file
    
    Args:
        file_path: File path
        default: Default value if file doesn't exist
    
    Returns:
        Parsed JSON data
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return default
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return default


def save_json_file(file_path: Union[str, Path], 
                   data: Any, 
                   indent: int = 2,
                   ensure_ascii: bool = False):
    """
    Save JSON file
    
    Args:
        file_path: File path
        data: Data to save
        indent: JSON indentation
        ensure_ascii: Whether to escape non-ASCII characters
    """
    file_path = Path(file_path)
    
    # Ensure directory exists
    ensure_directory(file_path.parent)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def calculate_age(birth_date: Union[date, datetime, str]) -> int:
    """
    Calculate age from birth date
    
    Args:
        birth_date: Birth date
    
    Returns:
        Age in years
    """
    # Convert string to date
    if isinstance(birth_date, str):
        birth_date = datetime.fromisoformat(birth_date).date()
    elif isinstance(birth_date, datetime):
        birth_date = birth_date.date()
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


def calculate_date_range(start_date: Union[date, str],
                         end_date: Union[date, str]) -> int:
    """
    Calculate days between two dates
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Number of days
    """
    # Convert strings to dates
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).date()
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).date()
    
    delta = end_date - start_date
    return delta.days


def get_quarter(date_value: Union[date, datetime] = None) -> int:
    """
    Get quarter from date
    
    Args:
        date_value: Date (default: today)
    
    Returns:
        Quarter number (1-4)
    """
    if date_value is None:
        date_value = date.today()
    elif isinstance(date_value, datetime):
        date_value = date_value.date()
    
    return (date_value.month - 1) // 3 + 1


def get_week_number(date_value: Union[date, datetime] = None) -> int:
    """
    Get ISO week number
    
    Args:
        date_value: Date (default: today)
    
    Returns:
        Week number
    """
    if date_value is None:
        date_value = date.today()
    elif isinstance(date_value, datetime):
        date_value = date_value.date()
    
    return date_value.isocalendar()[1]


def is_leap_year(year: int = None) -> bool:
    """
    Check if year is leap year
    
    Args:
        year: Year (default: current year)
    
    Returns:
        True if leap year
    """
    if year is None:
        year = datetime.now().year
    
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_days_in_month(month: int = None, year: int = None) -> int:
    """
    Get days in month
    
    Args:
        month: Month (1-12, default: current month)
        year: Year (default: current year)
    
    Returns:
        Number of days
    """
    from calendar import monthrange
    
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    return monthrange(year, month)[1]


def safe_divide(numerator: float, denominator: float, 
                default: float = 0.0) -> float:
    """
    Safe division with default value
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division fails
    
    Returns:
        Division result or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min and max
    
    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value
    
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def interpolate(value: float, in_min: float, in_max: float,
                out_min: float, out_max: float) -> float:
    """
    Map value from one range to another
    
    Args:
        value: Input value
        in_min: Input minimum
        in_max: Input maximum
        out_min: Output minimum
        out_max: Output maximum
    
    Returns:
        Mapped value
    """
    in_range = in_max - in_min
    out_range = out_max - out_min
    
    if in_range == 0:
        return out_min
    
    return out_min + (value - in_min) * out_range / in_range


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator
    
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def group_by(list_items: List[Dict], key: str) -> Dict[Any, List]:
    """
    Group list of dicts by key
    
    Args:
        list_items: List of dictionaries
        key: Key to group by
    
    Returns:
        Dictionary of grouped items
    """
    result = {}
    for item in list_items:
        group_key = item.get(key)
        if group_key not in result:
            result[group_key] = []
        result[group_key].append(item)
    return result


def sort_list(list_items: List[Dict], key: str, 
              reverse: bool = False) -> List[Dict]:
    """
    Sort list of dicts by key
    
    Args:
        list_items: List of dictionaries
        key: Key to sort by
        reverse: Sort in reverse order
    
    Returns:
        Sorted list
    """
    return sorted(list_items, key=lambda x: x.get(key, ''), reverse=reverse)


def search_list(list_items: List[Dict], search_text: str, 
                keys: List[str] = None) -> List[Dict]:
    """
    Search list of dicts
    
    Args:
        list_items: List of dictionaries
        search_text: Text to search
        keys: Keys to search in (None for all)
    
    Returns:
        Filtered list
    """
    if not search_text:
        return list_items
    
    search_text = search_text.lower().strip()
    result = []
    
    for item in list_items:
        if keys:
            # Search in specific keys
            for key in keys:
                value = str(item.get(key, '')).lower()
                if search_text in value:
                    result.append(item)
                    break
        else:
            # Search in all values
            for value in item.values():
                if search_text in str(value).lower():
                    result.append(item)
                    break
    
    return result


def paginate_list(list_items: List, page: int = 1, 
                  page_size: int = 20) -> Dict:
    """
    Paginate list
    
    Args:
        list_items: List to paginate
        page: Page number (1-indexed)
        page_size: Items per page
    
    Returns:
        Dict with items, page, page_size, total_pages, total_items
    """
    total_items = len(list_items)
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    
    # Ensure page is in valid range
    page = max(1, min(page, total_pages))
    
    # Get items for page
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    items = list_items[start_idx:end_idx]
    
    return {
        'items': items,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'total_items': total_items,
        'has_prev': page > 1,
        'has_next': page < total_pages,
    }


__all__ = [
    'generate_code',
    'generate_id',
    'get_project_root',
    'get_data_dir',
    'get_backup_dir',
    'ensure_directory',
    'backup_file',
    'cleanup_old_backups',
    'load_json_file',
    'save_json_file',
    'calculate_age',
    'calculate_date_range',
    'get_quarter',
    'get_week_number',
    'is_leap_year',
    'get_days_in_month',
    'safe_divide',
    'clamp',
    'interpolate',
    'deep_merge',
    'flatten_dict',
    'group_by',
    'sort_list',
    'search_list',
    'paginate_list',
]
