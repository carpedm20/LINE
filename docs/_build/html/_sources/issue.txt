Known issue
===========

1. Garbage data with python Thrift
----------------------------------

If you use methods like `curve.ttypes.Location` which get or send double type data through *Thrift*, you might get some garbage values.

Thre reason of this error is that *Thrift 0.9.1* installed via *pip* has an issue with serialization&deserialization of double type using CompactProtocol as described in `here <https://issues.apache.org/jira/browse/THRIFT-1639>`__.

Below is a patch which is suggedsted by Wittawat Tantisiriroj (wtantisiriroj@gmail.com)

-- Patch --
~~~~~~~~~~~

.. code-block:: sh

    diff --git a/lib/py/src/protocol/TCompactProtocol.py b/lib/py/src/protocol/TCompactProtocol.py
    index cdec607..c34edb8 100644
    --- a/lib/py/src/protocol/TCompactProtocol.py
    +++ b/lib/py/src/protocol/TCompactProtocol.py
    @@ -250,7 +250,7 @@ def writeI64(self, i64):
    
      @writer
      def writeDouble(self, dub):
    -    self.trans.write(pack('!d', dub))
    +    self.trans.write(pack('<d', dub))
    
      def __writeString(self, s):
        self.__writeSize(len(s))
    @@ -383,7 +383,7 @@ def readBool(self):
      @reader
      def readDouble(self):
        buff = self.trans.readAll(8)
    -    val, = unpack('!d', buff)
    +    val, = unpack('<d', buff)
        return val
    
      def __readString(self):
