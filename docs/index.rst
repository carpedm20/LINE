LINE manual
===========



Introduction
------------

*line* is a python library that allow you to send and receive a LINE message.
With *line* you can use LINE on any systems like Ubuntu or make your owb 
LINE bot which will automatically reply for your message!

Enjoy *line* and *May the LINE be with you...*

.. warning::

   Some codes are removed because of the request of LINE corporation. (2014.08.08)

Key Features
------------

* login to LINE server
* get a list of `contact`, `group` or chat `room`
* send and receive a `message` or `sticker`
* invite, join or leave a `group` or `room`
* `longPoll` method which will allow you to make a LINE bot easily


Todo
----

* Sending a Image
* More usable methods and objects


Installation
------------

First, you need to install **Apache Thrift**. Install instructions are here_. (This might take some time...)

.. _here: http://thrift.apache.org/docs/install/

Next:

.. code-block:: sh

   $ pip install line

Or, you can use:

.. code-block:: sh

    $ easy_install line

Or, you can also install manually:

.. code-block:: sh

    $ git clone git://github.com/carpedm20/line.git
    $ cd LINE
    $ python setup.py install


API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   tutorial

   api/client
   api/models
   api/api

   issue

Indices and tables
------------------

* :ref:`search`


Echo bot example
----------------

.. code-block:: python

   from line import LineClient, LineGroup, LineContact

   try:
      client = LineClient("ID", "PASSWORD")
      #client = LineClient(authToken="AUTHTOKEN")
   except:
      print "Login Failed"

   while True:
      op_list = []

      for op in client.longPoll():
         op_list.append(op)

      for op in op_list:
         sender   = op[0]
         receiver = op[1]
         message  = op[2]

         msg = message.text
         receiver.sendMessage("[%s] %s" % (sender.name, msg))

License
-------

Source codes are distributed under BSD license.

Author
------

Taehoon Kim / `@carpedm20 <http://carpedm20.github.io/about/>`_
