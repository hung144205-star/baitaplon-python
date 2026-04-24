#!/usr/bin/env python3
"""
Formatters - Format functions cho dữ liệu hiển thị
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Union, Optional


def format_currency(value: Union[int, float, Decimal], currency: str = "₫", 
                    show_symbol: bool = True, locale: str = "vi_VN") -> str:
    """
    Format currency value
    
    Args:
        value: Numeric value
        currency: Currency symbol (default: ₫)
        show_symbol: Whether to show currency symbol
        locale: Locale for formatting (vi_VN or en_US)
    
    Returns:
        Formatted currency string
    """
    if value is None:
        return "0" + (f" {currency}" if show_symbol else "")
    
    try:
        num_value = float(value)
    except (TypeError, ValueError):
        return str(value)
    
    if locale == "vi_VN":
        # Vietnamese format: 1.234.567,89 ₫
        formatted = f"{num_value:,.0f}".replace(',', '.')
    else:
        # US format: $1,234,567.89
        formatted = f"{num_value:,.2f}"
    
    if show_symbol:
        if locale == "vi_VN":
            return f"{formatted} {currency}"
        else:
            return f"{currency}{formatted}"
    
    return formatted


def format_number(value: Union[int, float], decimals: int = 0, 
                  thousands_separator: bool = True) -> str:
    """
    Format number with thousands separator
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        thousands_separator: Whether to use thousands separator
    
    Returns:
        Formatted number string
    """
    if value is None:
        return "0"
    
    try:
        num_value = float(value)
    except (TypeError, ValueError):
        return str(value)
    
    if decimals == 0:
        if thousands_separator:
            return f"{num_value:,.0f}".replace(',', '.')
        return f"{num_value:.0f}"
    else:
        if thousands_separator:
            return f"{num_value:,.{decimals}f}".replace(',', '.')
        return f"{num_value:.{decimals}f}"


def format_percentage(value: Union[int, float], decimals: int = 1) -> str:
    """
    Format percentage value
    
    Args:
        value: Percentage value (0-100)
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    if value is None:
        return "0%"
    
    try:
        num_value = float(value)
    except (TypeError, ValueError):
        return str(value)
    
    return f"{num_value:.{decimals}f}%"


def format_date(date_value: Union[date, datetime, str], 
                format_string: str = "dd/MM/yyyy") -> str:
    """
    Format date value
    
    Args:
        date_value: Date object or string
        format_string: Format pattern (dd/MM/yyyy, MM/dd/yyyy, yyyy-MM-dd)
    
    Returns:
        Formatted date string
    """
    if date_value is None:
        return ""
    
    # Convert to datetime if string
    if isinstance(date_value, str):
        try:
            date_value = datetime.fromisoformat(date_value).date()
        except ValueError:
            return date_value
    
    # Convert QDate to date
    if hasattr(date_value, 'toPyDate'):
        date_value = date_value.toPyDate()
    
    # Format based on pattern
    if format_string == "dd/MM/yyyy":
        return date_value.strftime("%d/%m/%Y")
    elif format_string == "MM/dd/yyyy":
        return date_value.strftime("%m/%d/%Y")
    elif format_string == "yyyy-MM-dd":
        return date_value.strftime("%Y-%m-%d")
    elif format_string == "dd/MM/yyyy HH:mm":
        if isinstance(date_value, datetime):
            return date_value.strftime("%d/%m/%Y %H:%M")
        return date_value.strftime("%d/%m/%Y")
    elif format_string == "dd/MM":
        return date_value.strftime("%d/%m")
    elif format_string == "MM/yyyy":
        return date_value.strftime("%m/%Y")
    elif format_string == "yyyy":
        return date_value.strftime("%Y")
    elif format_string == "dd MMM yyyy":
        return date_value.strftime("%d %b %Y")
    else:
        return date_value.strftime(format_string)


def format_datetime(datetime_value: Union[datetime, str],
                    format_string: str = "dd/MM/yyyy HH:mm") -> str:
    """
    Format datetime value
    
    Args:
        datetime_value: Datetime object or string
        format_string: Format pattern
    
    Returns:
        Formatted datetime string
    """
    if datetime_value is None:
        return ""
    
    # Convert to datetime if string
    if isinstance(datetime_value, str):
        try:
            datetime_value = datetime.fromisoformat(datetime_value)
        except ValueError:
            return datetime_value
    
    # Convert QDateTime to datetime
    if hasattr(datetime_value, 'toPyDateTime'):
        datetime_value = datetime_value.toPyDateTime()
    
    return format_date(datetime_value, format_string)


def format_time(time_value: str = "HH:mm") -> str:
    """
    Format time value
    
    Args:
        time_value: Time object or string
    
    Returns:
        Formatted time string
    """
    if time_value is None:
        return ""
    
    if isinstance(time_value, str):
        return time_value
    
    if hasattr(time_value, 'toString'):
        # QTime
        return time_value.toString("HH:mm")
    
    if isinstance(time_value, datetime):
        return time_value.strftime("%H:%M")
    
    return str(time_value)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human readable
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string (KB, MB, GB)
    """
    if size_bytes is None:
        return "0 B"
    
    try:
        size = int(size_bytes)
    except (TypeError, ValueError):
        return str(size_bytes)
    
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.1f} GB"


def format_phone(phone: str, country_code: str = "VN") -> str:
    """
    Format phone number
    
    Args:
        phone: Phone number string
        country_code: Country code (VN, US)
    
    Returns:
        Formatted phone string
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    if country_code == "VN":
        # Vietnamese format: 0901 234 567
        if clean_phone.startswith('84') and len(clean_phone) == 12:
            # +84 format
            clean_phone = clean_phone[2:]  # Remove 84
        
        if len(clean_phone) == 10:
            return f"0{clean_phone[1:4]} {clean_phone[4:7]} {clean_phone[7:]}"
        elif len(clean_phone) == 11:
            return f"0{clean_phone[1:5]} {clean_phone[5:8]} {clean_phone[8:]}"
    
    # Default format: group by 3s
    groups = []
    while len(clean_phone) > 3:
        groups.append(clean_phone[:3])
        clean_phone = clean_phone[3:]
    if clean_phone:
        groups.append(clean_phone)
    
    return ' '.join(groups)


def format_address(street: str = None, ward: str = None, 
                   district: str = None, city: str = None) -> str:
    """
    Format address components
    
    Args:
        street: Street address
        ward: Ward/Commune
        district: District
        city: City/Province
    
    Returns:
        Formatted address string
    """
    parts = []
    
    if street:
        parts.append(street.strip())
    if ward:
        parts.append(ward.strip())
    if district:
        parts.append(district.strip())
    if city:
        parts.append(city.strip())
    
    return ', '.join(parts) if parts else ""


def format_name(first_name: str = None, last_name: str = None,
                middle_name: str = None, display_order: str = "last_first") -> str:
    """
    Format full name
    
    Args:
        first_name: First name
        last_name: Last name
        middle_name: Middle name
        display_order: "last_first" or "first_last"
    
    Returns:
        Formatted full name
    """
    if display_order == "last_first":
        # Vietnamese order: Last Middle First
        parts = filter(None, [last_name, middle_name, first_name])
    else:
        # Western order: First Middle Last
        parts = filter(None, [first_name, middle_name, last_name])
    
    return ' '.join(parts)


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human readable
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    if seconds is None or seconds < 0:
        return "0s"
    
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}p {secs}s" if secs else f"{minutes}p"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}p" if minutes else f"{hours}h"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}n {hours}h" if hours else f"{days}n"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to max length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def capitalize_words(text: str) -> str:
    """
    Capitalize first letter of each word
    
    Args:
        text: Text to capitalize
    
    Returns:
        Capitalized text
    """
    if not text:
        return ""
    
    return ' '.join(word.capitalize() for word in text.split())


def slugify(text: str) -> str:
    """
    Convert text to slug
    
    Args:
        text: Text to slugify
    
    Returns:
        Slug string
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower().strip()
    
    # Replace spaces with hyphens
    text = text.replace(' ', '-')
    
    # Remove special characters
    import re
    text = re.sub(r'[^\w\s-]', '', text)
    
    # Remove multiple hyphens
    text = re.sub(r'-+', '-', text)
    
    return text


__all__ = [
    'format_currency',
    'format_number',
    'format_percentage',
    'format_date',
    'format_datetime',
    'format_time',
    'format_file_size',
    'format_phone',
    'format_address',
    'format_name',
    'format_duration',
    'truncate_text',
    'capitalize_words',
    'slugify',
]
