"""VoPU -- Volker's Python Utilities

(C) 2006  Volker Grabsch <vog@notjusthosting.com>
"""

__version__ = "1.0"

import codecs


def UnicodeStream(stream, encoding="utf8"):
    """Stream wrapper which automatically encodes and decodes.

    Return a stream whose methods read(), write(), ... take and return
    only unicode objects. These are encoded to and decoded from the given
    stream using the given encoding.

    Arguments:
    stream -- wrapped byte stream
    encoding -- encoding of stream (default: UTF-8)

    Example:
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


class StringStream:

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
    >>> print >>stream, "s"
    >>> print >>stream, "Line2"
    >>> stream.content
    'new contents\nLine2\n'
    >>> str(stream) == stream.content
    True
    """

    def __init__(self, content=""):
        """Create a new StringStream.

        Arguments:
        content -- initial content (default: "")

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
        str -- byte string to write into this stream
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
    obj -- byte string, byte stream or unicode object to read from
    encoding -- encoding of obj (default: UTF-8)

    Examples:
    >>> obj = u"Line1\nLine2\nLine3\n"
    >>> tuple(readlines(obj))
    (u'Line1\n', u'Line2\n', u'Line3\n')

    >>> obj = "Line1\nLine2\nLine3\n"
    >>> tuple(readlines(obj))
    (u'Line1\n', u'Line2\n', u'Line3\n')

    >>> import os
    >>> stream = os.tmpfile()
    >>> stream.write(obj)
    >>> stream.seek(0)
    >>> tuple(readlines(stream))
    (u'Line1\n', u'Line2\n', u'Line3\n')
    """
    if isinstance(obj, basestring):
        if isinstance(obj, str):
            obj = obj.decode(encoding)
        return obj.splitlines(True)
    else:
        return UnicodeStream(obj, encoding)


def split_labeled_uri(labeleduri, default=u""):
    """split a labeled URI into its URI and its label.

    Examples:
    >>> split_labeled_uri(u"http://www.google.com/ This is Google.")
    (u'http://www.google.com/', u'This is Google.')

    >>> split_labeled_uri(u"http://www.google.com/\\t  leading and trailing spaces ")
    (u'http://www.google.com/', u'leading and trailing spaces')
    """
    parts = labeleduri.strip().split(u" ", 1)
    uri = parts[0].strip()
    try:
        label = parts[1].strip()
    except IndexError:
        label = default
    return uri, label


def camelcase(ustr, maxlen=None):
    """convert a unicode string into CamelCase.

    If maxlen is not None, it specifies the maximum length of each word.

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


def _test():
    import doctest
    import vopu
    return doctest.testmod(vopu)

if __name__ == "__main__":
    _test()
