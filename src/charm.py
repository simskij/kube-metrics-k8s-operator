#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from charms.grafana_k8s.v0.grafana_dashboard import GrafanaDashboardProvider
from charms.prometheus_k8s.v0.prometheus_scrape import MetricsEndpointProvider
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class NodeExporterCharm(CharmBase):
    """NodeExporterCharm."""

    _stored = StoredState()
    _name = "kube-metrics"

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.node_exporter_pebble_ready, self._on_exporter_pebble_ready)
        self.framework.observe(self.on.kube_state_metrics_pebble_ready, self._on_kube_state_pebble_ready)
        self.framework.observe(self.on.metrics_server_pebble_ready, self._on_metrics_server_pebble_ready)

        self._stored.set_default(things=[])
        self._scraping = MetricsEndpointProvider(
            self,
            jobs=[
                { "job_name": "node_exporter", "static_configs": [{"targets": ["*:9100"]}]},
                { "job_name": "kube-state-metrics", "static_configs": [{"targets": ["*:8080", "*:8081"]}]}
            ]
        )

        self._dashboards = GrafanaDashboardProvider(
            self,
            relation_name="grafana-dashboard"
        )

    def _on_exporter_pebble_ready(self, event):
        container = event.workload
        pebble_layer = {
            "summary": "node-exporter layer",
            "description": "pebble config layer for node-exporter",
            "services": {
                "exporter": {
                    "override": "replace",
                    "summary": "exporter",
                    "command": "node_exporter",
                    "startup": "enabled",
                }
            },
        }

        container.add_layer(container.name, pebble_layer, combine=True)
        container.autostart()

        self.unit.status = ActiveStatus()

    def _on_kube_state_pebble_ready(self, event):
        container = event.workload
        pebble_layer = {
            "summary": "kube-state-metrics layer",
            "description": "pebble config layer for kube-state-metrics",
            "services": {
                "exporter": {
                    "override": "replace",
                    "summary": "exporter",
                    "command": "/kube-state-metrics --port=8080 --telemetry-port=8081 ",
                    "startup": "enabled",
                }
            },
        }

        container.add_layer(container.name, pebble_layer, combine=True)
        container.autostart()

    def _on_metrics_server_pebble_ready(self, event):
        container = event.workload
        pebble_layer = {
            "summary": "metrics-server layer",
            "description": "pebble config layer for metrics-server",
            "services": {
                "exporter": {
                    "override": "replace",
                    "summary": "exporter",
                    "command": "/metrics-server",
                    "startup": "enabled",
                }
            },
        }

        container.add_layer(container.name, pebble_layer, combine=True)
        container.autostart()


if __name__ == "__main__":
    main(NodeExporterCharm)
