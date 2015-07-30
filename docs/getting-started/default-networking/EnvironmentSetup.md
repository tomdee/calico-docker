# Preparing Environment 
The basic Calico demonstration is run on two Linux servers. These servers should be running a recent version of Linux and require a few network related kernel modules to be loaded. The easiest way to ensure this and that the servers meet the requirements is to run `calicoctl checksystem --fix`

The servers also need
* Docker to be running - since the Calico agent is packaged as a Docker container.
* An Etcd cluster - which Calico uses for coordinating state between the nodes.
* The `calicoctl` to be placed in the `$PATH`.

Once you have the environment set up, you can run through the [demonstration](Demonstration.md)

# Manual Setup

If you don't want to use one of the prepared environments above, you can create your own. 

## Requirements

For the demonstration, you just need 2 servers (bare metal or VMs) with a modern 64-bit Linux OS and Layer-2 network (Ethernet) connectivity between them.

They must have the following software installed.
 * Docker v1.6 or greater: [Docker](http://www.docker.com)
 * etcd installed and available on each node: [etcd Documentation](https://coreos.com/etcd/docs/latest/)
 * `ipset`, `iptables`, and `ip6tables` kernel modules.

They should be configured with the following hostnames and IPs
| hostname  | IP address   |
|-----------|--------------|
| calico-01 | 172.17.8.101 |
| calico-02 | 172.17.8.102 |

### Docker permissions
Running Docker is much easier if your user has permissions to run Docker commands. If your distro didn't set this permissions as part of the install, you can usually enable this by adding your user to the `docker` group and restarting your terminal.

    sudo usermod -aG docker <your_username>

If you prefer not to do this you can still run the demo but remember to run `docker` using `sudo`.

### Getting calicoctl Binary
Get the calicoctl binary onto each host.  You can download a specific [release](https://github.com/Metaswitch/calico-docker/releases/) from github.  For example, to retrieve the latest v0.5.3 release, on each host run

	wget https://github.com/Metaswitch/calico-docker/releases/download/v0.5.3/calicoctl
	chmod +x calicoctl
	
This binary should be placed in your $PATH so it can be run from any directory.

### Preload the Calico docker image (optional)
You can optionally preload the Calico Docker image to avoid the delay when you run `calicoctl node` the first time. 
Select the same version of the Calico Docker image as you selected above.  For example, to pull the latest released version

    docker pull calico/node:v0.5.3

## Final checks

Verify the hostnames and IP addresses assigned to your servers.  If they don't match the recommended versions above then you'll need to adjust the demonstration instructions.

Verify that your hosts can ping one another.

You should also verify each host can access etcd.  The following will return an error if etcd is not available.

    etcdctl ls /