# etcd Directory Structure

The following illustrates the directory structure calico uses in etcd.

 	+--calico  # root namespace
 	   |
 	   |--v1
 	   |  |--config
 	   |  |  |--InterfacePrefix # the prefix for Calico interface names
 	   |  |  `--LogSeverityFile # Log severity level for writing to file e.g. "DEBUG"
	   |  |--host
	   |  |  `--<hostname>      # one for each Docker host in the cluster
	   |  |     |--config       # Host level config
	   |  |     |  `--marker
	   |  |     |--ipv4_address # the next hop IP address of this host
	   |  |     `--workload
	   |  |        `--docker
	   |  |           `--<container-id>  # one for each container on the Docker Host
	   |  |              `--endpoint
	   |  |                 `--<endpoint-id>  # JSON endpoint config (see below)
	   |  |--policy
	   |  |  `--profile
	   |  |     `--<profile-id>  # Unique string name
	   |  |        |--tags  # JSON list of tags
	   |  |        `--rules  # JSON rules config (see below)
	   |  `--ipam  #IP Address Management
	   |     |--v4
	   |     |   |--pool
	   |     |   |  `--<CIDR>  # One per pool, key is CIDR with '/' replaced
	   |     |   |             # by '-', value is JSON object (see below)
	   |     |   `--assignment
	   |     |      `--<CIDR>  # One per pool
	   |     |         `--<address>  # One per assigned address in the pool
	   |     `--v6
	   |         |--pool
	   |         |  `--<CIDR>  # One per pool, key is CIDR with '/' replaced
	   |         |             # by '-', value is JSON object (see below)
	   |         `--assignment
	   |            `--<CIDR>  # One per pool
	   |               `--<address>  # One per assigned address in the pool
 	   `--bgp/v1  # root namespace
 	      |--global
 	      |  |--as_num    # the default BGP AS number for the nodes
 	      |  |--node_mesh # JSON node-to-node mesh configuration (see below)
	      |  |--peer_v4   # Global IPv4 BGP peers (all nodes peer with)
	      |  |  `--<BGP peer IPv4 address>  # JSON BGP peer configuration (see below)
	      |  `--peer_v6   # Global IPv6 BGP peers (all nodes peer with)
	      |     `--<BGP peer IPv6 address>  # JSON BGP peer configuration (see below)
	      `--host
	         `--<hostname>  # one for each Docker host in the cluster
	            |--ip_addr_v4 # the IP address BIRD listens on
	            |--ip_addr_v6 # the IP address BIRD6 listens on
	            |--as_num     # the AS number for this host
	            |--peer_v4    # Host specific IPv4 BGP peers
	            |  `--<BGP peer IPv4 address>  # JSON BGP peer configuration (see below)
	            `--peer_v6  # Host specific IPv6 BGP peers
	               `--<BGP peer IPv6 address>  # JSON BGP peer configuration (see below)


## JSON endpoint configuration

The endpoint configuration stored at 

	/calico/v1/host/<hostname>/workload/docker/<container_id>/endpoint/<endpoint_id>

is a JSON blob in this form:

	{
	  "state": "active|inactive",  # Later, "moved" etc...
	  "name": "<name of linux interface>",
	  "mac": "<MAC of the interface>",
	  "profile_id": "<profile_id>",
	  
	  # Subnets that are owned by the endpoint, ie. that it is
	  # allowed to use as a source for its traffic.
	  "ipv4_nets": [
	    # Always expecting /32s for now but later would could allow
	    # the workload to own a subnet.
	    "198.51.100.17/32",
	    … 
	  ],
	  "ipv6_nets": [
	    # Always expecting /128s for now.
	    "2001:db8::19/128",
	    …
	  ],
	  "ipv4_gateway": "<IP address>",
	  "ipv6_gateway": "<IP address>"
	}

## JSON rules configuration

The rules leaf at 

	/calico/v1/policy/profile/<profile_id>/rules

contains a JSON blob in this format

	{
	  "inbound": [{<rule>}, ...],
	  "outbound": [{<rule>}, ...]
	}

where each entry in the inbound/outbound list is a rule object:

	{
	  # Optional match criteria.  These are and-ed together.
	  "protocol": "tcp|udp|icmp|icmpv6",

	  "src_tag": "<tag name>",
	  "src_net": "<CIDR>",
	  "src_ports": [1234, "2048:4000"],  # List of ports or ranges.
	      # No artificial limit on number of ports in list.

	  # As above but for destination addr/port.
	  "dst_tag": "<tag name>",
	  "dst_net": "<CIDR>",
	  "dst_ports": [<list of ports / ranges>],

	  "icmp_type": <int>,  # Requires "protocol" to be set to an 
	      # ICMP type 

	  # Action if we match, defaults to allow, if missing.
	  "action": "deny|allow"
	} 

## JSON IP pool configuration

The IP pool configuration stored at

        /calico/v1/ipam/v4/pool/<CIDR> and
        /calico/v1/ipma/v6/pool/<CIDR>

is a JSON blob in this form:

        {
          "cidr": "<CIDR of pool - eg. 192.168.0.0/16 or fd80:24e2:f998:72d6::/64>",
          "ipip": "<IPIP device name if IPIP configured for the pool - usually tunl0>",
          "masquerade": true|false
        }

The ipip field is only included if IPIP is enabled for this pool.  IPIP is only supported on IPv4 pools.  

The masquerade field enables NAT for outbound traffic.  If omitted, masquerade defaults to false.

## JSON node-to-node mesh configuration

The configuration controlling whether a full node-to-node BGP mesh is set up
automatically.

The node-to-node mesh configuration stored at

	/calico/v1/config/bgp_node_mesh

is a JSON blob in this form:

 	{
	  "enabled": true|false
	}

If the key is missing from etcd, the node-to-node mesh is enabled by default.

## JSON BGP Peer configuration

Explicit BGP peers are configurable globally (all hosts peer with these), or
for a specific host.

The full set of peers for a specific host comprises all other hosts (if the
node-to-node mesh is enabled), the set of global peers and the set of peers
specific to the host.

The configuration for the global BGP peers is stored at

	/calico/v1/config/bgp_peer_v4/<BGP peer IPv4 address>
and
	/calico/v1/config/bgp_peer_v6/<BGP peer IPv6 address>


The configuration for the host node specific BGP peers is stored at

	/calico/v1/host/<hostname>/bgp_peer_v4/<BGP peer IPv4 address>
and
	/calico/v1/host/<hostname>/bgp_peer_v6/<BGP peer IPv6 address>

In all cases, the data is a JSON blob in the form:

        {
          "ip": "IP address of BGP Peer",
          "as_num": "The AS Number of the peer"
        }

