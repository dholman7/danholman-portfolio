"""Base page class implementing Page Object Model pattern."""

import time
from typing import Any, Dict, List, Optional, Tuple, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)

from ..config.settings import config
from ..utils.logger import get_logger
from ..utils.helpers import retry_on_exception


logger = get_logger(__name__)


class BasePage:
    """Base page class with common functionality for all page objects."""
    
    def __init__(self, driver: WebDriver, timeout: int = None):
        """
        Initialize base page.
        
        Args:
            driver: WebDriver instance
            timeout: Custom timeout for this page (uses config default if None)
        """
        self.driver = driver
        self.timeout = timeout or config.browser.explicit_wait
        self.wait = WebDriverWait(driver, self.timeout)
        self._page_loaded = False
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """
        Wait for page to fully load.
        
        Args:
            timeout: Custom timeout
            
        Returns:
            True if page loaded successfully, False otherwise
        """
        timeout = timeout or self.timeout
        
        try:
            # Wait for document ready state
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for jQuery if present
            try:
                self.wait.until(
                    lambda driver: driver.execute_script("return typeof jQuery === 'undefined' || jQuery.active === 0")
                )
            except TimeoutException:
                logger.warning("jQuery not found or still loading, continuing...")
            
            self._page_loaded = True
            return True
            
        except TimeoutException:
            logger.error(f"Page load timeout after {timeout} seconds")
            return False
    
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Find single element with retry logic.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            WebElement instance
            
        Raises:
            NoSuchElementException: If element not found
        """
        timeout = timeout or self.timeout
        
        @retry_on_exception(
            exceptions=(StaleElementReferenceException,),
            max_attempts=3,
            delay=0.5
        )
        def _find_element():
            return self.wait.until(EC.presence_of_element_located(locator))
        
        try:
            return _find_element()
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise NoSuchElementException(f"Element not found: {locator}")
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """
        Find multiple elements.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            List of WebElement instances
        """
        timeout = timeout or self.timeout
        
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.warning(f"No elements found: {locator}")
            return []
    
    def click_element(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """
        Click element with retry logic.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
        """
        timeout = timeout or self.timeout
        
        @retry_on_exception(
            exceptions=(ElementNotInteractableException, StaleElementReferenceException),
            max_attempts=3,
            delay=0.5
        )
        def _click_element():
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        
        try:
            _click_element()
            logger.debug(f"Clicked element: {locator}")
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise
    
    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = None) -> None:
        """
        Send keys to element.
        
        Args:
            locator: Tuple of (By, selector)
            text: Text to send
            clear_first: Whether to clear field first
            timeout: Custom timeout
        """
        timeout = timeout or self.timeout
        
        element = self.wait.until(EC.presence_of_element_located(locator))
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        logger.debug(f"Sent keys to element {locator}: {text[:10]}...")
    
    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """
        Get text from element.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            Element text
        """
        timeout = timeout or self.timeout
        element = self.find_element(locator, timeout)
        return element.text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: int = None) -> str:
        """
        Get attribute value from element.
        
        Args:
            locator: Tuple of (By, selector)
            attribute: Attribute name
            timeout: Custom timeout
            
        Returns:
            Attribute value
        """
        timeout = timeout or self.timeout
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Check if element is present.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            True if element is present, False otherwise
        """
        timeout = timeout or self.timeout
        
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            True if element is visible, False otherwise
        """
        timeout = timeout or self.timeout
        
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Wait for element to be visible.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            WebElement instance
        """
        timeout = timeout or self.timeout
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
            
        Returns:
            WebElement instance
        """
        timeout = timeout or self.timeout
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def select_dropdown_option(self, locator: Tuple[str, str], option: Union[str, int], timeout: int = None) -> None:
        """
        Select option from dropdown.
        
        Args:
            locator: Tuple of (By, selector)
            option: Option text or index
            timeout: Custom timeout
        """
        timeout = timeout or self.timeout
        element = self.find_element(locator, timeout)
        select = Select(element)
        
        if isinstance(option, str):
            select.select_by_visible_text(option)
        else:
            select.select_by_index(option)
        
        logger.debug(f"Selected dropdown option: {option}")
    
    def scroll_to_element(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """
        Scroll to element.
        
        Args:
            locator: Tuple of (By, selector)
            timeout: Custom timeout
        """
        timeout = timeout or self.timeout
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Allow scroll to complete
    
    def execute_javascript(self, script: str, *args) -> Any:
        """
        Execute JavaScript.
        
        Args:
            script: JavaScript code
            *args: Arguments to pass to script
            
        Returns:
            Script execution result
        """
        return self.driver.execute_script(script, *args)
    
    def take_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot.
        
        Args:
            filename: Custom filename
            
        Returns:
            Screenshot file path
        """
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = config.get_report_path(filename)
        self.driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)
    
    def get_page_title(self) -> str:
        """Get page title."""
        return self.driver.title
    
    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        """
        self.driver.get(url)
        self.wait_for_page_load()
        logger.info(f"Navigated to: {url}")
    
    def refresh_page(self) -> None:
        """Refresh current page."""
        self.driver.refresh()
        self.wait_for_page_load()
        logger.debug("Page refreshed")
    
    def go_back(self) -> None:
        """Go back in browser history."""
        self.driver.back()
        self.wait_for_page_load()
        logger.debug("Navigated back")
    
    def go_forward(self) -> None:
        """Go forward in browser history."""
        self.driver.forward()
        self.wait_for_page_load()
        logger.debug("Navigated forward")
