# vim:tw=0:ts=4:sw=4:et:norl:ft=python

# USAGE: Ansible loads this filter automatically when found in the playbook's
# filter_plugins/ directory. Call it to process MATE actions so your group_vars
# file can be more readable.

# MAYBE/2021-01-06 17:20: I just copied these from another filter...
# might not be necessary... or might be necessary for Python 2....
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# (lb): Just a note to self highlighting some filter behaviors,
# this one being that a filter can raise an error.
#
#  from ansible.errors import AnsibleFilterError

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
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

def to_gvim_keybinding_action(name_binding_actions, servername='SAMPI', user_home=''):
    """"""

    # (lb): I didn't figure out how to expandvars the return string, or send
    # it through the jinja2 filter, or however it'd be accomplished, that is:
    # - If a return string contains a {{ var }}, e.g., {{ ansible_env.HOME }},
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
        bash_cmd = (
            "'{user_home}/.local/bin/bash -c \\\""
                "{user_home}/.local/bin/gvim "
                    "--servername {servername} "
                    "--remote-silent {file_path} "
                "&& xdotool search "
                    "--name {servername} "
                    "windowactivate "
                "&& wmctrl -b add,sticky -r {servername}"
            "\\\"'"
        ).format(
            user_home=user_home,
            file_path=file_path,
            servername=servername,
        )
        return bash_cmd

    return _to_gvim_keybinding_action()

# ***

