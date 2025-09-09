"""Configuration settings for the automation framework."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class Environment(Enum):
    """Supported environments."""
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"
    LOCAL = "local"


class Browser(Enum):
    """Supported browsers."""
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    EDGE = "edge"


@dataclass
class DatabaseConfig:
    """Database configuration."""
    host: str
    port: int
    name: str
    username: str
    password: str
    ssl_mode: str = "require"
    connection_timeout: int = 30
    pool_size: int = 10


@dataclass
class APIConfig:
    """API configuration."""
    base_url: str
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    verify_ssl: bool = True
    api_key: Optional[str] = None
    auth_token: Optional[str] = None


@dataclass
class BrowserConfig:
    """Browser configuration."""
    browser: Browser = Browser.CHROME
    headless: bool = False
    window_size: tuple = (1920, 1080)
    implicit_wait: int = 10
    explicit_wait: int = 30
    page_load_timeout: int = 60
    script_timeout: int = 30
    download_dir: Optional[str] = None
    user_data_dir: Optional[str] = None
    extensions: List[str] = field(default_factory=list)
    capabilities: Dict[str, any] = field(default_factory=dict)


@dataclass
class TestConfig:
    """Test configuration."""
    environment: Environment = Environment.LOCAL
    parallel_workers: int = 1
    max_failures: int = 5
    test_timeout: int = 300
    retry_failed: int = 1
    data_driven: bool = True
    screenshots_on_failure: bool = True
    videos_on_failure: bool = False
    allure_enabled: bool = True
    report_dir: str = "reports"
    test_data_dir: str = "test_data"
    fixtures_dir: str = "fixtures"


@dataclass
class FrameworkConfig:
    """Main framework configuration."""
    test: TestConfig = field(default_factory=TestConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    api: Optional[APIConfig] = None
    database: Optional[DatabaseConfig] = None
    
    # Framework paths
    root_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    src_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    tests_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "tests")
    
    def __post_init__(self):
        """Initialize derived paths and configurations."""
        self._load_environment_variables()
        self._validate_configuration()
    
    def _load_environment_variables(self) -> None:
        """Load configuration from environment variables."""
        # Environment
        env_str = os.getenv("TEST_ENVIRONMENT", "local").lower()
        if env_str in [e.value for e in Environment]:
            self.test.environment = Environment(env_str)
        
        # Browser settings
        browser_str = os.getenv("BROWSER", "chrome").lower()
        if browser_str in [b.value for b in Browser]:
            self.browser.browser = Browser(browser_str)
        
        self.browser.headless = os.getenv("HEADLESS", "false").lower() == "true"
        self.test.parallel_workers = int(os.getenv("PARALLEL_WORKERS", "1"))
        
        # API configuration
        api_base_url = os.getenv("API_BASE_URL")
        if api_base_url:
            self.api = APIConfig(
                base_url=api_base_url,
                api_key=os.getenv("API_KEY"),
                auth_token=os.getenv("AUTH_TOKEN"),
                verify_ssl=os.getenv("API_VERIFY_SSL", "true").lower() == "true"
            )
        
        # Database configuration
        db_host = os.getenv("DB_HOST")
        if db_host:
            self.database = DatabaseConfig(
                host=db_host,
                port=int(os.getenv("DB_PORT", "5432")),
                name=os.getenv("DB_NAME", "testdb"),
                username=os.getenv("DB_USERNAME", "testuser"),
                password=os.getenv("DB_PASSWORD", "testpass")
            )
    
    def _validate_configuration(self) -> None:
        """Validate configuration settings."""
        if self.test.parallel_workers < 1:
            raise ValueError("parallel_workers must be >= 1")
        
        if self.test.max_failures < 0:
            raise ValueError("max_failures must be >= 0")
        
        if self.browser.implicit_wait < 0:
            raise ValueError("implicit_wait must be >= 0")
    
    @property
    def is_ci(self) -> bool:
        """Check if running in CI environment."""
        return os.getenv("CI", "false").lower() == "true"
    
    @property
    def is_parallel(self) -> bool:
        """Check if parallel execution is enabled."""
        return self.test.parallel_workers > 1
    
    def get_test_data_path(self, filename: str) -> Path:
        """Get full path to test data file."""
        return self.root_dir / self.test.test_data_dir / filename
    
    def get_fixture_path(self, filename: str) -> Path:
        """Get full path to fixture file."""
        return self.root_dir / self.test.fixtures_dir / filename
    
    def get_report_path(self, filename: str) -> Path:
        """Get full path to report file."""
        report_dir = self.root_dir / self.test.report_dir
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir / filename


# Global configuration instance
config = FrameworkConfig()
