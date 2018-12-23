zoidy_matecocido
================

An Ansible role to customize MATE on one Developer's
`Linux Mint 19 ‘Tara’ <https://linuxmint.com/edition.php?id=256>`__
(`Ubuntu 18.04 <http://releases.ubuntu.com/18.04/>`__)
-
`MATE <https://mate-desktop.org/>`__
development machine.

Requirements
------------

A fresh install of MATE.

Role Variables
--------------

Before and after configuring MATE, this role will create dump files
of the current settings on the host machine(s) in::

  ~/Documents/zoidy_matecocido/

Example Playbook
----------------

It's simple to run the role from a playbook::

  - hosts: servers
    roles:
       - role: zoidy_matecocido

License
-------

`GPLv3 <LICENSE>`__

