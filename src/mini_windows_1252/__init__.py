# Public API for the mini-windows-1252 package.
#
# We re-export the two pure functions decode and encode so callers can do:
#     from mini_windows_1252 import decode, encode
# The single source of truth for the mapping lives in core.py.
from mini_windows_1252.core import decode, encode, ENCODING_NAME

__all__ = ["decode", "encode", "ENCODING_NAME"]
