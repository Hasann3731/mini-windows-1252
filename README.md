# mini-windows-1252

A pure-Python, zero-dependency decoder and encoder for the Windows-1252 character set. Every one of the 256 byte values is mapped to a defined Unicode scalar.

```python
from mini_windows_1252 import decode, encode, ENCODING_NAME

decode(b"\x80")      # '\u20AC'  (EURO SIGN)
encode("\u20AC")      # b'\x80'
encode("\u2014")      # b'\x97'   (EM DASH)
```

The package exports `decode(data)`, `encode(text)`, and the constant `ENCODING_NAME` (the string `"windows-1252"`).

## Why

Python's standard library already has a `cp1252` codec. This library exists for two reasons: it makes the full 256-entry table auditable in one file rather than relying on the codecs registry, and it pins a single, predictable behaviour for the five bytes that the Windows-1252 standard leaves undefined (`0x81`, `0x8D`, `0x8F`, `0x90`, `0x9D`). CPython's builtin codec has historically been inconsistent about those slots; this library always decodes them to `U+FFFD`.

The trade-off is symmetry. Because no cp1252 byte means `U+FFFD`, `encode()` refuses to encode `U+FFFD` — and also refuses any code point outside the cp1252 repertoire (e.g. Cyrillic, Devanagari). `decode()` is total over all 256 byte values; `encode()` is not total over all of Unicode. This is deliberate: a round trip `decode(encode(s)) == s` holds for every encodable string, and an unencodable string fails loudly rather than silently producing wrong bytes.

## The awkward edge

The five undefined cp1252 bytes decode to `U+FFFD`. If you feed one of those bytes in, you will get `U+FFFD` back out, and you will not be able to re-encode that `U+FFFD` to recover the original byte. There is no byte to recover — the slot is undefined. If you need byte-perfect round-tripping of arbitrary bytes, use Latin-1 (`iso-8859-1`) instead; cp1252 cannot offer that guarantee by definition.
