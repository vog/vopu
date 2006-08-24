"""VoPU -- Volker's Python Utilities.

This module contains various functions and classes which are very
useful for my daily work with Python.

---

Copyright (c) 2006  Volker Grabsch <vog@notjusthosting.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__version__ = "1.2"

import codecs


def UnicodeStream(stream, encoding="utf8"):
    """Stream wrapper which automatically encodes and decodes.

    Return a stream whose methods read(), write(), ... take and return
    only unicode objects. These are encoded to and decoded from the given
    stream using the given encoding.

    This is a simpler interface to the codecs package.

    Arguments:
      - stream -- wrapped byte stream
      - encoding -- encoding of stream (default: UTF-8)

    Examples:

    >>> import sys
    >>> ustream = UnicodeStream(sys.stdout)
    >>> ustream.write(u"abc")
    abc

    >>> import os
    >>> stream = os.tmpfile()
    >>> stream.write("abc")
    >>> stream.seek(0)
    >>> ustream = UnicodeStream(stream)
    >>> ustream.read()
    u'abc'
    """
    reader = codecs.getreader(encoding)
    writer = codecs.getwriter(encoding)
    return codecs.StreamReaderWriter(stream, reader, writer)


class StringStream(object):

    r"""Stream which writes into a byte string.

    Example:

    >>> stream = StringStream()
    >>> stream.content
    ''
    >>> stream.write("foo")
    >>> stream.content
    'foo'
    >>> stream.write("bar")
    >>> stream.content
    'foobar'
    >>> print >>stream, "spam"
    >>> stream.content
    'foobarspam\n'
    >>> str(stream) == stream.content
    True

    >>> stream.content = "new content"
    >>> str(stream) == stream.content
    True
    >>> print >>stream, "Z"
    >>> print >>stream, "Line2"
    >>> stream.content
    'new contentZ\nLine2\n'
    >>> str(stream) == stream.content
    True
    """

    def __init__(self, content=""):
        """Create a new StringStream.

        Arguments:
          - content -- initial content (default: "")

        Examples:

        >>> stream = StringStream()
        >>> stream.content
        ''

        >>> stream = StringStream("spam")
        >>> stream.content
        'spam'
        """
        self.content = content

    def write(self, str):
        """Write a string into this stream.

        That means, append the given string to this stream's content.

        Arguments:
          - str -- byte string to write into this stream
        """
        self.content += str

    def __str__(self):
        """Return the content of this stream.

        In other words, return the concatenation of all strings that
        have been written into this stream.
        """
        return self.content


def readlines(obj, encoding="utf8"):
    r"""Return an iterator that steps through the lines of obj.

    Line endings are preserved.

    Arguments:
      - obj -- byte string, byte stream or unicode object to read from
      - encoding -- encoding of obj (default: UTF-8)

    Examples:

    >>> obj = u"Line1\nLine2\nLine3"
    >>> for line in readlines(obj):
    ...     print repr(line)
    u'Line1\n'
    u'Line2\n'
    u'Line3'

    >>> obj = u"Line1\nLine2\nLine3\n"
    >>> for line in readlines(obj):
    ...     print repr(line)
    u'Line1\n'
    u'Line2\n'
    u'Line3\n'

    >>> obj = "Line1\nLine2\nLine3\n"
    >>> for line in readlines(obj):
    ...     print repr(line)
    u'Line1\n'
    u'Line2\n'
    u'Line3\n'

    >>> import os
    >>> stream = os.tmpfile()
    >>> stream.write("Line1\nLine2\nLine3\n")
    >>> stream.seek(0)
    >>> for line in readlines(obj):
    ...     print repr(line)
    u'Line1\n'
    u'Line2\n'
    u'Line3\n'
    """
    if isinstance(obj, basestring):
        if isinstance(obj, str):
            obj = obj.decode(encoding)
        return obj.splitlines(True)
    else:
        return UnicodeStream(obj, encoding)


def split_labeled_uri(labeleduri, default=u""):
    """Split a labeled URI into its URI and its label.

    If the labeled URI doesn't contain a label, return the default label.

    Arguments:
      - labeleduri -- unicode string containing the labeled URI
      - default -- fallback label (default: u"")

    Examples:

    >>> split_labeled_uri(u"http://www.google.com/ This is Google.")
    (u'http://www.google.com/', u'This is Google.')

    >>> split_labeled_uri(u"http://www.google.com/  \\t surrounding spaces ")
    (u'http://www.google.com/', u'surrounding spaces')

    >>> split_labeled_uri(u"http://www.google.com/ given label", u"default label")
    (u'http://www.google.com/', u'given label')

    >>> split_labeled_uri(u"http://www.google.com/", u"default label")
    (u'http://www.google.com/', u'default label')
    """
    parts = labeleduri.strip().split(u" ", 1)
    uri = parts[0].strip()
    try:
        label = parts[1].strip()
    except IndexError:
        label = default
    return uri, label


def camelcase(ustr, maxlen=None):
    """Convert a unicode string into CamelCase.

    When maxlen is not None, each word is truncated to the length maxlen.

    Arguments:
      - labeleduri -- unicode string to convert
      - maxlen -- maximum length of each word (default: None)

    Examples:

    >>> camelcase(u"Abc")
    u'Abc'
    >>> camelcase(u"abc")
    u'Abc'
    >>> camelcase(u"ABC")
    u'Abc'

    >>> camelcase(u"This is a text")
    u'ThisIsAText'
    >>> camelcase(u"This is a text", None)
    u'ThisIsAText'

    >>> camelcase(u"This is a text", 4)
    u'ThisIsAText'
    >>> camelcase(u"This is a text", 3)
    u'ThiIsATex'
    >>> camelcase(u"This is a text", 2)
    u'ThIsATe'
    >>> camelcase(u"This is a text", 1)
    u'TIAT'
    >>> camelcase(u"This is a text", 0)
    u''

    >>> camelcase(u"")
    u''
    """
    return u"".join(word[:maxlen].capitalize() for word in ustr.split())


class OrderedByCreation(object):

    """Base class for objects which are ordered by their creation time.

    Example:

    >>> a = OrderedByCreation()
    >>> b = OrderedByCreation()
    >>> c = OrderedByCreation()
    >>> a < b
    True
    >>> b < c
    True
    >>> all = [b, c, a]
    >>> all.sort()
    >>> all == [a, b, c]
    True
    """

    __counter = 0

    def __init__(self):
        """Create a new OrderedByCreation object."""
        self.__class__.__counter += 1
        self.__key = self.__class__.__counter

    def __cmp__(self, other):
        """Compare two OrderedByCreation objects by their creation time.

        Example:

        >>> a = OrderedByCreation()
        >>> b = OrderedByCreation()
        >>> c = OrderedByCreation()
        >>> cmp(a, b)
        -1
        >>> cmp(b, b)
        0
        >>> cmp(c, b)
        1
        """
        return cmp(self.__key, other.__key)


def _test():
    """Run all doc tests of this module."""
    import doctest
    import vopu
    return doctest.testmod(vopu)

if __name__ == "__main__":
    _test()
