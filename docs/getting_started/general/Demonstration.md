TODO - Where (and how) best to link to troubleshooting... If you have difficulty, try the [Troubleshooting Guide](./Troubleshooting.md).
# Calico
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
    39de206f7499        calico/node:v0.5.2   "/sbin/my_init"        2 minutes ago       Up 2 minutes                                                         calico-node
    5e36a7c6b7f0        quay.io/coreos/etcd  "/etcd --name calico   30 minutes ago      Up 30 minutes       0.0.0.0:4001->4001/tcp, 0.0.0.0:7001->7001/tcp   quay.io-coreos-etcd

## Networking containers.
TODO - intro about what is actually going to be shown here. How networking is only done _after_ the container is started etc...

### Starting containers
Let's go ahead and start a few of containers on each host.

On calico-01

    docker run --net=none --name workload-A -tid busybox
    docker run --net=none --name workload-B -tid busybox
    docker run --net=none --name workload-C -tid busybox

On calico-02

    docker run --net=none --name workload-D -tid busybox
    docker run --net=none --name workload-E -tid busybox

### Adding Calico networking
TODO - run some calicoctl container add commands...

### Testing it
A, C and E are all in the same profile so should be able to ping each other.  B and D are in their own profile so shouldn't be able to ping anyone else.
    
On calico-01 check that A can ping C and E.

    docker exec workload-A ping -c 4 TODO
    docker exec workload-A ping -c 4 TODO

Also check that A cannot ping B or D

    docker exec workload-A ping -c 4 TODO
    docker exec workload-A ping -c 4 TODO

