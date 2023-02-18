from pkg_resources import require


__url__ = "https://github.com/eXhumer/pyeXDC"
__version__ = require(__package__)[0].version
__user_agent__ = f"DiscordBot ({__url__}, {__version__})"
