# vim:tw=0:ts=4:sw=4:et:norl:ft=python

# USAGE: Ansible loads this filter automatically when found in the playbook's
# ./filter_plugins/ directory.

# REFER: Erm, not really documented... See source for other filter examples:
#   https://github.com/search?q=repo%3Aansible%2Fansible+FilterModule&type=code
# - Where Ansible hardcode-expects 'FilterModule' class:
#   https://github.com/ansible/ansible/blob/c5ecb46c3f8/lib/ansible/plugins/loader.py#L1830
# - Here's official documentation, which doesn't mention 'FilterModule', etc.
#   https://docs.ansible.com/projects/ansible/latest/plugins/filter.html
#   https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_filters.html#playbooks-filters
# - Here are community docs that *do* mention conventions used below:
#   https://me.micahrl.com/blog/ansible-filter-pure-function/
#   https://www.dasblinkenlichten.com/creating-ansible-filter-plugins/

# MAYBE/2021-01-06 17:20: I just copied these from another filter...
# might not be necessary... or might be necessary for Python 2....
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError

# (lb): Just a note to self highlighting some filter behaviors,
# this one being that a filter can raise an error.
#
#  from ansible.errors import AnsibleFilterError

ANSIBLE_METADATA = {
    'metadata_version': '1.0.0',
    'status': ['preview'],
    'supported_by': 'community'
}


# ***

class FilterModule(object):
    ''' URI filter '''

    def filters(self):
        return {
            'to_gvim_keybinding_action': to_gvim_keybinding_action,
            # Another way to do it (lb: A note to self, b/c this my first filter!):
            #  'another_filter': self.b_filter,
        }

    # def b_filter(self, a_variable):
    #     a_new_variable = a_variable + ' says, "I've been filtered!"'
    #     return a_new_variable


# ***

# REFER: First arg is whatever's piped to the filter, e.g.,
# a simple string, or a dictionary object, etc.
# - The servername and user_home are added by our intermediate shim/decorator:
#     ansible/roles/zoidy_matecocido/tasks/keybinding-circus.yml @ 228
def to_gvim_keybinding_action(
    name_binding_actions,
    # ISOFF: See below: 'servername' obtained dynamically now;
    # but not removing arg. for now, emitting exception instead
    # if used.
    servername='',
    user_home='',
):
    """"""

    # (lb): I didn't figure out how to expandvars the return string, or send
    # it through the jinja2 filter, or however it'd be accomplished, that is:
    # - If a return string contains a {{ var }}, e.g., {{ ansible_facts['env']['HOME'] }},
    #   it will not be expanded after being returned from this filter function.
    # - As a work around, just have the caller pass it in.
    # - See also environment filter:
    #     from jinja2.filters import environmentfilter
    #     @environmentfilter
    #     def my_filter(environment, piped_input, optional_arg_1=None, ...):
    #         ...
    #   except I wasn't able to figure out how to use that to place the user
    #   home value... nor am I am even sure environmentfilter is meant to be
    #   used that way.
    # - Note that user_home probably os.path.expanduser('~')...
    #   except maybe when run over SSH on separate machines with
    #   separate users, then I'm not so sure.

    def _to_gvim_keybinding_action():
        # name_binding_actions is list of dict with 3 keys: name, binding, action.

        #  trace_msg = 'to_gvim_keybinding_action: --servername {} / len {}'.format(
        #      servername, len(name_binding_actions),
        #  )
        #  print(trace_msg)

        with_hydrated_actions = []
        for binding_def in name_binding_actions:
            # hydrated_action = binding_def['action']
            hydrated_action = hydrate_action(binding_def['file_path'])
            with_hydrated_action = {
                'name': binding_def['name'],
                'binding': binding_def['binding'],
                'action': hydrated_action,
            }
            with_hydrated_actions.append(with_hydrated_action)

        return with_hydrated_actions

    def hydrate_action(file_path):
        # OPTIONAL: We could enable row and line jumping, too.
        #           For now, not specified: \\\'\\\' \\\'\\\'.
        # CXREF: ~/.kit/sh/gvim-open-kindness/bin/gvim-open-kindness
        #
        # SAVVY/2024-06-06: Recently, gvim-open-kindness will pick the
        # active Gvim servername, if one is running, which makes it
        # easier for user to change their preferred servername without
        # having to repair all the keybindings. So prefer not setting.
        # - TL/DR: Prefer *not* setting servername.
        #
        # USYNC: CXREF: bin/sensible-gui-editor callers:
        # - 'gvim_open_kindness':
        #     depoxy/home/.hammerspoon/depoxy-hs.lua
        #   'to_gvim_keybinding_action':
        #     ansible/roles/zoidy_matecocido/filter_plugins/to_gvim_keybinding_action.py
        # - Callee:
        #     depoxy/bin/sensible-gui-editor
        #
        # CXREF: User env. determines if runs gvim or nvim (See:
        # GVIM_OPEN_PREFER_NVIM=true); if opens in current terminal
        # or GUI app (Neovide, MacVim, gVim, etc.); and (for nvim)
        # what socketname (path) to use. See:
        #   ~/.depoxy/running/home/.config/depoxy/depoxyrc
        #   ~/.local/state/depoxy/sensible-gui-editor.socketname
        #   ~/.kit/sh/gvim-open-kindness/bin/gvim-open-kindness
        if servername:
            # ISOFF/2026-08-09: Unused branch, AFAIK; but let's double-check.
            raise AnsibleError("Unexpected 'servername' passed to 'to_gvim_keybinding_action'")
        else:
            # INERT/FTREQ/2026-08-09: Decouple zoidy_matecocido from DepoXy:
            # - Make 'sensible-gui-editor' an installable dep?
            #   - E.g., install under ~/.local/bin/, and use instead
            #     of the ~/.depoxy/ambers/bin/ prefix.
            bash_cmd = (
                "'sh -c \\\""
                    "{user_home}/.depoxy/ambers/bin/sensible-gui-editor "
                        "\\\'{file_path}\\\';"
                "\\\"'"
            ).format(
                user_home=user_home,
                file_path=file_path,
            )
        return bash_cmd

    return _to_gvim_keybinding_action()

# ***
