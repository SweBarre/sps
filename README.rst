sps - SUSE P(roduct|ackage|atch) Search
========

CLI searching for packages in SUSE products.
It is a cli interface to the SUSE Customer Center search packages API https://scc.suse.com/packages

.. image:: https://asciinema.org/a/339205.svg
   :target: https://asciinema.org/a/339205

Installing
----------

::

    pip install --user https://github.com/SweBarre/sps/raw/master/dist/sps-0.2.0-py36-none-any.whl


Usage
-----

::

    $ sps --help
    usage: sps [-h] [--cache-file CACHE_FILE] [--cache-age CACHE_AGE] [--version]
               {package,product,completion,patchproduct} [pattern]

    positional arguments:
      {package,product,completion,patchproduct}
                            command to run
      pattern               pattern to search for

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE, -C CACHE_FILE
                            cache file to use, (default:
                            $HOME/.cache/sps_cache.json
      --cache-age CACHE_AGE, -a CACHE_AGE
                            Number of days before cache entry is flagged as old
      --version, -v         show program's version number and exit


Shell completion
---------------

To get bash completion you can run ``sps completion bash`` and redirect it to a file that you source from your .bashrc or just run the following

::

    $ source <(sps completion bash)



Product search
-------------

::

    $ sps product --help
    usage: sps [-h] [--cache-file CACHE_FILE] [--cache-age CACHE_AGE] [--version]
               [--update-cache] [--no-cache]
               [--sort-table {id,Name,Edition,Identifier,Arch}] [--no-borders]
               [--no-header]
               command [pattern]

    positional arguments:
      command               product related tasks
      pattern               pattern to search for

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE, -C CACHE_FILE
                            cache file to use, (default:
                            $HOME/.cache/sps_cache.json
      --cache-age CACHE_AGE, -a CACHE_AGE
                            Number of days before cache entry is flagged as old
      --version, -v         show program's version number and exit
      --update-cache, -u    Update the local product cache
      --no-cache, -N        Don't use the local cache
      --sort-table {id,Name,Edition,Identifier,Arch}, -S {id,Name,Edition,Identifier,Arch}
                            Sort output by column
      --no-borders, -n      Do not print borders
      --no-header, -H       Do not print headers


List all products

::

    $ sps product


To save a local product cache in ``~/.cache/sps/sps_cache.json`` just run the following command

::

    $ sps --update-cache product

List products that matches a SLES15

::

    $ sps product SLES15


Package search
--------------

::

    $ sps package --help
    usage: sps [-h] [--cache-file CACHE_FILE] [--cache-age CACHE_AGE] [--version]
               [--exact-match] [--sort-table {Name,Version,Release,Arch,Module}]
               [--no-borders] [--no-header]
               command product [pattern]

    positional arguments:
      command               package related tasks
      product               product id or identifier to search for packages in
      pattern               pattern to search for

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE, -C CACHE_FILE
                            cache file to use, (default:
                            $HOME/.cache/sps_cache.json
      --cache-age CACHE_AGE, -a CACHE_AGE
                            Number of days before cache entry is flagged as old
      --version, -v         show program's version number and exit
      --exact-match, -e     Only show where PATTERN matches exact
      --sort-table {Name,Version,Release,Arch,Module}, -S {Name,Version,Release,Arch,Module}
                            Sort output by column
      --no-borders, -n      Do not print borders
      --no-header, -H       Do not print headers



To search for packages just run ``sps package <PRODUCT NAME or PRODUCT ID> <PATTERN>``

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

    $ sps package SLES/15.1/x86_64 gvim --exact-match
    +------+----------+---------+--------+-----------------------------+
    | Name | Version  | Release | Arch   | Module                      |
    +------+----------+---------+--------+-----------------------------+
    | gvim | 8.0.1568 | 5.3.1   | x86_64 | Desktop Applications Module |
    | gvim | 8.0.1568 | 3.20    | x86_64 | Desktop Applications Module |
    +------+----------+---------+--------+-----------------------------+



If your have a local product cache you will get tab-completion for the product in package search

::


    $ sps package <TAB> <TAB>
    CAASP/3.0/x86_64                 SLES/12.2/ppc64le                SLES/15/ppc64le
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
    SLES/12.2/aarch64                SLES/15/aarch64


Patch Products
--------------

Searching for patches uses a different API and also different product names, to list products to search for patches in you can use

::

    $ sps patchproduct --help
    usage: sps [-h] [--cache-file CACHE_FILE] [--cache-age CACHE_AGE] [--version]
               [--no-cache] [--update-cache] [--sort-table {Name,Version,Arch,id}]
               [--no-borders] [--no-header]
               command [pattern]

    positional arguments:
      command               Patch product related tasks
      pattern               pattern to search for

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE, -C CACHE_FILE
                            cache file to use, (default:
                            $HOME/.cache/sps_cache.json
      --cache-age CACHE_AGE, -a CACHE_AGE
                            Number of days before cache entry is flagged as old
      --version, -v         show program's version number and exit
      --no-cache, -N        Don't use the local cache
      --update-cache, -u    Update the local patch product cache
      --sort-table {Name,Version,Arch,id}, -S {Name,Version,Arch,id}
                            Sort output by column
      --no-borders, -n      Do not print borders
      --no-header, -H       Do not print headers


To seach for patch products 

::

    $ sps patchproduct "Web and Script"
    +--------------------------+---------+---------+
    | Name                     | Version | Arch    |
    +--------------------------+---------+---------+
    | Web and Scripting Module | 12      | aarch64 |
    | Web and Scripting Module | 12      | ppc64le |
    | Web and Scripting Module | 12      | s390x   |
    | Web and Scripting Module | 12      | x86_64  |
    | Web and Scripting Module | 15      | aarch64 |
    | Web and Scripting Module | 15      | ppc64le |
    | Web and Scripting Module | 15      | s390x   |
    | Web and Scripting Module | 15      | x86_64  |
    | Web and Scripting Module | 15 SP1  | aarch64 |
    | Web and Scripting Module | 15 SP1  | ppc64le |
    | Web and Scripting Module | 15 SP1  | s390x   |
    | Web and Scripting Module | 15 SP1  | x86_64  |
    | Web and Scripting Module | 15 SP2  | aarch64 |
    | Web and Scripting Module | 15 SP2  | ppc64le |
    | Web and Scripting Module | 15 SP2  | s390x   |
    | Web and Scripting Module | 15 SP2  | x86_64  |
    +--------------------------+---------+---------+


To save a local patch product cache in ``~/.cache/sps/sps_cache.json`` just run the following command

::

    $ sps --update-cache patchproduct


Searching for patches
---------------------

::

    $ sps patch --help
    usage: sps [-h] [--cache-file CACHE_FILE] [--cache-age CACHE_AGE] [--version]
               [--severity {all,low,moderate,important,critical}]
               [--only-security-patches] [--date-from DATE_FROM]
               [--date-to DATE_TO] [--page PAGE]
               [--sort-table {Severity,Name,Product,Arch,id,Released}]
               [--product PRODUCT] [--arch ARCH]
               [--product-version PRODUCT_VERSION] [--detail] [--no-borders]
               [--no-header]
               command [pattern]

    positional arguments:
      command               Patch related tasts
      pattern               search by CVE, patch name, keywords

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE, -C CACHE_FILE
                            cache file to use, (default:
                            $HOME/.cache/sps_cache.json
      --cache-age CACHE_AGE, -a CACHE_AGE
                            Number of days before cache entry is flagged as old
      --version, -v         show program's version number and exit
      --severity {all,low,moderate,important,critical}, -e {all,low,moderate,important,critical}
                            search for patches with this severity level
      --only-security-patches, -o
                            only search for security patches
      --date-from DATE_FROM, -f DATE_FROM
                            search for patches starting from date YYYY-m-d
                            (2020-6-29)
      --date-to DATE_TO, -t DATE_TO
                            search for patches ending at date YYYY-m-d (2020-6-29)
      --page PAGE, -p PAGE  page number in search result to display
      --sort-table {Severity,Name,Product,Arch,id,Released}, -S {Severity,Name,Product,Arch,id,Released}
                            Sort output by column
      --product PRODUCT, -P PRODUCT
                            Product to limit the search to, spaces in product name
                            replaced with underscore
      --arch ARCH, -A ARCH  Architecture to limit the search to
      --product-version PRODUCT_VERSION, -V PRODUCT_VERSION
                            Version to limit the search to, spaces replaced with
                            underscore
      --detail, -d          Show detailed patch information
      --no-borders, -n      Do not print borders
      --no-header, -H       Do not print headers


You can search by CVE, patch name and keywords, if you hit more than 500 matches you will be displayed with a warning asking you to narrow down the search, use the options to narrow the search criteria further.

::

    $ sps patch CVE-2017-9107

    Page 1/4	 Hits: 38
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | Severity  | Name                     | Product                                                  | Arch    | id                                     | Released   |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Server ESPOS 12 SP3                | aarch64 | SUSE-SLE-SERVER-12-SP3-ESPOS-2020-1612 | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Server LTSS 12 SP2                 | ppc64le | SUSE-SLE-SERVER-12-SP2-2020-1612       | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Server for SAP Applications 12 SP2 | ppc64le | SUSE-SLE-SAP-12-SP2-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Server for SAP Applications 12 SP3 | ppc64le | SUSE-SLE-SAP-12-SP3-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Software Development Kit 12 SP4    | aarch64 | SUSE-SLE-SDK-12-SP4-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Software Development Kit 12 SP4    | ppc64le | SUSE-SLE-SDK-12-SP4-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Software Development Kit 12 SP4    | s390x   | SUSE-SLE-SDK-12-SP4-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Software Development Kit 12 SP5    | aarch64 | SUSE-SLE-SDK-12-SP5-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Software Development Kit 12 SP5    | ppc64le | SUSE-SLE-SDK-12-SP5-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+
    | important | Security update for adns | SUSE Linux Enterprise Software Development Kit 12 SP5    | s390x   | SUSE-SLE-SDK-12-SP5-2020-1612          | 2020-06-12 |
    +-----------+--------------------------+----------------------------------------------------------+---------+----------------------------------------+------------+

To display the patch details use the --detail option

::

    $ sps patch SUSE-SLE-SAP-12-SP3-2020-1612 --detail
    Detailed patch information
    ---------------------------------------------------------------------------
    Name:		Security update for adns
    Id:		SUSE-SLE-SAP-12-SP3-2020-1612
    Severity:	important
    Released:	2020-06-12
    Details:
    This update for adns fixes the following issues:
    
    - CVE-2017-9103,CVE-2017-9104,CVE-2017-9105,CVE-2017-9109: Fixed an issue in local recursive resolver
    which could have led to remote code execution (bsc#1172265).
    - CVE-2017-9106: Fixed an issue with upstream DNS data sources which could have led to denial of
    service (bsc#1172265).
    - CVE-2017-9107: Fixed an issue when quering domain names which could have led to denial of service (bsc#1172265).
    - CVE-2017-9108: Fixed an issue which could have led to denial of service (bsc#1172265).
    References
        bugzilla: 
                  1172265
        cve     : 
                  CVE-2017-9107 CVE-2017-9108 CVE-2017-9105 CVE-2017-9103 CVE-2017-9109
                  CVE-2017-9106 CVE-2017-9104
    Products: SUSE Linux Enterprise Server for SAP Applications 12 SP3
    Architecture: ppc64le
    Packages: 
              libadns1-1.4-103.3.1.ppc64le.rpm adns-1.4-103.3.1.src.rpm
    Detailed patch information
    ---------------------------------------------------------------------------
    Name:		Security update for adns
    Id:		SUSE-SLE-SAP-12-SP3-2020-1612
    Severity:	important
    Released:	2020-06-12
    Details:
    This update for adns fixes the following issues:
    
    - CVE-2017-9103,CVE-2017-9104,CVE-2017-9105,CVE-2017-9109: Fixed an issue in local recursive resolver
    which could have led to remote code execution (bsc#1172265).
    - CVE-2017-9106: Fixed an issue with upstream DNS data sources which could have led to denial of
    service (bsc#1172265).
    - CVE-2017-9107: Fixed an issue when quering domain names which could have led to denial of service (bsc#1172265).
    - CVE-2017-9108: Fixed an issue which could have led to denial of service (bsc#1172265).
    References
        bugzilla: 
                  1172265
        cve     : 
                  CVE-2017-9107 CVE-2017-9108 CVE-2017-9105 CVE-2017-9103 CVE-2017-9109
                  CVE-2017-9106 CVE-2017-9104
    Products: SUSE Linux Enterprise Server for SAP Applications 12 SP3
    Architecture: x86_64
    Packages: 
              libadns1-1.4-103.3.1.x86_64.rpm adns-1.4-103.3.1.src.rpm
    Page 1/1	 Hits: 2



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

::

    $ make test

If virtualenv isn’t active then use:

::

    $ pipenv run make
