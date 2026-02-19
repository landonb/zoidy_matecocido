zoidy_matecocido
================

An Ansible role to customize
`GNOME Shell <https://www.gnome.org/>`__
(or `MATE <https://mate-desktop.org/>`__)
keybindings, aka keyboard accelerators.

- I.e., those under ``/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/``.

Requirements
------------

GNOME Shell or MATE desktop environment.

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

History
-------

This project was originally created to customize MATE for the author's previous development environment, `Linux Mint 19 ‘Tara’ <https://linuxmint.com/>`__ running the `MATE <https://mate-desktop.org/>`__ desktop environment.

The author has since migrated to `Debian <https://www.debian.org/>`__ (starting at version 12; and GNOME Shell 44).

So this project is mostly MATE-related tasks.

But I still use a few tasks in this project to automatically manage
my GNOME Shell `custom keyboard shortcuts <https://help.gnome.org/gnome-help/keyboard-shortcuts-set.html#custom>`__.

License
-------

`GPLv3 <LICENSE>`__

