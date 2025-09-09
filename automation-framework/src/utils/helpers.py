"""Helper utilities for the automation framework."""

import time
import random
import string
from functools import wraps
from typing import Any, Callable, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import json
import yaml
from pathlib import Path

from ..config.settings import config
from .logger import get_logger

logger = get_logger(__name__)


def retry_on_exception(
    exceptions: Tuple[Exception, ...] = (Exception,),
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0
):
    """
    Decorator to retry function on specific exceptions.
    
    Args:
        exceptions: Tuple of exceptions to catch
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff_factor: Multiplier for delay after each retry
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            raise last_exception
        
        return wrapper
    return decorator


def wait_for_condition(
    condition: Callable[[], bool],
    timeout: float = 10.0,
    poll_interval: float = 0.5,
    timeout_message: str = "Condition not met within timeout"
) -> bool:
    """
    Wait for a condition to be true.
    
    Args:
        condition: Function that returns boolean
        timeout: Maximum time to wait
        poll_interval: Time between checks
        timeout_message: Message to log on timeout
        
    Returns:
        True if condition met, False if timeout
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(poll_interval)
    
    logger.warning(f"{timeout_message} (timeout: {timeout}s)")
    return False


def generate_random_string(length: int = 10, include_digits: bool = True) -> str:
    """
    Generate random string.
    
    Args:
        length: String length
        include_digits: Whether to include digits
        
    Returns:
        Random string
    """
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_email(domain: str = "example.com") -> str:
    """
    Generate random email address.
    
    Args:
        domain: Email domain
        
    Returns:
        Random email address
    """
    username = generate_random_string(8)
    return f"{username}@{domain}"


def generate_random_phone() -> str:
    """
    Generate random phone number.
    
    Returns:
        Random phone number in format +1-XXX-XXX-XXXX
    """
    area_code = random.randint(200, 999)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"+1-{area_code}-{exchange}-{number}"


def format_timestamp(timestamp: Optional[datetime] = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format timestamp.
    
    Args:
        timestamp: Timestamp to format (uses current time if None)
        format_str: Format string
        
    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime(format_str)


def parse_timestamp(timestamp_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse timestamp string.
    
    Args:
        timestamp_str: Timestamp string
        format_str: Format string
        
    Returns:
        Parsed datetime object
    """
    return datetime.strptime(timestamp_str, format_str)


def load_json_file(file_path: Union[str, Path]) -> dict:
    """
    Load JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: dict, file_path: Union[str, Path], indent: int = 2) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save file
        indent: JSON indentation
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_yaml_file(file_path: Union[str, Path]) -> dict:
    """
    Load YAML file.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed YAML data
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml_file(data: dict, file_path: Union[str, Path]) -> None:
    """
    Save data to YAML file.
    
    Args:
        data: Data to save
        file_path: Path to save file
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def get_test_data_file(filename: str) -> Path:
    """
    Get path to test data file.
    
    Args:
        filename: Test data filename
        
    Returns:
        Full path to test data file
    """
    return config.get_test_data_path(filename)


def get_fixture_file(filename: str) -> Path:
    """
    Get path to fixture file.
    
    Args:
        filename: Fixture filename
        
    Returns:
        Full path to fixture file
    """
    return config.get_fixture_path(filename)


def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    """
    Mask sensitive data for logging.
    
    Args:
        data: Data to mask
        mask_char: Character to use for masking
        visible_chars: Number of characters to keep visible
        
    Returns:
        Masked data string
    """
    if len(data) <= visible_chars:
        return mask_char * len(data)
    
    # Special handling for email addresses
    if "@" in data:
        local_part, domain = data.split("@", 1)
        # For emails, show the first visible_chars characters, but always mask at least one character
        if len(local_part) <= visible_chars:
            if len(local_part) > 1:
                # Show first 3 characters and mask the rest
                masked_local = local_part[:3] + mask_char * (len(local_part) - 3)
            else:
                masked_local = local_part
        else:
            masked_local = local_part[:visible_chars] + mask_char * (len(local_part) - visible_chars)
        return f"{masked_local}@{domain}"
    
    return data[:visible_chars] + mask_char * (len(data) - visible_chars)


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid email format
    """
    import re
    if not email or not isinstance(email, str):
        return False
    
    # More permissive regex that allows short domains like "a@b.c"
    # but rejects consecutive dots and other invalid patterns
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$'
    
    # Additional checks for invalid patterns
    if '..' in email or email.startswith('.') or email.endswith('.'):
        return False
    if email.count('@') != 1:
        return False
    
    # Check for valid local part (before @)
    local_part = email.split('@')[0]
    if not local_part or local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    # Check for valid domain part (after @)
    domain_part = email.split('@')[1]
    if not domain_part or '.' not in domain_part:
        return False
    
    # Check for dots at start/end of domain parts
    domain_parts = domain_part.split('.')
    for part in domain_parts:
        if not part or part.startswith('.') or part.endswith('.'):
            return False
    
    # Check for reasonable length limits
    if len(local_part) > 64 or len(domain_part) > 253:
        return False
    
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid phone format
    """
    import re
    
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's 10 digits (US format) or 11 digits (with country code)
    if len(digits) == 10:
        return True
    elif len(digits) == 11 and digits.startswith('1'):
        return True
    # International format: 7-14 digits (more restrictive than ITU-T E.164)
    elif 7 <= len(digits) <= 14:
        return True
    else:
        return False


def convert_to_dict(obj: Any) -> dict:
    """
    Convert object to dictionary recursively.
    
    Args:
        obj: Object to convert
        
    Returns:
        Dictionary representation
    """
    if hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                result[key] = convert_to_dict(value)
        return result
    elif isinstance(obj, (list, tuple)):
        return [convert_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def deep_merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flatten nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for recursion
        sep: Separator for keys
        
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


def get_environment_variable(key: str, default: Any = None, required: bool = False) -> Any:
    """
    Get environment variable with validation.
    
    Args:
        key: Environment variable key
        default: Default value if not found
        required: Whether variable is required
        
    Returns:
        Environment variable value
        
    Raises:
        ValueError: If required variable is not found
    """
    import os
    
    value = os.getenv(key, default)
    
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' not found")
    
    return value


def measure_execution_time(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    
    return wrapper
