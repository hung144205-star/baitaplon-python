"""
Test suite cho Formatters
"""
import pytest
from datetime import date, datetime
from decimal import Decimal

from src.utils.formatters import (
    format_currency,
    format_number,
    format_percentage,
    format_date,
    format_datetime,
    format_file_size,
    format_phone,
    format_address,
    format_name,
    format_duration,
    truncate_text,
    capitalize_words,
    slugify,
)


class TestFormatCurrency:
    """Test format_currency()"""
    
    def test_format_vnd(self):
        """Test VND formatting"""
        result = format_currency(1234567, currency="₫")
        assert "1.234.567" in result or "1234567" in result
        assert "₫" in result
    
    def test_format_with_symbol(self):
        """Test with currency symbol"""
        result = format_currency(1000000, currency="₫", show_symbol=True)
        assert "1.000.000" in result
        assert "₫" in result
    
    def test_format_without_symbol(self):
        """Test without currency symbol"""
        result = format_currency(1000000, show_symbol=False)
        assert "1.000.000" in result
        assert "₫" not in result
    
    def test_format_zero(self):
        """Test zero value"""
        result = format_currency(0)
        assert "0" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_currency(None)
        assert "0" in result
    
    def test_format_negative(self):
        """Test negative value"""
        result = format_currency(-500000)
        assert "-" in result
    
    def test_format_float(self):
        """Test float value"""
        result = format_currency(1234.56)
        assert "1.234" in result.replace(",", ".")
    
    def test_format_decimal(self):
        """Test Decimal value"""
        result = format_currency(Decimal("1234567.89"))
        assert "1.234.567" in result
    
    def test_format_us_locale(self):
        """Test US locale formatting"""
        result = format_currency(1234567.89, locale="en_US", currency="$")
        assert "1,234,567.89" in result
        assert "$" in result


class TestFormatNumber:
    """Test format_number()"""
    
    def test_format_integer(self):
        """Test integer formatting"""
        result = format_number(1234567)
        assert "1.234.567" in result
    
    def test_format_with_decimals(self):
        """Test formatting with decimals"""
        result = format_number(1234.56, decimals=2)
        assert "1.234,56" in result
    
    def test_format_zero_decimals(self):
        """Test zero decimals"""
        result = format_number(1234.56, decimals=0)
        assert "1.234" in result
    
    def test_format_no_separator(self):
        """Test without thousands separator"""
        result = format_number(1234567, thousands_separator=False)
        assert "1234567" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_number(None)
        assert "0" in result


class TestFormatPercentage:
    """Test format_percentage()"""
    
    def test_format_basic(self):
        """Test basic percentage"""
        result = format_percentage(75.5)
        assert "75.5%" in result
    
    def test_format_zero_decimals(self):
        """Test zero decimals"""
        result = format_percentage(75.567, decimals=0)
        assert "76%" in result
    
    def test_format_two_decimals(self):
        """Test two decimals"""
        result = format_percentage(75.567, decimals=2)
        assert "75.57%" in result
    
    def test_format_zero(self):
        """Test zero value"""
        result = format_percentage(0)
        assert "0%" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_percentage(None)
        assert "0%" in result
    
    def test_format_100(self):
        """Test 100%"""
        result = format_percentage(100)
        assert "100.0%" in result


class TestFormatDate:
    """Test format_date()"""
    
    def test_format_dd_mm_yyyy(self):
        """Test DD/MM/YYYY format"""
        d = date(2024, 4, 15)
        result = format_date(d, format_string="dd/MM/yyyy")
        assert "15/04/2024" in result
    
    def test_format_yyyy_mm_dd(self):
        """Test YYYY-MM-DD format"""
        d = date(2024, 4, 15)
        result = format_date(d, format_string="yyyy-MM-dd")
        assert "2024-04-15" in result
    
    def test_format_mm_dd_yyyy(self):
        """Test MM/DD/YYYY format"""
        d = date(2024, 4, 15)
        result = format_date(d, format_string="MM/dd/yyyy")
        assert "04/15/2024" in result
    
    def test_format_datetime(self):
        """Test datetime object"""
        dt = datetime(2024, 4, 15, 14, 30)
        result = format_date(dt, format_string="dd/MM/yyyy")
        assert "15/04/2024" in result
    
    def test_format_string_date(self):
        """Test string date input"""
        result = format_date("2024-04-15")
        assert "15/04/2024" in result
    
    def test_format_iso_string(self):
        """Test ISO format string"""
        result = format_date("2024-04-15T14:30:00", format_string="dd/MM/yyyy")
        assert "15/04/2024" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_date(None)
        assert "" in result
    
    def test_format_dd_mm(self):
        """Test DD/MM format"""
        d = date(2024, 4, 15)
        result = format_date(d, format_string="dd/MM")
        assert "15/04" in result
    
    def test_format_yyyy(self):
        """Test YYYY format"""
        d = date(2024, 4, 15)
        result = format_date(d, format_string="yyyy")
        assert "2024" in result


class TestFormatDatetime:
    """Test format_datetime()"""
    
    def test_format_basic(self):
        """Test basic datetime formatting"""
        dt = datetime(2024, 4, 15, 14, 30)
        result = format_datetime(dt)
        assert "15/04/2024" in result
        assert "14:30" in result
    
    def test_format_string(self):
        """Test string datetime input"""
        result = format_datetime("2024-04-15T14:30:00")
        assert "15/04/2024" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_datetime(None)
        assert "" in result


class TestFormatFileSize:
    """Test format_file_size()"""
    
    def test_format_bytes(self):
        """Test bytes"""
        result = format_file_size(500)
        assert "500 B" in result
    
    def test_format_kilobytes(self):
        """Test kilobytes"""
        result = format_file_size(1024)
        assert "1.0 KB" in result
    
    def test_format_megabytes(self):
        """Test megabytes"""
        result = format_file_size(1024 * 1024)
        assert "1.0 MB" in result
    
    def test_format_gigabytes(self):
        """Test gigabytes"""
        result = format_file_size(1024 * 1024 * 1024)
        assert "1.0 GB" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_file_size(None)
        assert "0" in result


class TestFormatPhone:
    """Test format_phone()"""
    
    def test_format_10_digit(self):
        """Test 10-digit Vietnamese phone"""
        result = format_phone("0901234567")
        assert "0901" in result
        assert "234" in result
        assert "567" in result
    
    def test_format_11_digit(self):
        """Test 11-digit Vietnamese phone"""
        result = format_phone("09012345678")
        assert "0901" in result
    
    def test_format_with_84(self):
        """Test phone with +84"""
        result = format_phone("84901234567")
        assert "090" in result
    
    def test_format_empty(self):
        """Test empty phone"""
        result = format_phone("")
        assert "" in result
    
    def test_format_none(self):
        """Test None phone"""
        result = format_phone(None)
        assert "" in result


class TestFormatAddress:
    """Test format_address()"""
    
    def test_format_full(self):
        """Test full address"""
        result = format_address(
            street="123 Nguyễn Văn Linh",
            ward="Phường 5",
            district="Quận 7",
            city="TP.HCM"
        )
        assert "123 Nguyễn Văn Linh" in result
        assert "Phường 5" in result
        assert "Quận 7" in result
        assert "TP.HCM" in result
    
    def test_format_partial(self):
        """Test partial address"""
        result = format_address(street="123 Nguyễn Văn Linh", city="TP.HCM")
        assert "123 Nguyễn Văn Linh" in result
        assert "TP.HCM" in result
    
    def test_format_empty(self):
        """Test empty address"""
        result = format_address()
        assert "" in result


class TestFormatName:
    """Test format_name()"""
    
    def test_format_last_first(self):
        """Test last-first order (Vietnamese)"""
        result = format_name(
            first_name="Văn",
            last_name="Nguyễn",
            middle_name="Văn",
            display_order="last_first"
        )
        assert "Nguyễn" in result
        assert "Văn Văn" in result  # middle + first
    
    def test_format_first_last(self):
        """Test first-last order (Western)"""
        result = format_name(
            first_name="John",
            last_name="Doe",
            middle_name="Smith",
            display_order="first_last"
        )
        assert "John" in result
        assert "Smith" in result
        assert "Doe" in result
    
    def test_format_empty(self):
        """Test empty name"""
        result = format_name()
        assert "" in result


class TestFormatDuration:
    """Test format_duration()"""
    
    def test_format_seconds(self):
        """Test seconds only"""
        result = format_duration(45)
        assert "45s" in result
    
    def test_format_minutes(self):
        """Test minutes"""
        result = format_duration(120)
        assert "2p" in result
    
    def test_format_hours(self):
        """Test hours"""
        result = format_duration(3600)
        assert "1h" in result
    
    def test_format_hours_minutes(self):
        """Test hours and minutes"""
        result = format_duration(5400)  # 1h 30p
        assert "1h" in result
        assert "30p" in result
    
    def test_format_days(self):
        """Test days"""
        result = format_duration(86400)  # 1 day
        assert "1n" in result
    
    def test_format_days_hours(self):
        """Test days and hours"""
        result = format_duration(97200)  # 1d 3h
        assert "1n" in result
        assert "3h" in result
    
    def test_format_none(self):
        """Test None value"""
        result = format_duration(None)
        assert "0s" in result
    
    def test_format_negative(self):
        """Test negative value"""
        result = format_duration(-100)
        assert "0s" in result


class TestTruncateText:
    """Test truncate_text()"""
    
    def test_truncate_long_text(self):
        """Test truncating long text"""
        text = "a" * 100
        result = truncate_text(text, max_length=50)
        assert len(result) == 50
        assert "..." in result
    
    def test_truncate_short_text(self):
        """Test text shorter than max"""
        text = "short"
        result = truncate_text(text, max_length=50)
        assert result == "short"
    
    def test_custom_suffix(self):
        """Test custom suffix"""
        text = "a" * 100
        result = truncate_text(text, max_length=50, suffix="...")
        assert result.endswith("...")
    
    def test_empty_text(self):
        """Test empty text"""
        result = truncate_text("")
        assert "" in result
    
    def test_none_text(self):
        """Test None text"""
        result = truncate_text(None)
        assert "" in result


class TestCapitalizeWords:
    """Test capitalize_words()"""
    
    def test_capitalize_basic(self):
        """Test basic capitalization"""
        result = capitalize_words("hello world")
        assert "Hello" in result
        assert "World" in result
    
    def test_capitalize_single(self):
        """Test single word"""
        result = capitalize_words("hello")
        assert "Hello" in result
    
    def test_capitalize_empty(self):
        """Test empty string"""
        result = capitalize_words("")
        assert "" in result
    
    def test_capitalize_none(self):
        """Test None"""
        result = capitalize_words(None)
        assert "" in result


class TestSlugify:
    """Test slugify()"""
    
    def test_slugify_basic(self):
        """Test basic slugify"""
        result = slugify("Hello World")
        assert "hello" in result
        assert "world" in result
        assert "-" in result
        assert " " not in result
    
    def test_slugify_special_chars(self):
        """Test with special characters"""
        result = slugify("Hello! World?")
        assert "hello" in result
        assert "world" in result
    
    def test_slugify_multiple_spaces(self):
        """Test with multiple spaces"""
        result = slugify("Hello   World")
        assert "--" not in result
    
    def test_slugify_empty(self):
        """Test empty string"""
        result = slugify("")
        assert "" in result


# Run tests with: pytest tests/test_utils/test_formatters.py -v
