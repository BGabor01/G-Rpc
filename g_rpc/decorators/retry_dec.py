import functools
import time

def retry(max_retries=3, delay = 1, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    args[0].logger.error(f"Error:  {str(e)}. Retrying after {delay} seconds")
                    time.sleep(delay)

            args[0].logger.error(f"Error: Reached max retries. Not retrying further.")
            raise TimeoutError("Error: Reached max retries. Not retrying further.")
        return wrapper
    return decorator
