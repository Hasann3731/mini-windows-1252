import unittest

from mini_windows_1252 import decode, encode, ENCODING_NAME


class TestDecode(unittest.TestCase):
    def test_empty_bytes_returns_empty_str(self):
        self.assertEqual(decode(b""), "")

    def test_ascii_passthrough(self):
        self.assertEqual(decode(b"Hello, world!"), "Hello, world!")

    def test_all_256_code_points_are_defined(self):
        # decode must be total over every byte value 0x00..0xFF.
        all_bytes = bytes(range(256))
        result = decode(all_bytes)
        self.assertEqual(len(result), 256)
        # No None, no exceptions — every slot produced a character.
        for ch in result:
            self.assertIsInstance(ch, str)

    def test_known_upper_block_mappings(self):
        self.assertEqual(decode(b"\x80"), "\u20AC")  # EURO SIGN
        self.assertEqual(decode(b"\x93"), "\u201C")  # LEFT DOUBLE QUOTATION
        self.assertEqual(decode(b"\x94"), "\u201D")  # RIGHT DOUBLE QUOTATION
        self.assertEqual(decode(b"\x96"), "\u2013")  # EN DASH
        self.assertEqual(decode(b"\x97"), "\u2014")  # EM DASH
        self.assertEqual(decode(b"\x99"), "\u2122")  # TRADE MARK

    def test_latin1_block_identity(self):
        # 0xA0..0xFF must match ISO-8859-1.
        for b in range(0xA0, 0x100):
            self.assertEqual(decode(bytes([b])), chr(b))

    def test_undefined_slots_become_replacement_character(self):
        for raw in (0x81, 0x8D, 0x8F, 0x90, 0x9D):
            self.assertEqual(decode(bytes([raw])), "\uFFFD")

    def test_bytearray_accepted(self):
        self.assertEqual(decode(bytearray(b"ABC")), "ABC")

    def test_integer_input_rejected(self):
        with self.assertRaises(TypeError):
            decode(0x80)

    def test_str_input_rejected(self):
        with self.assertRaises(TypeError):
            decode("not bytes")


class TestEncode(unittest.TestCase):
    def test_empty_str_returns_empty_bytes(self):
        self.assertEqual(encode(""), b"")

    def test_ascii_round_trips(self):
        s = "Hello, world!"
        self.assertEqual(encode(s), s.encode("ascii"))

    def test_upper_block_round_trips(self):
        cases = [
            ("\u20AC", b"\x80"),  # EURO
            ("\u201C", b"\x93"),  # LEFT DOUBLE QUOTATION
            ("\u201D", b"\x94"),  # RIGHT DOUBLE QUOTATION
            ("\u2013", b"\x96"),  # EN DASH
            ("\u2014", b"\x97"),  # EM DASH
            ("\u2122", b"\x99"),  # TRADE MARK
            ("\u0152", b"\x8C"),  # LATIN CAPITAL LIGATURE OE
            ("\u0153", b"\x9C"),  # LATIN SMALL LIGATURE OE
            ("\u0178", b"\x9F"),  # LATIN CAPITAL LETTER Y WITH DIAERESIS
        ]
        for ch, expected in cases:
            with self.subTest(ch=ch):
                self.assertEqual(encode(ch), expected)

    def test_latin1_block_round_trips(self):
        for cp in range(0xA0, 0x100):
            self.assertEqual(encode(chr(cp)), bytes([cp]))

    def test_replacement_character_not_encodable(self):
        # U+FFFD appears in our decode table for the five undefined slots,
        # but it is NOT a real cp1252 character — encode must refuse it.
        with self.assertRaises(ValueError):
            encode("\uFFFD")

    def test_non_cp1252_character_rejected(self):
        # Cyrillic A is not in cp1252.
        with self.assertRaises(ValueError):
            encode("\u0410")

    def test_bytes_input_rejected(self):
        with self.assertRaises(TypeError):
            encode(b"not a str")

    def test_integer_input_rejected(self):
        with self.assertRaises(TypeError):
            encode(0x80)


class TestRoundTrip(unittest.TestCase):
    def test_all_encodable_code_points_round_trip(self):
        # Build the set of every code point our encode accepts by walking the
        # decode table; this guarantees we test exactly what we implement.
        all_bytes = bytes(range(256))
        decoded = decode(all_bytes)
        # For every byte that does NOT map to U+FFFD, decode -> encode must
        # recover the original byte.
        for b in range(256):
            ch = decoded[b]
            if ch == "\uFFFD":
                continue  # intentionally not encodable
            self.assertEqual(encode(ch), bytes([b]))

    def test_mixed_string_round_trip(self):
        s = "Price: \u20AC5, \u201Cquoted\u201D \u2014 end."
        self.assertEqual(decode(encode(s)), s)


class TestEncodingName(unittest.TestCase):
    def test_encoding_name_value(self):
        # Documented constant; keep it pinned so downstream code can rely on it.
        self.assertEqual(ENCODING_NAME, "windows-1252")


if __name__ == "__main__":
    unittest.main()
