# sps - SUSE Package Search
This little tool searches for packages in SUSE products, it's uses the open API's at scc.suse.com

```
./sps --help
Usage: sps [OPTIONS] COMMAND [ARGS]...

Options:
  --debug
  --help   Show this message and exit.

Commands:
  package  Search for packages
  product  Search for products
```

## Getting the product ID
Inorder to search for a package you have to have the product ID to specify in what product you want to seach for the specific package.
To get the product ID you can do a product search.
```
./sps product --help
Usage: sps product [OPTIONS] [PATTERN]

  Search for products

Options:
  --field [name|identifier|edition]
                                  Search PATTERN in this field,
                                  default=identifier
  --help                          Show this message and exit.
```
the default fielt to search in is *identifier*, but that can be overridden by the *--field* option.
If no search PATTERN is given, all products will be returned
Let's limit our package search to SLES 15 and x86_64 architecture
```
./sps product SLES/15
+------+------------------------------+---------+-------------------+---------+
| id   | Name                         | Edition | Identifier        | Arch    |
+------+------------------------------+---------+-------------------+---------+
| 1760 | SUSE Linux Enterprise Server | 15 SP1  | SLES/15.1/aarch64 | aarch64 |
| 1763 | SUSE Linux Enterprise Server | 15 SP1  | SLES/15.1/x86_64  | x86_64  |
| 1761 | SUSE Linux Enterprise Server | 15 SP1  | SLES/15.1/ppc64le | ppc64le |
| 1762 | SUSE Linux Enterprise Server | 15 SP1  | SLES/15.1/s390x   | s390x   |
| 1586 | SUSE Linux Enterprise Server | 15      | SLES/15/aarch64   | aarch64 |
| 1575 | SUSE Linux Enterprise Server | 15      | SLES/15/x86_64    | x86_64  |
| 1584 | SUSE Linux Enterprise Server | 15      | SLES/15/s390x     | s390x   |
| 1585 | SUSE Linux Enterprise Server | 15      | SLES/15/ppc64le   | ppc64le |
+------+------------------------------+---------+-------------------+---------+
```
The id for that product is **1575**

## Searching for a package
```
./sps package --help
Usage: sps package [OPTIONS] PATTERN

  Search for packages

Options:
  --product INTEGER  id of product to search in  [required]
  --help             Show this message and exit.
```

we need to specify the product id on where we want to search so if we do a search for all package containing the word *vim* and  do that for *SLES 15 x86_64* product, the syntax would be
```
./sps package --product 1575 vim 
+---------------------------+-------------------+-------------+--------+-----------------------------+
| Name                      | Version           | Release     | Arch   | Module(s)                   |
+---------------------------+-------------------+-------------+--------+-----------------------------+
| ghc-yi-keymap-vim         | 0.14.0            | bp150.1.3   | x86_64 | SUSE Package Hub            |
| ghc-yi-keymap-vim-devel   | 0.14.0            | bp150.1.3   | x86_64 | SUSE Package Hub            |
| gvim                      | 8.0.1568          | 3.20        | x86_64 | Desktop Applications Module |
| neovim                    | 0.3.1             | bp150.2.3.1 | x86_64 | SUSE Package Hub            |
| neovim-lang               | 0.3.1             | bp150.2.3.1 | noarch | SUSE Package Hub            |
| python2-neovim            | 0.3.1             | bp150.3.3.1 | noarch | SUSE Package Hub            |
| python3-neovim            | 0.3.1             | bp150.3.3.1 | noarch | SUSE Package Hub            |
| rtorrent-vim              | 0.9.6.g116        | bp150.2.5   | noarch | SUSE Package Hub            |
| texlive-context-vim       | 2017.133.svn37413 | 5.18        | noarch | Desktop Applications Module |
| vim                       | 8.0.1568          | 3.20        | x86_64 | Basesystem Module           |
| vim-bootstrap             | 1.0+git7b40d33    | bp150.2.6   | x86_64 | SUSE Package Hub            |
| vim-data                  | 8.0.1568          | 3.20        | noarch | Basesystem Module           |
| vim-data-common           | 8.0.1568          | 3.20        | noarch | Basesystem Module           |
| vim-icinga2               | 2.8.4             | bp150.1.3   | x86_64 | SUSE Package Hub            |
| vim-plugin-a              | 2.18              | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-ack            | 1.0.9             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-align          | 36.42             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-bufexplorer    | 7.2.8             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-calendar       | 2.4               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-colorschemes   | 1.0               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-colorsel       | 20110107          | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-conky          | 1.10.6            | 1.46        | x86_64 | Desktop Applications Module |
| vim-plugin-devhelp        | 3.26.1            | 2.38        | x86_64 | Development Tools Module    |
| vim-plugin-diffchanges    | 0.6.346dae2       | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-editorconfig   | 0.3.3             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-fugitive       | 2.2               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-gitdiff        | 2                 | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-gnupg          | 2.6               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-latex          | 20120125          | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-locateopen     | 1.3               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-matrix         | 1.10              | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-minibufexpl    | 6.3.2             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-multiplesearch | 1.3               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-neomutt        | 20180104          | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-NERDcommenter  | 2.3.0             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-NERDtree       | 4.2.0             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-powerline      | 2.6               | bp150.3.3.1 | noarch | SUSE Package Hub            |
| vim-plugin-project        | 1.4.1             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-quilt          | 0.9.7             | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-rails          | 4.4               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-searchcomplete | 1.1               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-showmarks      | 2.2               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-snipmate       | 0.83              | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-supertab       | 1.0               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-taglist        | 4.5               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-tlib           | 0.42              | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-tregisters     | 0.2               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-tselectbuffer  | 0.7               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-tselectfiles   | 0.10              | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-utl            | 2.0               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-vimwiki        | 2.1               | bp150.2.3   | noarch | SUSE Package Hub            |
| vim-plugin-zoomwin        | 24                | bp150.2.3   | noarch | SUSE Package Hub            |
+---------------------------+-------------------+-------------+--------+-----------------------------+
```



## Install in python virtual environment
You need to install the build_basis pattern inorder to compile PyCurl
```
python3 -m venv venv
source venv/bin/activate
sudo zypper in -t pattern devel_basis
sudo zypper in python3-devel
export PYCURL_SSL_LIBRARY=openssl
pip install -r requirements.txt
```

copy the sps shell-script to a location in your path (e.g. ~/bin or ~/.local/bin) and change the path to where you have the files and created the python virtual environment
if you want the bash completion you can add the following row to ~./bashrc
```bash
source <(sps completion bash)
```

