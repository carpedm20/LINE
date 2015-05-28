LINE Episode I: A New Hope
==========================

If you are a core pythonic programmer, you can jump into writing the code
right away! But if you are not familiar with Python, you should read this
tutorial first before proceeding to the more details of *line*. Now, this
manual will git you a quick introduction on how you can send a message and 
do other things with *line*


Part 1: Login and Pin authentication
------------------------------------

Let's start with login to LINE and pass through a pin authentication.

.. code-block:: python
   
   >>> from line import LineClient
   >>> client = LineClient("carpedm20@gmail.com", "xxxxxxxxxx")
   Enter PinCode '7390' to your mobile phone in 2 minutes
   >>> client = LineClient("carpedm20", "xxxxxxxxxx")
   Enter PinCode '9779' to your mobile phone in 2 minutes

.. warning::

   You will failed to login because of the request of LINE corporation. (I have to remove some codes) However, you can use this library by login with `authToken`. The instruction about `authToken` login is explained in bellow paragraphs.

As you can see, you can login by making a `LineClient` instance and pass your
email and password as parameters. If you have a NAVER account and link it to 
LINE account, you can login with your NAVER account! 

Then, you will see a `PinCode` which you have to put in to your mobile phone
to authenticate your `LineClinet` instance as a desktop Line client. This number
will be expired in 2 minutes, so don't be lazy!

If you enter your `Pincode` to your mobile phone, now you can see your `authToken`
which will notify your LINE session.

.. code-block:: python

   >>> authToken = client.authToken
   >>> print authToken
   DJg5VZTBdkjMCQOeodf4.9guiWkX1koTnwiGNVkacva.49blBzv5W9ex/2M06QQofByLxigMCAnnGfmTOAgY3wo=


With this `authToken`, you don't have to enter `Pincode` when you create a new
`LineClient` instance!

.. code-block:: python

   >>> client = LineClient(authToken=authToken)

You can save your authToken in cache like *redis* or something else!


.. Note::

    If the client will be expired after a specific time (I couldn't find a exact
    time yet), so you have to get a new `authToken` after it is expired.


Part 2: Profile and Contacts
----------------------------

Now, let's see your profile to check whether `PinCode` authentication was
successful or not.

.. code-block:: python

   >> profile = client.profile
   >> print profile
   <LineContact 김태훈>

You might want to send any `message` to your friend that you have succeeded
to login to LINE! But you have to choose which one to send a `message`.

.. code-block:: python

   >>> print client.contacts  # your friends
   [<LineContact 파랑봇> <LineContact 검정봇>]

Then, choose anyone to send a hello world message, and send it away!

.. code-block:: python

   >>> friend = client.contacts[0]
   >>> friend.sendMessage("hello world!")
   True

If you want to send an `image`, you can use `sendImage()` with specific path for image

.. code-block:: python

   >>> friend.sendImage("./image.jpg") # use your path for image to send
   True

Or you can use an URL for image to send any `image` to your friends with `sendImageWithURL()`!

.. code-block:: python

   >>> friend.sendImageWithURL("https://avatars3.githubusercontent.com/u/3346407?v=3&s=460")
   True

If you want to send a `sticker` (which is one of the most fun features of LINE!)

.. code-block:: python

   >>> friend.sendSticker() # send a default sticker
   True
   >>> friend.sendSticker(stickerId="13",stickerPackageId="1",stickerVersion="100")
   True

If you see `True` message, then it means message is successfully sended to your
friend. If you want to receive 10 recent messages:

.. code-block:: python

   >>> messages = friend.getRecentMessages(count=10)
   >>> print messages
   [LineMessage (contentType=NONE, sender=None, receiver=<LineContact 파랑봇>, msg="hello World!")]

I just make a one conversation with *파랑봇* so I only get one message with `getRecentMessages` method.


Part 3: Rooms and Groups
------------------------

There are two type of chat rooms in LINE, one is just a `room` with multiple users,
and the other is `group` which have more features then room. For examle, `group`
has its own name but `room` don't have any room for itself.

Now let's see a list of  `group` and `room` you are participated in.

.. code-block:: python

   >>> print client.groups
   [<LineGroup 하트 #4>, <LineGroup 검정 #1 (invited)>]
   >>> print client.rooms
   <LineRoom [<LineContact 파랑봇>]>, <LineRoom [<LineContact 파랑봇>, <LineContact 검정봇>]>]

In the case of `client.groups` you can see a word *(invited)* and this represent
that you are invited to a group but you didn't accep the invitation yet.
'#{number}' means the number of members in the specific group.
If you want to accept it:

.. code-block:: python

   >>> group = client.groups[1]
   >>> group.acceptGroupInvitation()
   True

Other methods are same as the case of `contact` like if you want to get a 
list of recent messages, use `getRecentMessages` method:

.. code-block:: python

   >>> messages = client.contacts[0].getRecentMessages(count=10)
   >>> messages = client.groups[0].getRecentMessages(count=15)

If you have too much groups and want to find a specific group with its `name`:

.. code-block:: python

   >>> group = client.getGroupByName('GROUP_NAME')
   >>> contact = client.getContactByName('CONTACT_NAME')

There are other methods in `contact`, `rooms` and `group` instances so I'll
recommend you to take a look at the :ref:`models <api/models>` section.

   
Part 4: Make your own bot
-------------------------

So, most of you may want to use *line* to make your LINE bot. I also started this
project to make a bot, so let's talk about how to make our own bot. Below code
is a basic structure of a LINE bot:

.. code-block:: python
   :linenos:
   :emphasize-lines: 12

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

One of the most important line is #12, and you might notice there is a new
method named `longPoll`. This method pull a list of operations which should
be handled by our LINE bot. There are various type of operations, but 
our interest might be `RECEIVE_MESSAGE` operation. This operation contain a new
message sent by other `contact`, `room` or `group`. So we can get a received 
`message` and its `sender` by 

.. code-block:: python

   sender   = op[0]
   receiver = op[1]
   message  = op[2]
