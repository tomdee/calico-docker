# Preparing Environment for Libnetwork Demonstration
The demonstration of the Calico libnetwork plugin is run on two Linux servers. As well as the [general](TODO) Calico requirements, libnetwork imposes a few more
* An experimental version of Docker
* consul for clustering Docker

We've prepared a number of guides for creating such an environment, or if you know what you're doing, the steps are documented below.
* [Vagrant install of Ubuntu](TODO) 
* [Vagrant install of CoreOS](TODO)
* [AWS](TODO) - TODO say which OS
* [DO](TODO)
* [GCE](TODO)

Once you have the environment set up, you can run through the [demonstration](Demonstration.md)

# Manual Setup

If you don't want to use one of the prepared environments above, you can create your own. 

## Requirements

In addition to the requirements from [general](TODO) you'll need the following.

### Consul
TODO consul
Grab the binary, unzip it, and run it with the following command...
See https://github.com/Metaswitch/calico-ubuntu-vagrant/blob/f2bf232134e3770360bb9e79b6e52da544b48ada/Vagrantfile#L41

### Experimental Docker

## Final checks
In addition to the checks in [general](TODO), check that you have the right version of Docker

   docker version
   
Check that it shows 1.8.0 and experimental
