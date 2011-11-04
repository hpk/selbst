
def call_func(name, *args, **kwargs):
    """Call a function when all you have is the [str] name and arguments."""
    parts = name.split('.')
    module = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
    return getattr(module, parts[-1])(*args, **kwargs)
