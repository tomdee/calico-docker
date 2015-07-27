# Set up Calico on CoreOS using Vagrant

You can quickly set up a CoreOS cluster ready to network Docker containers with <a href="https://github.com/Metaswitch/calico-docker">Calico Docker networking</a> using the Vagrant files in this repo.

## Streamlined setup

1) Install dependencies

* [VirtualBox][virtualbox] 4.3.10 or greater.
* [Vagrant][vagrant] 1.6 or greater.
* [Git][git]

2) Clone this project and get it running!

    git clone https://github.com/Metaswitch/calico-coreos-vagrant-example.git
    cd calico-coreos-vagrant-example

3) Startup and SSH

Run
    vagrant up

To connect to your servers
* Linux/Mac OS X
    * run `vagrant ssh <hostname>`
* Windows
    * Follow instructions from https://github.com/nickryand/vagrant-multi-putty
    * run `vagrant putty <hostname>`

4) Verify environment

You should now have two CoreOS servers, each running etcd in a cluster. The servers are named calico-01 and calico-02 and IP addresses 172.17.8.101 and 172.17.8.102.

At this point, it's worth checking that your servers can ping each other.

From calico-01

    ping 172.17.8.102

From calico-02

    ping 172.17.8.101

If you see ping failures, the likely culprit is a problem with the VirtualBox network between the VMs.  You should check that each host is connected to the same virtual network adapter in VirtualBox and rebooting the host may also help.  Remember to shut down the VMs with `vagrant halt` before you reboot.

You should also verify that etcd is running and showing both nodes as healthy.

    etcdctl cluster-health

## Try out Calico networking
Now you have a basic two node CoreOS cluster setup and you are ready to try Calico neworking.

Follow the step by step [getting started instructions][using-calico] in the main calico-docker repo.

[virtualbox]: https://www.virtualbox.org/
[vagrant]: https://www.vagrantup.com/downloads.html
[using-coreos]: http://coreos.com/docs/using-coreos/
[using-calico]: https://github.com/Metaswitch/calico-docker/blob/powerstrip-archive/docs/GettingStarted.md
[git]: http://git-scm.com/