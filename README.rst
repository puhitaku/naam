NAAM
====

*No Argparse Any More.*

Don’t google argparse just take some NAAM
-----------------------------------------

-  I forget how to use argparse every time I make utilities
-  10+ lines for just parsing arguments? No way!
-  There should be a super pythonic way to parse arguments!!!!
-  `I love Kizuna Ai. <https://www.youtube.com/watch?v=COXCojRKbk8>`__

Install
-------

``pip install naam``

How to use it
-------------

Just decorate your main function like ``@naam.bind_args`` and execute
it!

Example
-------

Here’s a code (placed in examples/optional.py):

.. code:: python

    from naam import bind_args


    @bind_args
    def hello(first_name, last_name=None):
        msg = 'Hello world! My name is %s.'
        if last_name is None:
            print(msg % first_name)
        else:
            print(msg % '{} {}'.format(first_name, last_name))


    hello()

With empty arguments, this outputs:

::

    Usage: optional.py [-l LAST_NAME | --last_name LAST_NAME] FIRST_NAME

With arguments, this outputs like:

::

    $ python optional.py Miku
    Hello world! My name is Miku.

    $ python optional.py Miku --last_name Hatsune
    Hello world! My name is Miku Hatsune.

    $ python optional.py Miku -l Hatsune
    Hello world! My name is Miku Hatsune.

Prerequisites
-------------

No dependencies. Works on Python 3.x (Built on Python 3.6.2).

Features I crave
----------------

-  Type casting for type-annotated args

