"""
Test suite cho Validators
"""
import pytest
from src.utils.validators import (
    validate_email,
    validate_phone,
    validate_required,
    validate_length,
    validate_number,
    validate_date,
    validate_currency,
    validate_password,
    validate_form,
)


class TestValidateEmail:
    """Test validate_email()"""
    
    def test_valid_email(self):
        """Test valid emails"""
        valid_emails = [
            'test@example.com',
            'nguyenvana@email.com',
            'test.user@company.co.uk',
            'user+tag@gmail.com',
            'user123@test.org',
        ]
        
        for email in valid_emails:
            result = validate_email(email)
            assert result.is_valid, f"Email {email} should be valid"
    
    def test_invalid_email(self):
        """Test invalid emails"""
        invalid_emails = [
            'invalid',
            'invalid@',
            '@example.com',
            'invalid@.com',
            'invalid @example.com',
            '',
        ]
        
        for email in invalid_emails:
            result = validate_email(email)
            assert not result.is_valid, f"Email {email} should be invalid"
    
    def test_empty_email(self):
        """Test empty email"""
        result = validate_email('')
        assert not result.is_valid
        assert 'không được để trống' in result.message
    
    def test_long_email(self):
        """Test very long email"""
        long_email = 'a' * 250 + '@example.com'
        result = validate_email(long_email)
        assert not result.is_valid
        assert 'quá dài' in result.message


class TestValidatePhone:
    """Test validate_phone()"""
    
    def test_valid_phone(self):
        """Test valid Vietnamese phone numbers"""
        valid_phones = [
            '0901234567',
            '09012345678',
            '0123456789',
            '0345678901',
            '0567890123',
            '0789012345',
            '0890123456',
            '84901234567',
            '+84901234567',
        ]
        
        for phone in valid_phones:
            result = validate_phone(phone)
            assert result.is_valid, f"Phone {phone} should be valid"
    
    def test_invalid_phone(self):
        """Test invalid phone numbers"""
        invalid_phones = [
            '123456',  # Too short
            '1234567890123',  # Too long
            'abc1234567',  # Contains letters
            '',  # Empty
            '090 123 456',  # Incomplete
        ]
        
        for phone in invalid_phones:
            result = validate_phone(phone)
            assert not result.is_valid, f"Phone {phone} should be invalid"
    
    def test_phone_with_spaces(self):
        """Test phone with spaces/dashes"""
        result = validate_phone('0901 234 567')
        assert result.is_valid  # Should handle spaces
    
    def test_empty_phone(self):
        """Test empty phone"""
        result = validate_phone('')
        assert not result.is_valid
        assert 'không được để trống' in result.message


class TestValidateRequired:
    """Test validate_required()"""
    
    def test_valid_required(self):
        """Test valid required fields"""
        valid_values = [
            'text',
            123,
            0,
            ['item'],
            {'key': 'value'},
            True,
            False,
        ]
        
        for value in valid_values:
            result = validate_required(value, 'Test field')
            assert result.is_valid, f"Value {value} should be valid"
    
    def test_invalid_required(self):
        """Test invalid required fields"""
        invalid_values = [
            None,
            '',
            '   ',  # whitespace only
            [],
            {},
        ]
        
        for value in invalid_values:
            result = validate_required(value, 'Test field')
            assert not result.is_valid, f"Value {value} should be invalid"
            assert 'không được để trống' in result.message


class TestValidateLength:
    """Test validate_length()"""
    
    def test_valid_length(self):
        """Test valid length"""
        result = validate_length('hello', min_len=1, max_len=10, field_name='Test')
        assert result.is_valid
    
    def test_too_short(self):
        """Test too short"""
        result = validate_length('hi', min_len=5, field_name='Test field')
        assert not result.is_valid
        assert 'ít nhất 5 ký tự' in result.message
    
    def test_too_long(self):
        """Test too long"""
        result = validate_length('hello world', max_len=5, field_name='Test field')
        assert not result.is_valid
        assert 'không được vượt quá 5 ký tự' in result.message
    
    def test_non_string(self):
        """Test with non-string value"""
        result = validate_length(123, min_len=1, field_name='Test')
        assert result.is_valid  # Should skip validation


class TestValidateNumber:
    """Test validate_number()"""
    
    def test_valid_number(self):
        """Test valid numbers"""
        valid_values = [10, 10.5, '10', '10.5', 0, -5]
        
        for value in valid_values:
            result = validate_number(value, field_name='Test')
            assert result.is_valid, f"Value {value} should be valid"
    
    def test_min_value(self):
        """Test minimum value"""
        result = validate_number(5, min_value=10, field_name='Test field')
        assert not result.is_valid
        assert 'lớn hơn hoặc bằng 10' in result.message
    
    def test_max_value(self):
        """Test maximum value"""
        result = validate_number(15, max_value=10, field_name='Test field')
        assert not result.is_valid
        assert 'nhỏ hơn hoặc bằng 10' in result.message
    
    def test_invalid_number(self):
        """Test invalid number"""
        result = validate_number('abc', field_name='Test field')
        assert not result.is_valid
        assert 'phải là số' in result.message


class TestValidateCurrency:
    """Test validate_currency()"""
    
    def test_valid_currency(self):
        """Test valid currency values"""
        valid_values = [100, 100.5, 100.55, '100', 0]
        
        for value in valid_values:
            result = validate_currency(value, 'Test amount')
            assert result.is_valid, f"Value {value} should be valid"
    
    def test_negative_currency(self):
        """Test negative currency"""
        result = validate_currency(-100, 'Test amount')
        assert not result.is_valid
        assert 'lớn hơn hoặc bằng 0' in result.message
    
    def test_too_many_decimals(self):
        """Test too many decimal places"""
        result = validate_currency(100.555, 'Test amount')
        assert not result.is_valid
        assert 'không được vượt quá 2 chữ số thập phân' in result.message


class TestValidatePassword:
    """Test validate_password()"""
    
    def test_valid_password(self):
        """Test valid passwords"""
        valid_passwords = [
            'password1',
            'MyP@ssw0rd',
            '123456a',
            'abcdefgh1',
        ]
        
        for password in valid_passwords:
            result = validate_password(password, min_length=6)
            assert result.is_valid, f"Password {password} should be valid"
    
    def test_too_short(self):
        """Test too short password"""
        result = validate_password('abc12', min_length=6)
        assert not result.is_valid
        assert 'ít nhất 6 ký tự' in result.message
    
    def test_no_letter(self):
        """Test password without letter"""
        result = validate_password('12345678', min_length=6)
        assert not result.is_valid
        assert 'chứa ít nhất một chữ cái' in result.message
    
    def test_no_number(self):
        """Test password without number"""
        result = validate_password('abcdefgh', min_length=6)
        assert not result.is_valid
        assert 'chứa ít nhất một số' in result.message
    
    def test_empty_password(self):
        """Test empty password"""
        result = validate_password('', min_length=6)
        assert not result.is_valid
        assert 'không được để trống' in result.message


class TestValidateForm:
    """Test validate_form()"""
    
    def test_valid_form(self):
        """Test valid form"""
        data = {
            'email': 'test@example.com',
            'phone': '0901234567',
        }
        
        validators = {
            'email': validate_email,
            'phone': validate_phone,
        }
        
        is_valid, errors = validate_form(data, validators)
        
        assert is_valid
        assert len(errors) == 0
    
    def test_invalid_form(self):
        """Test invalid form"""
        data = {
            'email': 'invalid',
            'phone': '123',
        }
        
        validators = {
            'email': validate_email,
            'phone': validate_phone,
        }
        
        is_valid, errors = validate_form(data, validators)
        
        assert not is_valid
        assert 'email' in errors
        assert 'phone' in errors
    
    def test_partial_valid_form(self):
        """Test form with some valid and some invalid fields"""
        data = {
            'email': 'valid@example.com',
            'phone': 'invalid',
        }
        
        validators = {
            'email': validate_email,
            'phone': validate_phone,
        }
        
        is_valid, errors = validate_form(data, validators)
        
        assert not is_valid
        assert 'email' not in errors
        assert 'phone' in errors


# Run tests with: pytest tests/test_utils/test_validators.py -v
