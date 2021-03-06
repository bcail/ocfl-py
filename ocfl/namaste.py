"""NAMASTE file support.

NAMASTE spec: http://www.cdlib.org/inside/diglib/namaste/namastespec.html

See also command line tool: http://github.com/mjgiarlo/namaste
"""
import os
import os.path
import re


def content_to_tvalue(content):
    """Safe and limited length tvalue from content.

    Return string will be at most 40 characters, trimmed of starting or ending
    whitespace, any input characters not word, dot, hyphen, underscore, colon
    will be converted to underscore.
    """
    content = content.strip()
    return re.sub(r'''[^\w\.\-:]''', '_', content[:40])


def find_namastes(d, dir, max=10):
    """Find NAMASTE files with tag d in dir, return list of Namaste objects.

    max sets a limit on the number of Namaste objects returned, a NamasteException
    will be raised if more than max files with tag d are found.
    """
    prefix = str(d) + '='
    namastes = []
    for filename in os.listdir(dir):
        if filename.startswith(prefix):
            if len(namastes) >= max:
                raise NamasteException("Found too many Namaste files with tag %s in %s" % (str(d), dir))
            namastes.append(Namaste(d, tvalue=filename[len(prefix):]))
    return namastes


def get_namaste(d, dir):
    """Find NAMASTE file with tag d in dir, return Namaste object.

    Raises NamasteException if not exaclty one.
    """
    namastes = find_namastes(d, dir, max=1)
    if len(namastes) != 1:
        raise NamasteException("Failed to find on Namaste file with tag %s in %s" % (str(d), dir))
    return namastes[0]


class NamasteException(Exception):
    """Class for exceptions from Namaste."""

    pass


class Namaste(object):
    """Class implementing NAMASTE specification."""

    def __init__(self, d=0, content='', tvalue=None, tr_func=content_to_tvalue):
        """Initialize Namaste object.

        Parameters:
            d - tag name, D in NAMASTE specification
            content - metadata content of NAMASTE file from which tvalue is derived
            tvalue - explicity set tvalue instead of deriving
            tr_func - function reference used to derive a tvalue from content,
                overriding default content_to_tvalue
        """
        self.d = d
        self.content = content
        self._tvalue = tvalue
        self._tr_func = tr_func

    @property
    def filename(self):
        """Filename of Namaste file."""
        return str(self.d) + '=' + self.tvalue

    @property
    def tvalue(self):
        """tvalue of Namaste file."""
        if self._tvalue is not None:
            return self._tvalue
        else:
            return self._tr_func(self.content)

    def write(self, dir):
        """Write NAMASTE file to dir.

        e.g.
            Namaste(0, 'ocfl_1.0').write(dir)
        """
        with open(os.path.join(dir, self.filename), 'w') as fh:
            fh.write(self.content + "\n")

    def check_content(self, dir):
        """Check that the file content is compatible with the tvalue based on tr_func, else raise NamasteException."""
        filepath = os.path.join(dir, self.filename)
        if self.tvalue == '':
            raise NamasteException("Cannot check Namaste file %s without tvalue being set!" % (filepath))
        if not os.path.isfile(filepath):
            raise NamasteException("Namaste file %s does not exist!" % (filepath))
        with open(filepath, 'r') as fh:
            content = fh.read()
        if self.tvalue != self._tr_func(content):
            raise NamasteException("Content of Namaste file %s doesn't match tvalue %s" % (filepath, self.tvalue))

    def content_ok(self, dir):
        """True is check_content() does not raise an exception."""
        try:
            self.check_content(dir)
        except Exception:
            return False
        return True
