sps
========

CLI searching for packages in SUSE products.

Installing
----------

::
    pip install --user https://raw.githubusercontent.com/SweBarre/sps/dist/sps-0.1.0-py36-none-any.whl


Usage
-----

::
    sps --help
    usage: sps [-h] [--cache-file CACHE_FILE]
               {package,product,completion} [pattern]

    positional arguments:
      {package,product,completion}
                            command to run
      pattern               pattern to search for

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE, -C CACHE_FILE
                            cache file to use, (default:
                            /home/<username>/.cache/sps_products.json


List all products available

::

    $ sps product


To ave a local product cache in ``~/.cache/sps/products`` just run the following command

::

    $ sps product --update-cache

List products that matches a SLES15

::
    $ sps product SLES15


To search for packes just run ``sps package <PRODUCT NAME or PRODUCT ID> <PATTERN>``

::
    $ sps package SLES/15.1/x86_64 gvim
    +----------------+----------+---------+--------+-----------------------------+
    | Name           | Version  | Release | Arch   | Module                      |
    +----------------+----------+---------+--------+-----------------------------+
    | gvim           | 8.0.1568 | 5.3.1   | x86_64 | Desktop Applications Module |
    | gvim           | 8.0.1568 | 3.20    | x86_64 | Desktop Applications Module |
    | gvim-debuginfo | 8.0.1568 | 3.20    | x86_64 | Desktop Applications Module |
    +----------------+----------+---------+--------+-----------------------------+
    
    $ sps package 1763 gvim
    +----------------+----------+---------+--------+-----------------------------+
    | Name           | Version  | Release | Arch   | Module                      |
    +----------------+----------+---------+--------+-----------------------------+
    | gvim           | 8.0.1568 | 5.3.1   | x86_64 | Desktop Applications Module |
    | gvim           | 8.0.1568 | 3.20    | x86_64 | Desktop Applications Module |
    | gvim-debuginfo | 8.0.1568 | 3.20    | x86_64 | Desktop Applications Module |
    +----------------+----------+---------+--------+-----------------------------+

To get bash completion you can run ``sps completion bash`` and redirect it to a file that you source from your .bashrc or just run the following

::
    $ source <(sps completion bash)

If your have a local product cache you will get tab-completion for the product in package search

code-block::
    $ sps package <TAB> <TAB>
    CAASP/3.0/x86_64                 SLES/12.2/aarch64                SLES/15/aarch64
    --help                           SLES/12.2/ppc64le                SLES/15/ppc64le
    SLED/12.1/x86_64                 SLES/12.2/s390x                  SLES/15/s390x
    SLED/12.2/x86_64                 SLES/12.2/x86_64                 SLES/15/x86_64
    SLED/12.3/x86_64                 SLES/12.3/aarch64                SLES_SAP/12.1/ppc64le
    SLED/12.4/x86_64                 SLES/12.3/ppc64le                SLES_SAP/12.1/x86_64
    SLED/12/x86_64                   SLES/12.3/s390x                  SLES_SAP/12.2/ppc64le
    SLED/15.1/x86_64                 SLES/12.3/x86_64                 SLES_SAP/12.2/x86_64
    SLED/15.2/x86_64                 SLES/12.4/aarch64                SLES_SAP/12.3/ppc64le
    SLED/15/x86_64                   SLES/12.4/ppc64le                SLES_SAP/12.3/x86_64
    SLE-HPC/12.2/x86_64              SLES/12.4/s390x                  SLES_SAP/12.4/ppc64le
    SLE-HPC/12.3/aarch64             SLES/12.4/x86_64                 SLES_SAP/12.4/x86_64
    SLE-HPC/12.3/x86_64              SLES/12.5/aarch64                SLES_SAP/12.5/ppc64le
    SLE-HPC/12.4/aarch64             SLES/12.5/ppc64le                SLES_SAP/12.5/x86_64
    SLE-HPC/12.4/x86_64              SLES/12.5/s390x                  SLES_SAP/12/x86_64
    SLE-HPC/12.5/aarch64             SLES/12.5/x86_64                 SLES_SAP/15.1/ppc64le
    SLE-HPC/12.5/x86_64              SLES/12/ppc64le                  SLES_SAP/15.1/x86_64
    SLE_HPC/15.1/aarch64             SLES/12/s390x                    SLES_SAP/15.2/ppc64le
    SLE_HPC/15.1/x86_64              SLES/12/x86_64                   SLES_SAP/15.2/x86_64
    SLE_HPC/15.2/aarch64             SLES/15.1/aarch64                SLES_SAP/15/ppc64le
    SLE_HPC/15.2/x86_64              SLES/15.1/ppc64le                SLES_SAP/15/x86_64
    SLE_HPC/15/aarch64               SLES/15.1/s390x                  SUSE-Manager-Server/4.0/ppc64le
    SLE_HPC/15/x86_64                SLES/15.1/x86_64                 SUSE-Manager-Server/4.0/s390x
    SLE_RT/15.1/x86_64               SLES/15.2/aarch64                SUSE-Manager-Server/4.0/x86_64
    SLES/12.1/ppc64le                SLES/15.2/ppc64le                SUSE-Manager-Server/4.1/ppc64le
    SLES/12.1/s390x                  SLES/15.2/s390x                  SUSE-Manager-Server/4.1/s390x
    SLES/12.1/x86_64                 SLES/15.2/x86_64                 SUSE-Manager-Server/4.1/x86_64


Preparing for Development
-------------------------

1. Ensure ``pip`` and ``pipenv`` are installed
2. Clone repository: ``git clone https://github.com/SweBarre/sps.git``
3. ``cd`` into repository
4. Activate virtualenv: ``pipenv shell``
5. Fetch development dependencies ``make dev``



Running Tests
-------------

Run tests locally using ``make`` if virtualenv is active:

    code-block::

    $ make test

If virtualenv isn’t active then use:

::

    $ pipenv run make
