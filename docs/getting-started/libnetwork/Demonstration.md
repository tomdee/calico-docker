TODO - Where (and how) best to link to troubleshooting... If you have difficulty, try the [Troubleshooting Guide](./Troubleshooting.md).
# Calico as a libnetwork plugin.
TODO - intro...
TODO video e.g. [![asciicast](https://asciinema.org/a/14.png)](https://asciinema.org/a/14?autoplay=1)

## Environment
This demonstration makes some assumptions about the environment you have. See [EnvironmentSetup](EnvironmentSetup.md) for instructions on getting an appropriate environment.

If you have everything set up properly you should have the following hosts and should have calicoctl in your $PATH.

| hostname  | IP address   |
|-----------|--------------|
| calico-01 | 172.17.8.101 |
| calico-02 | 172.17.8.102 |

## Starting Calico services<a id="calico-services"></a>

Once you have your cluster up and running, start calico on all the nodes

On calico-01

    sudo calicoctl node

On calico-02

    sudo calicoctl node

This will start a container on each host. Check they are running

    docker ps

You should see output like this on each node

    vagrant@calico-01:~$ docker ps -a
    CONTAINER ID        IMAGE                    COMMAND                CREATED             STATUS              PORTS                                            NAMES
    39de206f7499        calico/node:v0.5.3   "/sbin/my_init"        2 minutes ago       Up 2 minutes                                                         calico-node


## Creating networked endpoints

The experimental channel version of Docker introduces a new flag to `docker run` to network containers:  `--publish-service <service>.<network>.<driver>`.

 * `<service>` is the name by which you want the container to be known on the network.
 * `<network>` is the name of the network to join.  Containers on different networks cannot communicate with each other.
 * `<driver>` is the name of the network driver to use.  Calico's driver is called `calico`.

So let's go ahead and start a few of containers on each host.

On calico-01

    docker run --publish-service srvA.net1.calico --name workload-A -tid busybox
    docker run --publish-service srvB.net2.calico --name workload-B -tid busybox
    docker run --publish-service srvC.net1.calico --name workload-C -tid busybox

On calico-02

    docker run --publish-service srvD.net3.calico --name workload-D -tid busybox
    docker run --publish-service srvE.net1.calico --name workload-E -tid busybox

By default, networks are configured so that their members can communicate with one another, but workloads in other networks cannot reach them.  A, C and E are all in the same network so should be able to ping each other.  B and D are in their own networks so shouldn't be able to ping anyone else.
    
On calico-01 check that A can ping C and E.

    docker exec workload-A ping -c 4 srvC
    docker exec workload-A ping -c 4 srvE

Also check that A cannot ping B or D

    docker exec workload-A ping -c 4 srvB
    docker exec workload-A ping -c 4 srvD

To see the list of networks, use

    docker network ls

TODO is this really the best demo???

## IPv6 (Optional)
TODO - make this happen as part of the environment setup...

To connect your containers with IPv6, first make sure your Docker hosts each have an IPv6 address assigned.

On calico-01

    sudo ip addr add fd80:24e2:f998:72d7::1/112 dev eth1

On calico-02

    sudo ip addr add fd80:24e2:f998:72d7::2/112 dev eth1

Verify connectivity by pinging.

On calico-01

    ping6 -c 4 fd80:24e2:f998:72d7::2

Then restart your calico-node processes with the `--ip6` parameter to enable v6 routing.

On calico-01

    calicoctl node --ip=172.17.8.101 --ip6=fd80:24e2:f998:72d7::1

On calico-02

    calicoctl node --ip=172.17.8.102 --ip6=fd80:24e2:f998:72d7::2

Then, you can start containers with IPv6 connectivity. By default, Calico is configured to use IPv6 addresses in the pool fd80:24e2:f998:72d6/64 (`calicoctl pool add` to change this).

On calico-01

    docker run --publish-service srvF.net4.calico --name workload-F -tid ubuntu

Then get the ipv6 address of workload-F

    docker inspect --format "{{ .NetworkSettings.GlobalIPv6Address }}" workload-F

Note that we have used `ubuntu` instead of `busybox`.  Busybox doesn't support IPv6 versions of network tools like ping.

One calico-02

    docker run --publish-service srvG.net4.calico --name workload-G -tid ubuntu

Then ping workload-F via its ipv6 address that you received above (change the IP address if necessary):

    docker exec workload-G ping6 -c 4 fd80:24e2:f998:72d6::1
