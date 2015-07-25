# Running Calico on a Docker Swarm
The following instructions configure a Docker Swarm cluster networked using Calico.  In this tutorial, we will do the following. 
- Configure etcd and Calico on a cluster.
- Configure Docker Swarm on our VM cluster.
- Provision workloads on the Swarm, and check they can communicate.

## Prerequisites
To complete this demo, make sure you have the following prerequisites.
- Four Linux servers (VMs or bare-metal) with [Docker 1.4](https://docs.docker.com/installation/) or later installed.  The servers should have IP connectivity to each other.

Our Docker Swarm will consist of four nodes with the following roles: 
  - 1 Swarm manager (to manage the Swarm nodes)
  - 1 Swarm client (to control the Swarm)
  - 2 Swarm nodes (to host our containers)

## Installing etcd
Calico requires etcd, so let's install it on our cluster.  For this example, we'll only configure a single node etcd cluster.  However, in a production environment, a minimum size of three nodes is recommended.

Run the following on the **manager server* to download the etcd binaries:
```
# Download etcd for Linux 
curl -L https://github.com/coreos/etcd/releases/download/v2.0.11/etcd-v2.0.11-linux-amd64.tar.gz -o etcd-v2.0.11-linux-amd64.tar.gz
tar xzvf etcd-v2.0.11-linux-amd64.tar.gz

# Move the binaries to /usr/local/bin for easy access.
cd etcd-v2.0.11-linux-amd64
sudo cp etcd /usr/local/bin
sudo cp etcdctl /usr/local/bin
```

Now that etcd is installed, let's run our single node cluster. We need to start etcd with the IP address of the manager server, so store the manager server's IP as environment variable for easy access.
```
export MANAGER_IP=<Manager's IP address>
```

Then, start etcd:
```
etcd -name etcd0  -advertise-client-urls http://$MANAGER_IP:2379,http://$MANAGER_IP:4001 \
  -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
  -initial-advertise-peer-urls http://$MANAGER_IP:2380 \
  -listen-peer-urls http://0.0.0.0:2380  \
  -initial-cluster-token etcd-cluster-1 \
  -initial-cluster etcd0=http://$MANAGER_IP:2380 \
  -initial-cluster-state new &
```

## Installing Calico 
Now that etcd is running, we can install calico.  

To make things simpler, let's store a couple of commonly used values in environment variable on each **Swarm node** to be used later:
```
export MANAGER_IP=<Manager's IP Address>
export NODE_IP=<This Node's IP Address>
```

Run the following set of commands on each **node** to download and start Calico.
```
# Download calicoctl and make it executable:
wget https://github.com/Metaswitch/calico-docker/releases/download/v0.4.8/calicoctl
chmod +x ./calicoctl

# Point this node at the etcd cluster
export ETCD_AUTHORITY=$MANAGER_IP:4001

# Configure local Docker requests to be routed through Powerstrip.
export DOCKER_HOST=localhost:2377

# Check that all required dependencies are installed.
sudo ./calicoctl checksystem --fix

# Start the calico node service.  We must specify the ETCD_AUTHORITY variable since 
# sudo uses its own environment.
sudo ETCD_AUTHORITY=$MANAGER_IP:4001 ./calicoctl node --ip=$NODE_IP
```

We want to install calicoctl on our client as well, so that we can direct calico commands at the Swarm cluster. However, we don't need to start a Calico node on the client, since we won't be running any containers on it.

Run the following on your **client**:
```
# Set the IP of the Swarm manager
export MANAGER_IP=<Manager's IP Address>

# Download calicoctl and make it executable:
wget https://github.com/Metaswitch/calico-docker/releases/download/v0.4.8/calicoctl
chmod +x ./calicoctl

# Point this node at the etcd cluster
export ETCD_AUTHORITY=$MANAGER_IP:4001
```

## Installing Swarm on your cluster
Now that Calico networking is configured on our cluster, lets join our nodes into a Docker Swarm cluster.

We'll use the token based discovery backend, so let's first create the token which will identify our swarm.  To do this, run the following on your **client**.  Note that docker commands may need to be run with root privileges depending on your docker installation.
```
docker pull swarm
docker run --rm swarm create
``` 

The second command will print a unique cluster ID token which we must use to configure our Swarm.  We'll reference this value in the tutorial as ```<swarm_token>```. 
Your token should look something like this: d435dc104abdd89af24ae2392c7338ce

Now that we've got a token, we can begin to configure our Swarm.  First, let's join each of our two Swarm nodes to the
cluster.  

Run the following commands on each node, replacing ```<swarm_token>``` with the token from above.
```
docker run -d swarm join --addr=$NODE_IP:2377 token://<swarm_token>
```

Let's now configure the Swarm manager.  To do this, run the following on your **Swarm manager**.  Note that ```<swarm_port>``` in the following command can be any unused TCP port on the manager server.  This is the port the client will use to communicate with the Swarm manager daemon. 
```
docker run -d -p <swarm_port>:2375 swarm manage token://<swarm_token>
```

We're now ready to provision containers on our Swarm. 

## Create containers and check connectivity.
At this point we should have a fully configured Calico networked Swarm cluster.  However, there are no workloads running on our cluster.  Let's create a few containers and check their connectivity.  We can run the following commands on the client against the Swarm Manager using the -H flag.

Set the SWARM_PORT environment variable on the **client** to the value chosen when configuring the Swarm manager.
```
export SWARM_PORT=<swarm_port>
```

First, create profiles using calicoctl.  These profiles will allow our containers to communicate. Run the following commands on your **client**.
```
./calicoctl profile add PROF_A_B_C
./calicoctl profile add PROF_D
./calicoctl profile add PROF_E
```

Now, let's create some containers on our cluster. Run the following commands on your **client**.
```
docker -H $MANAGER_IP:$SWARM_PORT run -e CALICO_IP=192.168.1.1 \
      -e CALICO_PROFILE=PROF_A_B_C --name workload-A -tid busybox
docker -H $MANAGER_IP:$SWARM_PORT run -e CALICO_IP=192.168.1.2 \
      -e CALICO_PROFILE=PROF_A_B_C --name workload-B -tid busybox
docker -H $MANAGER_IP:$SWARM_PORT run -e CALICO_IP=192.168.1.3 \
      -e CALICO_PROFILE=PROF_A_B_C --name workload-C -tid busybox
docker -H $MANAGER_IP:$SWARM_PORT run -e CALICO_IP=192.168.1.4 \
      -e CALICO_PROFILE=PROF_D --name workload-D -tid busybox
docker -H $MANAGER_IP:$SWARM_PORT run -e CALICO_IP=192.168.1.5 \
      -e CALICO_PROFILE=PROF_E --name workload-E -tid busybox
```

We can run ```ps``` on the **client** against the Swarm manager to check that the containers have been created. 
```
docker -H $MANAGER_IP:$SWARM_PORT ps
```

You should see output which looks similar to this - notice that the containers have been distributed across our two Swarm nodes.
```
CONTAINER ID        IMAGE                COMMAND             CREATED             STATUS              PORTS         NAMES
11a76a439cfa        busybox              "/bin/sh"           42 minutes ago      Up 42 minutes                     swarm-node2/workload-E
9196feb986ef        busybox              "/bin/sh"           43 minutes ago      Up 42 minutes                     swarm-node1/workload-D
6971bed91ea7        busybox              "/bin/sh"           43 minutes ago      Up 43 minutes                     swarm-node2/workload-C
4ad182b5cfbd        busybox              "/bin/sh"           43 minutes ago      Up 43 minutes                     swarm-node1/workload-B
58736abaf698        busybox              "/bin/sh"           44 minutes ago      Up 44 minutes                     swarm-node2/workload-A
9c22e2e3b393        calico/node:v0.4.8   "/sbin/my_init"     56 minutes ago      Up 55 minutes                     swarm-node1/calico-node
3dff7c3d76c6        calico/node:v0.4.8   "/sbin/my_init"     About an hour ago   Up 59 minutes                     swarm-node2/calico-node
```

Container workload-A should be able to ping workload-B and workload-C, since they belong to the same profile.  Verify this by running the following commands on our **client**:
```
docker -H $MANAGER_IP:$SWARM_PORT exec workload-A ping -c 4 192.168.1.2 
docker -H $MANAGER_IP:$SWARM_PORT exec workload-A ping -c 4 192.168.1.3 
```
