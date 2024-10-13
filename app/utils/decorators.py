import functools
import asyncio
import inspect
from app.configs.logging_config import logger

def log_function(start_message=None, end_message=None):
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                bound_args = inspect.signature(func).bind(*args, **kwargs)
                bound_args.apply_defaults()

                if start_message:
                    logger.info(start_message.format(**bound_args.arguments))
                else:
                    logger.info(f"Starting {func.__name__}")

                result = await func(*args, **kwargs)

                if end_message:
                    logger.info(end_message.format(result=result, **bound_args.arguments))
                else:
                    logger.info(f"Finished {func.__name__} successfully")
                
                return result

            except Exception as exc:
                logger.error(f"Error in {func.__name__}: {str(exc)}")
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                bound_args = inspect.signature(func).bind(*args, **kwargs)
                bound_args.apply_defaults()

                if start_message:
                    logger.info(start_message.format(**bound_args.arguments))
                else:
                    logger.info(f"Starting {func.__name__}")

                result = func(*args, **kwargs)

                if end_message:
                    logger.info(end_message.format(result=result, **bound_args.arguments))
                else:
                    logger.info(f"Finished {func.__name__} successfully")
                
                return result

            except Exception as exc:
                logger.error(f"Error in {func.__name__}: {str(exc)}")
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator
