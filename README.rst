sps
========

CLI searching for packages in SUSE products.

Preparing for Development
-------------------------

1. Ensure ``pip`` and ``pipenv`` are installed
2. Clone repository: ``git clone xxx@xxxxxxx.xx``
3. ``cd`` into repository
4. Activate virtualenv: ``pipenv shell``
5. Fetch development dependencies ``make dev``

Usage
-----

::
    sps --help
    Usage: sps [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      completion  Completion for shells
      package     Search for packages
      product     Search for products


List all products available

::

    $ sps product


Save a local product cache in ``~/.cache/sps/products``

::

    $ sps product --update-cache

List products that matches a SLES15

::
    $ sps product SLES15


Running Tests
-------------

Run tests locally using ``make`` if virtualenv is active:

::

    $ make

If virtualenv isn’t active then use:

::

    $ pipenv run make
