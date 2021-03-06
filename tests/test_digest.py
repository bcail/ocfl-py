"""Digest tests."""
import unittest
from ocfl.digest import file_digest


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_empty(self):
        """Create Digest object."""
        self.assertEqual(file_digest('tests/testdata/files/empty', 'md5'),
                         'd41d8cd98f00b204e9800998ecf8427e')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha1'),
                         'da39a3ee5e6b4b0d3255bfef95601890afd80709')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha256'),
                         'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha512'),
                         'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-512'),
                         '786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-384'),
                         'b32811423377f52d7862286ee1a72ee540524380fda1724a6f25d7978c6fd3244a6caf0498812673c5e05ef583825100')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-256'),
                         '0e5751c026e543b2e8ab2eb06099daa1d1e5df47778f7787faab45cdf12fe3a8')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'blake2b-160'),
                         '3345524abf6bbe1809449224b5972c41790b6cf2')
        self.assertEqual(file_digest('tests/testdata/files/empty', 'sha512-spec-ex'),
                         'cf83e1...a3e')
        self.assertRaises(Exception, file_digest, 'tests/testdata/files/empty', 'bad-digest-type')

    def test02_long(self):
        """Create Digest object for file with content."""
        self.assertEqual(file_digest('tests/testdata/files/hello_out_there.txt', 'md5'),
                         '9c7ec1389a61f1e15185bd976672bc63')
