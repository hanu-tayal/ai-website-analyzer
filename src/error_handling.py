"""
Error handling and retry mechanisms for the Playwright AI Browser.
"""
import asyncio
import time
from typing import Callable, Any, Optional, Dict, List
from functools import wraps
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetryError(Exception):
    """Custom exception for retry failures."""
    pass


class BrowserError(Exception):
    """Custom exception for browser-related errors."""
    pass


class AIAnalysisError(Exception):
    """Custom exception for AI analysis errors."""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,)
):
    """Decorator that retries a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        jitter: Whether to add random jitter to delays
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise RetryError(f"Function {func.__name__} failed after {max_retries} retries") from e
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    
                    # Add jitter if enabled
                    if jitter:
                        import random
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    
                    await asyncio.sleep(delay)
            
            # This should never be reached, but just in case
            raise RetryError(f"Function {func.__name__} failed after {max_retries} retries") from last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise RetryError(f"Function {func.__name__} failed after {max_retries} retries") from e
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    
                    # Add jitter if enabled
                    if jitter:
                        import random
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise RetryError(f"Function {func.__name__} failed after {max_retries} retries") from last_exception
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


class ErrorHandler:
    """Centralized error handling for the AI browser."""
    
    def __init__(self, max_retries: int = 3):
        """Initialize the error handler.
        
        Args:
            max_retries: Default maximum number of retries
        """
        self.max_retries = max_retries
        self.error_counts: Dict[str, int] = {}
        self.error_history: List[Dict[str, Any]] = []
    
    def log_error(self, error_type: str, error: Exception, context: Dict[str, Any] = None) -> None:
        """Log an error with context.
        
        Args:
            error_type: Type of error (e.g., 'navigation', 'ai_analysis', 'form_fill')
            error: The exception that occurred
            context: Additional context about the error
        """
        error_info = {
            "timestamp": time.time(),
            "error_type": error_type,
            "error_message": str(error),
            "error_class": error.__class__.__name__,
            "context": context or {}
        }
        
        self.error_history.append(error_info)
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        logger.error(f"{error_type} error: {error}")
        if context:
            logger.error(f"Context: {context}")
    
    def should_retry(self, error_type: str, error: Exception) -> bool:
        """Determine if an error should be retried.
        
        Args:
            error_type: Type of error
            error: The exception that occurred
            
        Returns:
            True if the error should be retried
        """
        # Don't retry if we've exceeded max retries for this error type
        if self.error_counts.get(error_type, 0) >= self.max_retries:
            return False
        
        # Don't retry certain types of errors
        non_retryable_errors = (
            KeyboardInterrupt,
            SystemExit,
            MemoryError,
            RecursionError
        )
        
        if isinstance(error, non_retryable_errors):
            return False
        
        # Don't retry authentication errors
        if "auth" in error_type.lower() or "login" in error_type.lower():
            return False
        
        return True
    
    def get_retry_delay(self, error_type: str) -> float:
        """Get the delay before retrying based on error type and history.
        
        Args:
            error_type: Type of error
            
        Returns:
            Delay in seconds before retrying
        """
        base_delay = 1.0
        error_count = self.error_counts.get(error_type, 0)
        
        # Exponential backoff with jitter
        delay = base_delay * (2 ** error_count)
        delay = min(delay, 30.0)  # Cap at 30 seconds
        
        # Add jitter
        import random
        delay *= (0.5 + random.random() * 0.5)
        
        return delay
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of all errors that occurred.
        
        Returns:
            Dictionary containing error summary
        """
        return {
            "total_errors": len(self.error_history),
            "error_counts": self.error_counts.copy(),
            "recent_errors": self.error_history[-10:],  # Last 10 errors
            "error_types": list(self.error_counts.keys())
        }


def safe_async_execute(func: Callable, *args, **kwargs) -> Any:
    """Safely execute an async function with error handling.
    
    Args:
        func: The async function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
        
    Returns:
        Result of the function execution or None if it failed
    """
    async def _execute():
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error executing {func.__name__}: {e}")
            return None
    
    return asyncio.run(_execute())


def validate_url(url: str) -> bool:
    """Validate that a URL is properly formatted.
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL is valid, False otherwise
    """
    import re
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))


def validate_credentials(credentials: Dict[str, str]) -> List[str]:
    """Validate user credentials and return any validation errors.
    
    Args:
        credentials: Dictionary containing user credentials
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    # Check required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if not credentials.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate email format
    email = credentials.get('email', '')
    if email and '@' not in email:
        errors.append("Invalid email format")
    
    # Validate password strength
    password = credentials.get('password', '')
    if password and len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    return errors


class CircuitBreaker:
    """Circuit breaker pattern implementation for preventing cascading failures."""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        """Initialize the circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening the circuit
            timeout: Time in seconds before attempting to close the circuit
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function through the circuit breaker.
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function execution
            
        Raises:
            Exception: If the circuit is open or the function fails
        """
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self) -> None:
        """Handle successful function execution."""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self) -> None:
        """Handle failed function execution."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
