#! /usr/bin/env python3
import collections
import logging
import socket
import json


from ops.charm import CharmBase

from ops.main import main

from ops.framework import (
    Object,
    ObjectEvents,
    StoredState,
)


logger = logging.getLogger()


def dict_keys_without_hyphens(a_dict):
    """Return the a new dict with underscores instead of hyphens in keys.
    https://github.com/juju/charm-helpers/blob/f9c06a96b0d1587a1c94d4d398efde8a403026eb/charmhelpers/contrib/templating/contexts.py#L31,L34
    """
    return dict(
        (key.replace('-', '_'), val) for key, val in a_dict.items())


def get_partitions(node_data):
    part_dict = collections.defaultdict(dict)
    for node in node_data:
        part_dict[node['partition']].setdefault('hosts', [])
        part_dict[node['partition']]['hosts'].append(node['hostname'])
        part_dict[node['partition']]['default'] = node['default']
    return dict(part_dict)


class RequirerRelationEvents(ObjectEvents):
    """Requirer Relation Events"""


class TestingRequirerRelation(Object):

    on = RequirerRelationEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)

        self._relation_name = relation_name
        self.hostname = socket.gethostname()

        self.framework.observe(
            charm.on[self._relation_name].relation_created,
            self._on_relation_created
        )

        self.framework.observe(
            charm.on[self._relation_name].relation_joined,
            self._on_relation_joined
        )

        self.framework.observe(
            charm.on[self._relation_name].relation_changed,
            self._on_relation_changed
        )

        self.framework.observe(
            charm.on[self._relation_name].relation_departed,
            self._on_relation_departed
        )

        self.framework.observe(
            charm.on[self._relation_name].relation_broken,
            self._on_relation_broken
        )

    def get_partitions(self):
        return self._partitions

    def get_node_data(self):
        return self._nodes

    @property
    def _relation(self):
        return self.framework.model.get_relation(self._relation_name)

    @property
    def _partitions(self):
        return get_partitions(self._get_all_nodes)

    @property
    def _nodes(self):
        """
        node_info = []
        for relation in relations:
            for unit in relation.units:
                node_info.append(relation.data[unit]['node_info'])
        return node_info
        """
        node_info_keys = {
            'ingress-address', 'hostname',
            'partition', 'inventory', 'default',
        }

        return [
            [
                dict_keys_without_hyphens({
                    k: relation.data[unit][k]
                    for k in node_info_keys
                })
                for unit in relation.units
            ]
            for relation in self.framework.model.relations['slurmd']
        ]

    def _on_relation_created(self, event):
        logger.debug("################ LOGGING RELATION CREATED ####################")
        #logger.debug(self._relation)
        #event.relation.data[self.model.unit]['hostname'] = self.hostname
        #event.relation.data[self.model.app]['hostname'] = self.hostname
        #logger.debug(self._relation)

    def _on_relation_joined(self, event):
        logger.debug("################ LOGGING RELATION JOINED ####################")

        #logger.debug(self._relation)
        #logger.debug(event.relation.data)
        #logger.debug("################ LOGGING EVENT DATA in RELATION JOINED ####################")
        #logger.debug(event.relation.data[self.model.app])
        #logger.debug(event.relation.data[self.model.unit])
        #logger.debug("################ LOGGING SELF RELATION DATA in RELATION JOINED ####################")
        #logger.debug(self._relation)
        #loggevent.relation.data.geter.debug(self._relation.data)

    def _on_relation_changed(self, event):
        logger.debug("################ LOGGING RELATION CHANGED ####################")
        for relation in self.framework.model.relations['slurmd']:
            for unit in relation.units:
                for key in ['ingress-address', 'hostname', 'partition', 'inventory', 'default']:
                    if not relation.data[unit].get(key):
                        event.defer()
                        return
        self.framework.breakpoint("in-relation-changed")

    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")


class RequirerCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)
        
        self.slurmd_requirer = TestingRequirerRelation(self, "slurmd")
        
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)

    def on_install(self, event):
        pass

    def on_start(self, event):
        pass

if __name__ == "__main__":
    main(RequirerCharm)
