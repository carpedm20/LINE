LineClient
==========

Introduction
------------

This is the most important class to use LINE with python. You have to make an
instance of `LineClient` first and have to give your `id` and `password` as a
parameters to login to LINE server. Then you should enter `PinCode` to pass 
through `PinCode` authentication

.. code-block:: python

   >>> from line import LineClient
   >>> client = LineClient("carpedm20@gmail.com", "xxxxxxxxxx")
   Enter PinCode '7390' to your mobile phone in 2 minutes
   >>> client = LineClient("carpedm20", "xxxxxxxxxx")
   Enter PinCode '9779' to your mobile phone in 2 minutes

With `authToken` of your line instance, you don't have to enter `Pincode`
everytime when you create a new `LineClient` instance.

.. code-block:: python

   >>> client = LineClient(authToken=authToken) # login with authToken


LineClient
----------

.. autoclass:: line.LineClient
    :members:
