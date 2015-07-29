# Preparing Environment for Powerstrip 
The Powerstrip Calico demonstration is run on two Linux servers. The requirements the same as the [general ones](../general/EnvironmentSetup.md) but with one important exception.
 
Development of the Powerstrip version of Calico is lagging behind the master branch, so an older version of `calicoctl` and the `calico-node` docker image are required.

Once you have the environment set up, you can run through the [demonstration](Demonstration.md)

# Manual Setup

If you don't want to use one of the prepared environments above, you can create your own. Follow the requirements from the [general requirements](../general/EnvironmentSetup.md) environment setup but make the following changes. 

## Getting Calico Binaries
Get the calicoctl binary onto each host.  Don't use the latest [release](https://github.com/Metaswitch/calico-docker/releases/) from github. Version v0.4.8 is required.

	wget https://github.com/Metaswitch/calico-docker/releases/download/v0.4.8/calicoctl
	chmod +x calicoctl
	
This binary should be placed in your $PATH so it can be run from any directory.

### Preload the Calico docker image (optional)
You can optionally preload the Calico Docker image to avoid the delay when you run `calicoctl node` the first time. 
Be sure to use the v0.4.8 release.

    docker pull calico/node:v0.4.8
