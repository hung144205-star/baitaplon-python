#!/usr/bin/env python3
"""
Validators - Validation functions cho dữ liệu
"""
import re
from typing import Tuple, Optional


class ValidationResult:
    """Kết quả validation"""
    def __init__(self, is_valid: bool, message: str = ""):
        self.is_valid = is_valid
        self.message = message
    
    def __bool__(self):
        return self.is_valid


def validate_email(email: str) -> ValidationResult:
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        ValidationResult with is_valid and message
    """
    if not email or not email.strip():
        return ValidationResult(False, "Email không được để trống")
    
    email = email.strip()
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return ValidationResult(False, "Email không đúng định dạng")
    
    if len(email) > 254:
        return ValidationResult(False, "Email quá dài (tối đa 254 ký tự)")
    
    return ValidationResult(True, "")


def validate_phone(phone: str) -> ValidationResult:
    """
    Validate Vietnamese phone number
    
    Args:
        phone: Phone number string
    
    Returns:
        ValidationResult
    """
    if not phone or not phone.strip():
        return ValidationResult(False, "Số điện thoại không được để trống")
    
    phone = phone.strip().replace(' ', '').replace('-', '').replace('.', '')
    
    # Vietnamese phone patterns
    patterns = [
        r'^0\d{9,10}$',  # 0xxxxxxxxx or 0xxxxxxxxxx
        r'^84\d{9,10}$',  # 84xxxxxxxxx
        r'^\+84\d{9,10}$',  # +84xxxxxxxxx
    ]
    
    for pattern in patterns:
        if re.match(pattern, phone):
            return ValidationResult(True, "")
    
    return ValidationResult(False, "Số điện thoại không đúng định dạng (ví dụ: 0901234567)")


def validate_required(value, field_name: str = "Trường này") -> ValidationResult:
    """
    Validate required field
    
    Args:
        value: Value to check
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    if value is None:
        return ValidationResult(False, f"{field_name} không được để trống")
    
    if isinstance(value, str) and not value.strip():
        return ValidationResult(False, f"{field_name} không được để trống")
    
    if isinstance(value, (list, dict)) and len(value) == 0:
        return ValidationResult(False, f"{field_name} không được để trống")
    
    return ValidationResult(True, "")


def validate_length(value: str, min_len: int = 0, max_len: int = None, 
                    field_name: str = "Trường này") -> ValidationResult:
    """
    Validate string length
    
    Args:
        value: String to validate
        min_len: Minimum length
        max_len: Maximum length
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    if not isinstance(value, str):
        return ValidationResult(True, "")  # Skip if not string
    
    if len(value) < min_len:
        return ValidationResult(False, f"{field_name} phải có ít nhất {min_len} ký tự")
    
    if max_len and len(value) > max_len:
        return ValidationResult(False, f"{field_name} không được vượt quá {max_len} ký tự")
    
    return ValidationResult(True, "")


def validate_number(value, min_value: float = None, max_value: float = None,
                    field_name: str = "Trường này") -> ValidationResult:
    """
    Validate number range
    
    Args:
        value: Number to validate
        min_value: Minimum value
        max_value: Maximum value
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    try:
        num_value = float(value)
    except (TypeError, ValueError):
        return ValidationResult(False, f"{field_name} phải là số")
    
    if min_value is not None and num_value < min_value:
        return ValidationResult(False, f"{field_name} phải lớn hơn hoặc bằng {min_value}")
    
    if max_value is not None and num_value > max_value:
        return ValidationResult(False, f"{field_name} phải nhỏ hơn hoặc bằng {max_value}")
    
    return ValidationResult(True, "")


def validate_date(date_value, field_name: str = "Ngày") -> ValidationResult:
    """
    Validate date
    
    Args:
        date_value: Date to validate
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    from PyQt6.QtCore import QDate
    
    if date_value is None:
        return ValidationResult(False, f"{field_name} không được để trống")
    
    if isinstance(date_value, QDate):
        if not date_value.isValid():
            return ValidationResult(False, f"{field_name} không hợp lệ")
        return ValidationResult(True, "")
    
    return ValidationResult(False, f"{field_name} không đúng định dạng ngày")


def validate_date_range(start_date, end_date, 
                        field_name: str = "Khoảng ngày") -> ValidationResult:
    """
    Validate date range (start < end)
    
    Args:
        start_date: Start date
        end_date: End date
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    if start_date is None or end_date is None:
        return ValidationResult(True, "")  # Skip if either is None
    
    from PyQt6.QtCore import QDate
    
    if isinstance(start_date, QDate) and isinstance(end_date, QDate):
        if start_date > end_date:
            return ValidationResult(False, f"Ngày bắt đầu phải trước ngày kết thúc")
    
    return ValidationResult(True, "")


def validate_currency(value, field_name: str = "Số tiền") -> ValidationResult:
    """
    Validate currency value (positive number)
    
    Args:
        value: Value to validate
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    result = validate_number(value, min_value=0, field_name=field_name)
    if not result:
        return result
    
    # Check decimal places (max 2)
    try:
        str_value = str(float(value))
        if '.' in str_value:
            decimals = len(str_value.split('.')[1])
            if decimals > 2:
                return ValidationResult(False, f"{field_name} không được vượt quá 2 chữ số thập phân")
    except:
        pass
    
    return ValidationResult(True, "")


def validate_unique(value, existing_values: list, 
                    field_name: str = "Giá trị") -> ValidationResult:
    """
    Validate value is unique in list
    
    Args:
        value: Value to check
        existing_values: List of existing values
        field_name: Field name for error message
    
    Returns:
        ValidationResult
    """
    if value in existing_values:
        return ValidationResult(False, f"{field_name} đã tồn tại")
    
    return ValidationResult(True, "")


def validate_password(password: str, min_length: int = 6) -> ValidationResult:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        min_length: Minimum password length
    
    Returns:
        ValidationResult
    """
    if not password:
        return ValidationResult(False, "Mật khẩu không được để trống")
    
    if len(password) < min_length:
        return ValidationResult(False, f"Mật khẩu phải có ít nhất {min_length} ký tự")
    
    # Check for at least one letter
    if not any(c.isalpha() for c in password):
        return ValidationResult(False, "Mật khẩu phải chứa ít nhất một chữ cái")
    
    # Check for at least one number
    if not any(c.isdigit() for c in password):
        return ValidationResult(False, "Mật khẩu phải chứa ít nhất một số")
    
    return ValidationResult(True, "")


def validate_form(data: dict, validators: dict) -> Tuple[bool, dict]:
    """
    Validate form data with multiple validators
    
    Args:
        data: Form data dict
        validators: Dict of {field_name: validator_function}
    
    Returns:
        Tuple (is_valid, errors_dict)
    """
    errors = {}
    
    for field_name, validator in validators.items():
        value = data.get(field_name)
        result = validator(value)
        
        if not result:
            errors[field_name] = result.message
    
    return len(errors) == 0, errors


__all__ = [
    'ValidationResult',
    'validate_email',
    'validate_phone',
    'validate_required',
    'validate_length',
    'validate_number',
    'validate_date',
    'validate_date_range',
    'validate_currency',
    'validate_unique',
    'validate_password',
    'validate_form',
]
