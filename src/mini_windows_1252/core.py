# Windows-1252 codec implemented as a single explicit mapping table.
#
# Python's standard library already knows how to decode cp1252 via the codecs
# machinery, and for the 0x81 / 0x8D / 0x8F / 0x90 / 0x9D gap it historically
# substituted U+FFFD. We deliberately provide our own table instead, mapping
# every one of the 256 code points to a defined Unicode scalar, including the
# otherwise-undefined slots, which we map to U+FFFD (REPLACEMENT CHARACTER).
#
# Why hand-roll instead of wrapping codecs.lookup('cp1252')?
# - The table is only 256 entries; it fits in one screenful and is auditable.
# - The cp1252 builtin's error behaviour for the five undefined slots has
#   historically been inconsistent across CPython versions. Our behaviour is
#   fixed: undefined slots become U+FFFD, and encode() rejects U+FFFD input
#   because no code point in cp1252 produces it.
# - We avoid importing the codecs module's lazy registry machinery; the table
#   is a module-level tuple built once at import time.

# Lookup table: index = cp1252 byte, value = Unicode code point as int.
# Every slot is defined; undefined positions hold 0xFFFD (U+FFFD).
#
# Layout:
# - 0x00-0x7F: identical to ASCII
# - 0x80-0x9F: the Windows-specific upper-Latin block; five slots are
#   officially undefined in the standard, filled here with U+FFFD.
# - 0xA0-0xFF: identical to ISO-8859-1 (Latin-1).
_TABLE = (
    # 0x00-0x1F: C0 controls, same as ASCII/Latin-1
    0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007,
    0x0008, 0x0009, 0x000A, 0x000B, 0x000C, 0x000D, 0x000E, 0x000F,
    0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x0015, 0x0016, 0x0017,
    0x0018, 0x0019, 0x001A, 0x001B, 0x001C, 0x001D, 0x001E, 0x001F,
    # 0x20-0x7F: printable ASCII
    0x0020, 0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027,
    0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F,
    0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037,
    0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F,
    0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047,
    0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F,
    0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057,
    0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x005F,
    0x0060, 0x0061, 0x0062, 0x0063, 0x0064, 0x0065, 0x0066, 0x0067,
    0x0068, 0x0069, 0x006A, 0x006B, 0x006C, 0x006D, 0x006E, 0x006F,
    0x0070, 0x0071, 0x0072, 0x0073, 0x0074, 0x0075, 0x0076, 0x0077,
    0x0078, 0x0079, 0x007A, 0x007B, 0x007C, 0x007D, 0x007E, 0x007F,
    # 0x80-0x9F: Windows-specific block. Five slots are officially undefined
    # in the cp1252 standard; we fill them with U+FFFD so that decode() is
    # total over all 256 byte values rather than raising.
    0x20AC, 0xFFFD, 0x201A, 0x0192, 0x201E, 0x2026, 0x2020, 0x2021,
    0x02C6, 0x2030, 0x0160, 0x2039, 0x0152, 0xFFFD, 0x017D, 0xFFFD,
    0xFFFD, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014,
    0x02DC, 0x2122, 0x0161, 0x203A, 0x0153, 0xFFFD, 0x017E, 0x0178,
    # 0xA0-0xFF: identical to ISO-8859-1 (Latin-1)
    0x00A0, 0x00A1, 0x00A2, 0x00A3, 0x00A4, 0x00A5, 0x00A6, 0x00A7,
    0x00A8, 0x00A9, 0x00AA, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x00AF,
    0x00B0, 0x00B1, 0x00B2, 0x00B3, 0x00B4, 0x00B5, 0x00B6, 0x00B7,
    0x00B8, 0x00B9, 0x00BA, 0x00BB, 0x00BC, 0x00BD, 0x00BE, 0x00BF,
    0x00C0, 0x00C1, 0x00C2, 0x00C3, 0x00C4, 0x00C5, 0x00C6, 0x00C7,
    0x00C8, 0x00C9, 0x00CA, 0x00CB, 0x00CC, 0x00CD, 0x00CE, 0x00CF,
    0x00D0, 0x00D1, 0x00D2, 0x00D3, 0x00D4, 0x00D5, 0x00D6, 0x00D7,
    0x00D8, 0x00D9, 0x00DA, 0x00DB, 0x00DC, 0x00DD, 0x00DE, 0x00DF,
    0x00E0, 0x00E1, 0x00E2, 0x00E3, 0x00E4, 0x00E5, 0x00E6, 0x00E7,
    0x00E8, 0x00E9, 0x00EA, 0x00EB, 0x00EC, 0x00ED, 0x00EE, 0x00EF,
    0x00F0, 0x00F1, 0x00F2, 0x00F3, 0x00F4, 0x00F5, 0x00F6, 0x00F7,
    0x00F8, 0x00F9, 0x00FA, 0x00FB, 0x00FC, 0x00FD, 0x00FE, 0x00FF,
)

assert len(_TABLE) == 256, "cp1252 table must cover all 256 byte values"

# Encode lookup is built at import time: a dict from Unicode code point (int)
# back to the cp1252 byte that produced it. Because the five undefined cp1252
# slots map to U+FFFD, U+FFFD is deliberately NOT in this dict — there is no
# byte whose meaning is U+FFFD, so we refuse to encode it.
_ENCODE_MAP = {}
for _i in range(256):
    _cp = _TABLE[_i]
    # Don't let U+FFFD round-trip. If we allowed this, code could encode
    # U+FFFD to 0x81 and decode 0x81 back to U+FFFD, implying U+FFFD is a
    # real character in cp1252. It is not.
    if _cp != 0xFFFD:
        _ENCODE_MAP[_cp] = _i
del _i, _cp

# A name callers can pass to codecs.lookup() or for documentation. We expose
# it so downstream code does not have to hardcode the literal string.
ENCODING_NAME = "windows-1252"


def decode(data):
    """Decode a Windows-1252 byte string into a Python ``str``.

    Every one of the 256 possible byte values is defined by our table;
    the five slots that are officially undefined in the cp1252 standard
    (0x81, 0x8D, 0x8F, 0x90, 0x9D) decode to U+FFFD (REPLACEMENT CHARACTER)
    rather than raising. This makes :func:`decode` a total function over
    all length-256-or-less byte strings.

    :param data: a ``bytes`` (or ``bytearray``) value. ``int`` is rejected
        so callers do not accidentally pass a single code point.
    :returns: a ``str`` of the same length as ``len(data)``.
    :raises TypeError: if *data* is not bytes-like.
    """
    if isinstance(data, (bytes, bytearray)):
        # chr() on each int is faster than building via a comprehension of
        # table lookups when data is ASCII-heavy, but a list comprehension is
        # the clearest expression of intent and the table is only 256 entries.
        return "".join(chr(_TABLE[b]) for b in data)
    raise TypeError(
        "decode() expects bytes or bytearray, got %s" % type(data).__name__
    )


def encode(text):
    """Encode a Python ``str`` into Windows-1252 bytes.

    Every Unicode code point that has a real cp1252 byte is accepted.
    U+FFFD is rejected even though it appears in our decode table, because
    no cp1252 byte is defined to mean U+FFFD — those slots are simply
    undefined. Any other code point outside the cp1252 repertoire raises
    :class:`ValueError`.

    :param text: a ``str``.
    :returns: a ``bytes`` of the same length as ``len(text)``.
    :raises TypeError: if *text* is not a ``str``.
    :raises ValueError: if *text* contains a code point not representable
        in cp1252 (including U+FFFD).
    """
    if not isinstance(text, str):
        raise TypeError(
            "encode() expects str, got %s" % type(text).__name__
        )
    out = bytearray()
    for ch in text:
        cp = ord(ch)
        b = _ENCODE_MAP.get(cp)
        if b is None:
            raise ValueError(
                "character U+%04X is not representable in Windows-1252" % cp
            )
        out.append(b)
    return bytes(out)
