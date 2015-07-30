[![Circle CI](https://circleci.com/gh/Metaswitch/calico-docker/tree/master.svg?style=svg)](https://circleci.com/gh/Metaswitch/calico-docker/tree/master)
# Calico on Docker
As well as providing networking for OpenStack VMs, Calico can provide networking for containers in a Docker environment.  Each container gets its own IP and fine grain security policy.  In addition, Calico can be deployed without encapsulation or overlays to provide high performance at massive scales.  For more information on Project Calico see http://www.projectcalico.org/learn/.

Development is very active at the moment so please Star this project and check back often.

We welcome questions/comments/feedback (and pull requests).

* Mailing List - http://lists.projectcalico.org/listinfo/calico
* IRC - [#calico](http://webchat.freenode.net?randomnick=1&channels=%23calico&uio=d4)
* For Calico-on-Docker specific issues, please [raise issues](https://github.com/Metaswitch/calico-docker/issues/new) on Github.

## Getting Started

To get started using [Calico Docker networking][calico-networking], we recommend running through one or more of the
available tutorials described below.

If you would like to get involved writing code for calico-docker, or if you need to build binaries specific to your
OS, checkout out the [Building and testing guide](docs/Building.md).

### Tutorials

Fully worked demonstrations of Calico Docker networking are available for the following environments:

- [Vagrant install with CoreOS](docs/getting-started/VagrantCoreOS.md)
- [Vagrant install with Ubuntu](docs/getting-started/VagrantUbuntu.md)
- [Amazon Web Services (AWS)](docs/getting-started/AWS.md)
- [Google Compute Engine (GCE)](docs/getting-started/GCE.md)
- [DigitalOcean](docs/getting-started/DigitalOcean.md)

For each of these environments, it is possible to run with one of three different 
[networking options](#networking-options), described below.  Each of the demonstrations indicates where the instructions
differ for each of these networking options.

We also provide a demonstration of a [Docker Swarm cluster](docs/getting-started/powerstrip/CalicoSwarm.md) networked 
using Calico. This particular demonstration utilizes the [powerstrip](#docker-with-powerstrip) networking option.

For a quick start, we'd recommend following one of the Vagrant installations using the default docker networking.


### Networking options

#### Default docker networking

This uses Dockers standard networking infrastructure, requiring you to explicitly add a created contained into a
Calico network.

#### Docker with libnetwork

Docker's native [libnetwork network driver](https://github.com/docker/libnetwork) is available in the Docker
[experimental channel](https://github.com/docker/docker/tree/master/experimental) alongside the Docker 1.7 release.
Docker's experimental channel is still moving fast and some of its features are not yet fully stable.  The current
master branch of calico-docker is largely focussed on interworking with libnetwork.

#### Docker with Powerstrip

Powerstrip is a pluggable HTTP proxy for the Docker API.  Development of the Powerstrip version of Calico is lagging 
behind the master branch, so an older version of `calicoctl` and the `calico-node` docker image are required.
  

## How does it work?

Calico connects datacenter workloads (containers, VMs, or bare metal) via IP no matter which compute host they are on.
Read about it on the [Project Calico website](http://www.projectcalico.org).  Endpoints are network interfaces
associated with workloads.

Project Calico uses [etcd](https://github.com/coreos/etcd) to distribute information about workloads, endpoints, and 
policy to each Docker host.

The `calico-node` service is a worker that configures the network endpoints for containers, handles IP routing, and 
installs policy rules.  It runs in its own Docker container, and comprises
- Felix, the Calico worker process
- BIRD, the routing process

We provide a command line tool, `calicoctl`, which makes it easy to configure and start the Calico services listed 
above, and allows you to interact with the etcd datastore to define and apply network and security policy to the 
containers you create. Using `calicoctl`, you can provision Calico nodes, endpoints, and define and manage a rich set 
of security policy. 

## FAQ 
For more information on what you can do with Calico, please visit the [frequently asked questions](docs/FAQ.md) page. 
