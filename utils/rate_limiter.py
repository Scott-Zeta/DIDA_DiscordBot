import time
from datetime import datetime
from functools import wraps
from collections import defaultdict
from utils.logger import Logger

log = Logger("utils.rate_limiter")

class RateLimiter:
    """Rate limiter utility for Discord commands and events"""
    
    def __init__(self):
        # Store user rate limit data in a nested structure:
        # {function_id: {user_id: {"last_used": timestamp, "count": number}}}
        self.limits = defaultdict(lambda: defaultdict(lambda: {"last_used": 0, "count": 0}))
        
    def _is_rate_limited(self, function_id, user_id, cooldown_seconds, max_uses=1):
        """
        Check if a user is currently rate limited for a specific function
        
        Args:
            function_id: Identifier for the function being rate limited
            user_id: The Discord user ID
            cooldown_seconds: Cooldown period in seconds
            max_uses: Maximum number of uses within cooldown period
            
        Returns:
            tuple: (is_limited, remaining_seconds, remaining_uses)
        """
        now = time.time()
        user_data = self.limits[function_id][user_id]
        
        # If cooldown period passed, reset counter
        if now - user_data["last_used"] > cooldown_seconds:
            user_data["count"] = 1  # Set to 1 since we're using it now
            user_data["last_used"] = now
            return False, 0, max_uses - 1
        
        # Check if under max uses
        if user_data["count"] < max_uses:
            user_data["count"] += 1
            return False, 0, max_uses - user_data["count"]
        
        # User is rate limited
        remaining = cooldown_seconds - (now - user_data["last_used"])
        return True, remaining, 0

# Create a single global rate limiter instance
global_rate_limiter = RateLimiter()

def rate_limit(cooldown_seconds=30, max_uses=1, key_func=None, shared_limit=False, feature_name="this feature"):
    """
    Decorator for rate limiting Discord commands and event handlers
    
    Args:
        cooldown_seconds: Cooldown period in seconds
        max_uses: Maximum number of uses within the cooldown period
        key_func: Function to extract rate limit key from function args 
                 (defaults to using message.author.id)
        shared_limit: If True, share the rate limit across all functions with the same shared_limit value
                     If False (default), each function has its own separate rate limit
    
    Returns:
        Function decorator
    """
    def decorator(func):
        # Create a unique identifier for this function
        function_id = shared_limit if shared_limit else f"{func.__module__}.{func.__qualname__}"
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the Discord context or message
            if len(args) < 2:
                log.warning(f"Rate limit decorator used on function with too few args: {func.__qualname__}")
                return await func(*args, **kwargs)
            
            # Try to get user_id from the arguments
            user_id = None
            
            if key_func:
                # Custom key function provided
                user_id = key_func(*args, **kwargs)
            else:
                # Default extraction from common Discord objects
                obj = args[1]  # The context or message object
                
                if hasattr(obj, 'author'):
                    # Message or similar object with author 
                    user_id = obj.author.id
                elif hasattr(obj, 'user'):
                    # Interaction or context with user
                    user_id = obj.user.id
            
            # No limit for bot itself
            if obj.author.bot:
                return await func(*args, **kwargs)
            
            if not user_id:
                log.warning(f"Could not extract user ID for rate limiting in {func.__qualname__}")
                return await func(*args, **kwargs)
                
            # Check rate limit using function-specific tracking
            is_limited, remaining, remaining_uses = global_rate_limiter._is_rate_limited(
                function_id, user_id, cooldown_seconds, max_uses)
            
            if is_limited:
                log.info(f"Rate limited user {user_id} on {func.__qualname__} for {remaining:.1f}s")
                
                # For command contexts that have respond method
                if hasattr(args[1], 'respond'):
                    await args[1].respond(f"⏳ Please wait {remaining:.1f} seconds before using {feature_name} again.")
                    return None
                    
                # For message events
                elif hasattr(args[1], 'channel') and hasattr(args[1], 'author'):
                    await args[1].channel.send(
                        f"⏳ {args[1].author.mention}, please wait {remaining:.1f} seconds before using {feature_name} again."
                    )
                    return None
            
            # Not rate limited, proceed with the function
            return await func(*args, **kwargs)
        
        # Store original function and rate limit info for introspection
        wrapper.__rate_limit_info__ = {
            "cooldown": cooldown_seconds,
            "max_uses": max_uses,
            "function_id": function_id,
            "shared": shared_limit
        }
        return wrapper
    
    return decorator