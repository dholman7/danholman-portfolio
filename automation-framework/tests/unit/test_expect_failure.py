"""
Unit tests that are expected to fail for demonstration purposes.

These tests are intentionally designed to fail to demonstrate:
- Allure failure reporting capabilities
- Test framework error handling
- CI/CD pipeline behavior with failures
- Test result analysis and debugging workflows
"""

import pytest
from src.utils.helpers import validate_email, validate_phone, generate_random_string


@pytest.mark.unit
@pytest.mark.expect_failure
class TestExpectedFailures:
    """Test cases that are expected to fail for demonstration purposes."""

    @pytest.mark.unit
    def test_email_validation_strict_mode(self):
        """
        This test demonstrates a failure due to overly strict email validation.
        The test expects all emails to pass validation, but some edge cases fail.
        """
        # These emails should be valid but our current implementation rejects them
        edge_case_emails = [
            "user+tag+more@example.com",  # Multiple plus signs
            "user.name+tag@sub.domain.com",  # Complex local part
            "1234567890@example.com",  # Numeric local part
        ]
        
        for email in edge_case_emails:
            assert validate_email(email) is True, f"Email should be valid: {email}"

    @pytest.mark.unit
    def test_phone_validation_international_format(self):
        """
        This test demonstrates a failure due to international phone format validation.
        The test expects certain international formats to be accepted.
        """
        # These international phone numbers should be valid but our implementation rejects them
        international_phones = [
            "+44 20 7946 0958",  # UK format with spaces
            "+33 1 42 86 83 26",  # French format with spaces
            "+49 30 12345678",  # German format
            "+81 3 1234 5678",  # Japanese format
        ]
        
        for phone in international_phones:
            assert validate_phone(phone) is True, f"Phone should be valid: {phone}"

    @pytest.mark.unit
    def test_random_string_length_consistency(self):
        """
        This test demonstrates a failure due to random string length inconsistency.
        The test expects all generated strings to have exactly the requested length.
        """
        # This test will fail because generate_random_string(0) returns empty string
        # but the test expects it to return a string of length 0 (which it does, but the assertion is wrong)
        length = 0
        result = generate_random_string(length)
        assert len(result) == length, f"Expected length {length}, got {len(result)}"
        assert result != "", "Empty string should not be returned for length 0"

    @pytest.mark.unit
    def test_email_validation_performance(self):
        """
        This test demonstrates a failure due to performance expectations.
        The test expects email validation to complete within a certain time limit.
        """
        import time
        
        # Generate a very long email to test performance
        long_email = "a" * 1000 + "@" + "b" * 1000 + ".com"
        
        start_time = time.time()
        result = validate_email(long_email)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # This will fail because our validation is too slow for very long emails
        assert execution_time < 0.001, f"Email validation took too long: {execution_time:.4f}s"
        assert result is True, "Long email should be valid"

    @pytest.mark.unit
    def test_phone_validation_with_special_characters(self):
        """
        This test demonstrates a failure due to phone validation not handling special characters.
        The test expects certain phone formats with special characters to be accepted.
        """
        # These phone numbers contain special characters that should be handled
        special_phones = [
            "+1 (555) 123-4567",  # Parentheses
            "+1-555-123-4567",  # Dashes
            "+1.555.123.4567",  # Dots
            "+1 555 123 4567",  # Spaces
        ]
        
        for phone in special_phones:
            assert validate_phone(phone) is True, f"Phone with special chars should be valid: {phone}"

    @pytest.mark.unit
    def test_random_string_character_set(self):
        """
        This test demonstrates a failure due to random string character set expectations.
        The test expects certain character sets to be included in generated strings.
        """
        # This test will fail because our implementation doesn't guarantee specific character types
        result = generate_random_string(100)
        
        # These assertions will fail because we can't guarantee specific character types
        assert any(c.isupper() for c in result), "String should contain uppercase letters"
        assert any(c.islower() for c in result), "String should contain lowercase letters"
        assert any(c.isdigit() for c in result), "String should contain digits"
        assert any(c in "!@#$%^&*" for c in result), "String should contain special characters"

    @pytest.mark.unit
    def test_email_validation_case_sensitivity(self):
        """
        This test demonstrates a failure due to email case sensitivity expectations.
        The test expects email validation to be case-insensitive.
        """
        # These emails should be valid regardless of case
        case_variations = [
            "TEST@EXAMPLE.COM",
            "Test@Example.Com",
            "test@EXAMPLE.com",
        ]
        
        for email in case_variations:
            assert validate_email(email) is True, f"Email should be valid regardless of case: {email}"

    @pytest.mark.unit
    def test_phone_validation_country_code_handling(self):
        """
        This test demonstrates a failure due to country code validation expectations.
        The test expects certain country codes to be accepted.
        """
        # These phone numbers have country codes that should be accepted
        country_code_phones = [
            "+1 555 123 4567",  # US
            "+44 20 7946 0958",  # UK
            "+33 1 42 86 83 26",  # France
            "+49 30 12345678",  # Germany
            "+81 3 1234 5678",  # Japan
        ]
        
        for phone in country_code_phones:
            assert validate_phone(phone) is True, f"Phone with country code should be valid: {phone}"

    @pytest.mark.unit
    def test_random_string_uniqueness_guarantee(self):
        """
        This test demonstrates a failure due to uniqueness guarantee expectations.
        The test expects generated strings to be unique within a reasonable sample size.
        """
        # This test will fail because we can't guarantee uniqueness with a small sample size
        strings = [generate_random_string(5) for _ in range(1000)]  # Small length, large sample
        
        # This assertion will likely fail due to the birthday paradox
        assert len(set(strings)) == len(strings), "All generated strings should be unique"

    @pytest.mark.unit
    def test_email_validation_domain_validation(self):
        """
        This test demonstrates a failure due to domain validation expectations.
        The test expects certain domain formats to be accepted.
        """
        # These domain formats should be valid but our implementation might reject them
        domain_emails = [
            "test@sub.domain.com",  # Subdomain
            "test@domain.co.uk",  # Country code TLD
            "test@domain.info",  # Generic TLD
            "test@domain.museum",  # Long TLD
        ]
        
        for email in domain_emails:
            assert validate_email(email) is True, f"Email with domain should be valid: {email}"
