"""Logging utilities for the automation framework."""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from ..config.settings import config


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        """Format log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up logger with file and console handlers.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        console_output: Whether to output to console
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = config.get_report_path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class ContextLogger:
    """Test-specific logger with additional context."""
    
    def __init__(self, test_name: str, logger: Optional[logging.Logger] = None):
        """
        Initialize test logger.
        
        Args:
            test_name: Name of the test
            logger: Optional base logger
        """
        self.test_name = test_name
        self.logger = logger or get_logger(f"test.{test_name}")
        self.start_time = datetime.now()
        
        self.logger.info(f"Starting test: {test_name}")
    
    def log_step(self, step: str, details: str = "") -> None:
        """
        Log test step.
        
        Args:
            step: Step description
            details: Additional details
        """
        message = f"[{self.test_name}] {step}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_assertion(self, assertion: str, result: bool) -> None:
        """
        Log assertion result.
        
        Args:
            assertion: Assertion description
            result: Assertion result
        """
        status = "PASS" if result else "FAIL"
        self.logger.info(f"[{self.test_name}] Assertion: {assertion} - {status}")
    
    def log_error(self, error: str, exception: Optional[Exception] = None) -> None:
        """
        Log error.
        
        Args:
            error: Error description
            exception: Optional exception instance
        """
        self.logger.error(f"[{self.test_name}] Error: {error}")
        if exception:
            self.logger.exception(f"[{self.test_name}] Exception details: {exception}")
    
    def log_warning(self, warning: str) -> None:
        """
        Log warning.
        
        Args:
            warning: Warning message
        """
        self.logger.warning(f"[{self.test_name}] Warning: {warning}")
    
    def log_test_completion(self, passed: bool) -> None:
        """
        Log test completion.
        
        Args:
            passed: Whether test passed
        """
        duration = datetime.now() - self.start_time
        status = "PASSED" if passed else "FAILED"
        self.logger.info(f"[{self.test_name}] Test {status} in {duration.total_seconds():.2f}s")


# Global logger setup
def setup_framework_logging():
    """Set up framework-wide logging."""
    # Create logs directory
    logs_dir = config.root_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Set up main framework logger
    framework_logger = setup_logger(
        "framework",
        level="INFO",
        log_file="framework.log"
    )
    
    # Set up test logger
    test_logger = setup_logger(
        "tests",
        level="DEBUG",
        log_file="tests.log"
    )
    
    return framework_logger, test_logger


# Initialize framework logging
framework_logger, test_logger = setup_framework_logging()
