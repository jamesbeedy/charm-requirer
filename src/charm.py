#! /usr/bin/env python3
from ops.charm import CharmBase

from ops.main import main


import logging
import socket
import json

from ops.framework import (
    Object,
    ObjectEvents,
    StoredState,
)


logger = logging.getLogger()


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

    @property
    def _relation(self):
        return self.framework.model.get_relation(self._relation_name)

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
        #logger.debug(self._relation.data)

    def _on_relation_changed(self, event):
        logger.debug("################ LOGGING RELATION CHANGED ####################")
        self.framework.breakpoint('testing-requirer-on-relation-joined')
        
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
