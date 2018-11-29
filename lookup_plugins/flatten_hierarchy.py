# (c) 2013, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  lookup: Select a random license key from a file and remove it from future lookups
  author: Tim Rupp <caphrim007@gmail.com>
  version_added: 2.8
  short_description: Return random license from list
  description:
    - Flattens a list containing a hierarchy of resources.
    - The returned list is ordered so that parents always appear before their children.
      This results in a list that can be provided to an F5 Ansible module which can then
      correctly loop over the resources ensuring that they are created in the correct
      order.
"""

EXAMPLES = """
- name: Flatten list of HTTP Monitors
  set_fact:
    ordered_monitors: "{{ lookup('flatten_hierarchy', root='/Common/http', items=raw_monitors, name_key='MonitorName', parent_key='Parent') }}"
"""

RETURN = """
  _terms:
    description:
      - random item
"""

from anytree import AnyNode
from anytree import LevelOrderIter

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):
        super(LookupModule, self).__init__(loader, templar, **kwargs)

    def run(self, terms, variables=None, **kwargs):
        """
    - name: /Common/origin-sng.mobile.walmart.com-HTTP-monitor
      parent: /Common/wmt-default-http-monitor
    - name: /Common/torbit_health_ECV_80-monitor
      parent: /Common/wmt-default-http-monitor
    - name: /Common/torbit_health_ECV_80-monitor
      parent: /Common/wmt-default-http-monitor
    - name: /Common/wmt-default-http-monitor
      parent: /Common/http


        :param terms:
        :param variables:
        :param kwargs:
        :return:
        """
        root = kwargs.pop('root', None)  # /Common/http
        items = kwargs.pop('items', None)  # List of items to sort
        name_key = kwargs.pop('name_key', 'name')  # Key that identifies the name of the item
        parent_key = kwargs.pop('parent_key', 'parent')  # Key that identifies the parent of the item

        # Contains a list of nodes
        #
        # A node is an object with an ``id``, a ``parent`` and a series of
        # attributes which are taken from the entries in the ``items`` list
        # provided to this lookup
        nodes = []

        if root is None:
            raise AnsibleError("No 'root' was specified")

        # A base root must be created so that we can assign items in the
        # list to *something*. The root is the base parent of the ``items``
        # in the list.
        #
        # For example, if you want to order HTTP Monitors, then the root
        # would be ``/Common/http`` because this is the base parent class
        # for **all** HTTP monitors.
        #
        r = AnyNode(id=root)

        if items is None:
            return []

        # Populate the list of nodes
        for item in items:
            name = item.get(name_key, None)
            if name is None:
                raise AnsibleError("No 'name' key found in the current item.")

            # Create a generic node which uses the ``root`` as the default parent
            #
            # Correct parenting will be performed in the next loop. This process
            # is broken into two loops because we cannot know at this time what
            # the parent node is because not all parents have been put into nodes.
            #
            # We will only have a complete list of nodes once this loop here finishes.
            #
            node = AnyNode(id=name, parent=r, **item)
            nodes.append(node)

        for x in nodes:
            parent = getattr(x, parent_key, None)
            if parent is None:
                continue

            # Find the correct parent, or default to the root
            p = next((node for node in nodes if node.id == parent), r)

            # Update the parent so that it is correct
            x.parent = p

        ret = []

        # Flatten the tree so that the dependencies are correctly ordered.
        #
        # This will produce a list such that parents will always come before
        # the children they are parents of.
        #
        # The end result here is that you have a list that you can give to
        # Ansible which will always create resources in the correct order.
        nodes = [node for node in LevelOrderIter(r) if node.id != root]

        # Cleans up the list of nodes
        #
        # The lookup expects that a list of dictionaries be returned. Currently,
        # we have a list of AnyNode objects.
        #
        # Therefore, we need to convert these objects to plain-old-dictionaries.
        # Part of this process is removing some of the attrs that are specific
        # to the AnyNode object.
        #
        for node in nodes:
            tmp = node.__dict__
            tmp.pop('_NodeMixin__children', None)
            tmp.pop('_NodeMixin__parent', None)

            # Appending will correctly maintain the order of the parents
            ret.append(tmp)
        return ret
