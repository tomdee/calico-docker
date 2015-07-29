# Set up Calico on CoreOS using Vagrant

These instructions allow you to set up a CoreOS cluster ready to network Docker containers with 
[Calico Docker networking][calico-networking] using Vagrant.

## Streamlined setup

1) Install dependencies

* [VirtualBox][virtualbox] 4.3.10 or greater.
* [Vagrant][vagrant] 1.6 or greater.
* [Git][git]

2) Clone this project

    git clone https://github.com/Metaswitch/calico-docker.git
    
3) There are three demonstration options depending on whether you are running with libnetwork, powerstrip or the default docker networking.  Select the required demonstration by cd-ing into the appropriate directory:

  - For default docker networking
  
    ```cd calico-docker/docs/getting-started/default-networking/vagrant-coreos```
    
  - For libnetwork
  
    ```cd calico-docker/docs/getting-started/libnetwork/vagrant-coreos```
    
  - For powerstrip
  
    ```cd calico-docker/docs/getting-started/powerstrip/vagrant-coreos```

4) Startup and SSH

Run

    vagrant up

To connect to your servers
* Linux/Mac OS X
    * run `vagrant ssh <hostname>`
* Windows
    * Follow instructions from https://github.com/nickryand/vagrant-multi-putty
    * run `vagrant putty <hostname>`

5) Verify environment

You should now have two CoreOS servers, each running etcd in a cluster. The servers are named calico-01 and calico-02 
and IP addresses 172.17.8.101 and 172.17.8.102.

At this point, it's worth checking that your servers can ping each other.

From calico-01

    ping calico-02

From calico-02

    ping calico-01

If you see ping failures, the likely culprit is a problem with the VirtualBox network between the VMs.  You should 
check that each host is connected to the same virtual network adapter in VirtualBox and rebooting the host may also 
help.  Remember to shut down the VMs with `vagrant halt` before you reboot.

You should also verify that etcd is running and showing both nodes as healthy.

    etcdctl cluster-health

## Try out Calico networking
Now you have a basic two node CoreOS cluster setup and you are ready to try Calico neworking.

You can now run through the standard Calico demonstration.  There are three demonstration options depending on 
whether you are running with libnetwork, powerstrip or the default docker networking.

- [demonstration with docker default networking](default-networking/Demonstration.md)
- [demonstration with libnetwork](libnetwork/Demonstration.md) 
- [demonstration with powerstrip](powerstrip/Demonstration.md)


[calico-networking]: https://github.com/Metaswitch/calico-docker
[virtualbox]: https://www.virtualbox.org/
[vagrant]: https://www.vagrantup.com/downloads.html
[using-coreos]: http://coreos.com/docs/using-coreos/
[git]: http://git-scm.com/