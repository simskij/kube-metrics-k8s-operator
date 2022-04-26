# kube-metrics-k8s-operator

## Description

The Kube Metrics k8s operator is a charm that combines the Prometheus [node_exporter]()
and the [kube_state_metrics]() into a single charm. It allows for easy, turn-key monitoring 
using the charms of the [Canonical Observability Stack]().
## Usage

To deploy this charm using Juju 2.9.0 or later, switch to a model running 
on Kubernetes and run:

```shell
$ juju deploy \
    kube-metrics-k8s \
    metrics \
    --channel edge \
    --trust
```
## Relations

The kube-metrics charm offers two relations, `metrics-endpoint` and `grafana-dashboard`.

`metrics-endpoint` implements the provider-side of the `prometheus_scrape` interface, allowing you to relate it to a `prometheus-k8s` charm for automated scraping. 

`grafana-dashboard` implements the provider-side of the `grafana_dashboard` interface, allowing you to relate
it to a `grafana-k8s` charm for automated dashboard provisioning. 
## OCI Images

This charm uses two OCI images, one for `kube-state-metrics` and one for `node_exporter`. Both images are listed in [metadata.yaml](metadata.yaml).

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines on enhancements to this
charm following best practice guidelines, and
[CONTRIBUTING.md](CONTRIBUTING.md) for developer
guidance.
