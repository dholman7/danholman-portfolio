"""
Unit tests for helper functions and utilities.

These tests focus on testing individual helper functions in isolation,
verifying their behavior with various inputs and edge cases.
"""

import pytest
import time
from datetime import datetime, timedelta
from src.utils.helpers import (
    validate_email,
    generate_random_string,
    generate_random_email,
    generate_random_phone,
    format_timestamp,
    parse_timestamp,
    mask_sensitive_data,
    validate_phone,
    convert_to_dict,
    deep_merge_dicts,
    chunk_list,
    flatten_dict,
    get_environment_variable,
    measure_execution_time
)


class TestGenerateRandomString:
    """Test random string generation utility."""

    @pytest.mark.unit
    def test_default_length(self):
        """Test default string length."""
        result = generate_random_string()
        assert len(result) == 10  # Default length
        assert result.isalnum()

    @pytest.mark.unit
    def test_custom_length(self):
        """Test custom string length."""
        for length in [5, 15, 50, 100]:
            result = generate_random_string(length)
            assert len(result) == length
            assert result.isalnum()

    @pytest.mark.unit
    def test_zero_length(self):
        """Test zero length string."""
        result = generate_random_string(0)
        assert result == ""

    @pytest.mark.unit
    def test_negative_length(self):
        """Test negative length string."""
        result = generate_random_string(-1)
        assert result == ""

    @pytest.mark.unit
    def test_string_uniqueness(self):
        """Test that generated strings are unique."""
        strings = [generate_random_string(20) for _ in range(100)]
        assert len(set(strings)) == 100  # All should be unique


class TestValidateEmail:
    """Test email validation utility."""

    @pytest.mark.unit
    def test_valid_emails(self):
        """Test valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@numbers.com",
            "a@b.c"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True, f"Should be valid: {email}"

    @pytest.mark.unit
    def test_invalid_emails(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@.com",
            "test@example.",
            "",
            None,
            "test@example.com.",
            "test@.example.com"
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False, f"Should be invalid: {email}"

    @pytest.mark.unit
    def test_email_edge_cases(self):
        """Test email validation edge cases."""
        # Empty string
        assert validate_email("") is False
        
        # None input
        assert validate_email(None) is False
        
        # Very long email
        long_email = "a" * 100 + "@example.com"
        assert validate_email(long_email) is False


class TestGenerateRandomEmail:
    """Test random email generation utility."""

    @pytest.mark.unit
    def test_default_domain(self):
        """Test email generation with default domain."""
        email = generate_random_email()
        assert "@example.com" in email
        assert validate_email(email) is True

    @pytest.mark.unit
    def test_custom_domain(self):
        """Test email generation with custom domain."""
        email = generate_random_email("test.org")
        assert "@test.org" in email
        assert validate_email(email) is True

    @pytest.mark.unit
    def test_email_uniqueness(self):
        """Test that generated emails are unique."""
        emails = [generate_random_email() for _ in range(100)]
        assert len(set(emails)) == 100  # All should be unique


class TestGenerateRandomPhone:
    """Test random phone generation utility."""

    @pytest.mark.unit
    def test_phone_format(self):
        """Test phone number format."""
        phone = generate_random_phone()
        assert phone.startswith("+")
        assert len(phone) >= 10
        assert phone[1:].replace("-", "").replace(" ", "").isdigit()

    @pytest.mark.unit
    def test_phone_validation(self):
        """Test that generated phones pass validation."""
        phone = generate_random_phone()
        assert validate_phone(phone) is True

    @pytest.mark.unit
    def test_phone_uniqueness(self):
        """Test that generated phones are unique."""
        phones = [generate_random_phone() for _ in range(100)]
        assert len(set(phones)) == 100  # All should be unique


class TestFormatTimestamp:
    """Test timestamp formatting utility."""

    @pytest.mark.unit
    def test_format_current_time(self):
        """Test formatting current time."""
        result = format_timestamp()
        assert isinstance(result, str)
        assert len(result) == 19  # "YYYY-MM-DD HH:MM:SS"

    @pytest.mark.unit
    def test_format_specific_time(self):
        """Test formatting specific time."""
        test_time = datetime(2021, 1, 1, 12, 30, 45)
        result = format_timestamp(test_time)
        assert result == "2021-01-01 12:30:45"

    @pytest.mark.unit
    def test_custom_format(self):
        """Test custom format string."""
        test_time = datetime(2021, 1, 1, 12, 30, 45)
        result = format_timestamp(test_time, "%Y-%m-%d")
        assert result == "2021-01-01"


class TestParseTimestamp:
    """Test timestamp parsing utility."""

    @pytest.mark.unit
    def test_parse_valid_timestamp(self):
        """Test parsing valid timestamp."""
        timestamp_str = "2021-01-01 12:30:45"
        result = parse_timestamp(timestamp_str)
        assert isinstance(result, datetime)
        assert result.year == 2021
        assert result.month == 1
        assert result.day == 1
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45

    @pytest.mark.unit
    def test_parse_custom_format(self):
        """Test parsing with custom format."""
        timestamp_str = "01/01/2021"
        result = parse_timestamp(timestamp_str, "%m/%d/%Y")
        assert isinstance(result, datetime)
        assert result.year == 2021
        assert result.month == 1
        assert result.day == 1

    @pytest.mark.unit
    def test_parse_invalid_timestamp(self):
        """Test parsing invalid timestamp."""
        with pytest.raises(ValueError):
            parse_timestamp("invalid-timestamp")


class TestMaskSensitiveData:
    """Test sensitive data masking utility."""

    @pytest.mark.unit
    def test_mask_email(self):
        """Test masking email addresses."""
        email = "test@example.com"
        result = mask_sensitive_data(email)
        assert "tes" in result  # First 3 characters should be visible
        assert "@example.com" in result
        assert "*" in result

    @pytest.mark.unit
    def test_mask_phone(self):
        """Test masking phone numbers."""
        phone = "+1234567890"
        result = mask_sensitive_data(phone)
        assert "*" in result
        assert len(result) == len(phone)

    @pytest.mark.unit
    def test_mask_custom_visible_chars(self):
        """Test masking with custom visible characters."""
        data = "1234567890"
        result = mask_sensitive_data(data, visible_chars=2)
        assert result.count("*") == 8
        assert len(result) == 10

    @pytest.mark.unit
    def test_mask_short_data(self):
        """Test masking short data."""
        data = "12"
        result = mask_sensitive_data(data)
        assert result == "**"  # All characters masked


class TestValidatePhone:
    """Test phone validation utility."""

    @pytest.mark.unit
    def test_valid_phones(self):
        """Test valid phone numbers."""
        valid_phones = [
            "+1234567890",
            "+1-234-567-8900",
            "+1 (234) 567-8900",
            "+44 20 7946 0958",
            "123-456-7890"
        ]
        
        for phone in valid_phones:
            assert validate_phone(phone) is True, f"Should be valid: {phone}"

    @pytest.mark.unit
    def test_invalid_phones(self):
        """Test invalid phone numbers."""
        invalid_phones = [
            "123",  # Too short
            "abc-def-ghij",  # Contains letters
            "",  # Empty
            None,  # None
            "123456789012345"  # Too long
        ]
        
        for phone in invalid_phones:
            assert validate_phone(phone) is False, f"Should be invalid: {phone}"


class TestConvertToDict:
    """Test object to dictionary conversion utility."""

    @pytest.mark.unit
    def test_convert_dict(self):
        """Test converting dictionary."""
        data = {"key": "value", "nested": {"inner": "data"}}
        result = convert_to_dict(data)
        assert result == data

    @pytest.mark.unit
    def test_convert_list(self):
        """Test converting list."""
        data = [1, 2, 3, {"key": "value"}]
        result = convert_to_dict(data)
        assert result == data

    @pytest.mark.unit
    def test_convert_primitive(self):
        """Test converting primitive types."""
        assert convert_to_dict("string") == "string"
        assert convert_to_dict(123) == 123
        assert convert_to_dict(True) == True
        assert convert_to_dict(None) == None


class TestDeepMergeDicts:
    """Test deep dictionary merging utility."""

    @pytest.mark.unit
    def test_merge_simple_dicts(self):
        """Test merging simple dictionaries."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        result = deep_merge_dicts(dict1, dict2)
        expected = {"a": 1, "b": 2, "c": 3, "d": 4}
        assert result == expected

    @pytest.mark.unit
    def test_merge_nested_dicts(self):
        """Test merging nested dictionaries."""
        dict1 = {"a": 1, "nested": {"x": 1, "y": 2}}
        dict2 = {"b": 2, "nested": {"y": 3, "z": 4}}
        result = deep_merge_dicts(dict1, dict2)
        expected = {"a": 1, "b": 2, "nested": {"x": 1, "y": 3, "z": 4}}
        assert result == expected

    @pytest.mark.unit
    def test_merge_with_overwrite(self):
        """Test merging with value overwriting."""
        dict1 = {"key": "value1"}
        dict2 = {"key": "value2"}
        result = deep_merge_dicts(dict1, dict2)
        assert result["key"] == "value2"


class TestChunkList:
    """Test list chunking utility."""

    @pytest.mark.unit
    def test_chunk_even_division(self):
        """Test chunking list with even division."""
        data = [1, 2, 3, 4, 5, 6]
        result = chunk_list(data, 2)
        expected = [[1, 2], [3, 4], [5, 6]]
        assert result == expected

    @pytest.mark.unit
    def test_chunk_uneven_division(self):
        """Test chunking list with uneven division."""
        data = [1, 2, 3, 4, 5]
        result = chunk_list(data, 2)
        expected = [[1, 2], [3, 4], [5]]
        assert result == expected

    @pytest.mark.unit
    def test_chunk_empty_list(self):
        """Test chunking empty list."""
        result = chunk_list([], 3)
        assert result == []

    @pytest.mark.unit
    def test_chunk_single_element(self):
        """Test chunking single element."""
        data = [1]
        result = chunk_list(data, 2)
        expected = [[1]]
        assert result == expected


class TestFlattenDict:
    """Test dictionary flattening utility."""

    @pytest.mark.unit
    def test_flatten_simple_dict(self):
        """Test flattening simple dictionary."""
        data = {"a": 1, "b": 2}
        result = flatten_dict(data)
        expected = {"a": 1, "b": 2}
        assert result == expected

    @pytest.mark.unit
    def test_flatten_nested_dict(self):
        """Test flattening nested dictionary."""
        data = {"a": 1, "b": {"c": 2, "d": 3}}
        result = flatten_dict(data)
        expected = {"a": 1, "b.c": 2, "b.d": 3}
        assert result == expected

    @pytest.mark.unit
    def test_flatten_deeply_nested_dict(self):
        """Test flattening deeply nested dictionary."""
        data = {"a": {"b": {"c": 1}}}
        result = flatten_dict(data)
        expected = {"a.b.c": 1}
        assert result == expected

    @pytest.mark.unit
    def test_flatten_custom_separator(self):
        """Test flattening with custom separator."""
        data = {"a": {"b": 1}}
        result = flatten_dict(data, sep="_")
        expected = {"a_b": 1}
        assert result == expected


class TestMeasureExecutionTime:
    """Test execution time measurement utility."""

    @pytest.mark.unit
    def test_measure_execution_time(self):
        """Test measuring execution time."""
        @measure_execution_time
        def test_function():
            time.sleep(0.01)  # 10ms
            return "test"
        
        result = test_function()
        assert result == "test"
        # The function should have added execution time info
        # This is tested by ensuring the function runs without error

    @pytest.mark.unit
    def test_measure_execution_time_with_args(self):
        """Test measuring execution time with function arguments."""
        @measure_execution_time
        def test_function_with_args(x, y):
            return x + y
        
        result = test_function_with_args(1, 2)
        assert result == 3