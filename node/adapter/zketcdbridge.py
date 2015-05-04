from kazoo.client import KazooClient


class Client(object):
    def __init__(self):
        # self.etcd_client = etcd.Client(host=host, port=int(port))
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()

    def read(self, config_dir):
        # Need recursive
        # Need to return leaves and children and value
        pass

    def write(self, param, IF_PREFIX):
        # Need append=True too
        # And prevValue
        pass

    def delete(self, host_path, dir, recursive):
        # dir=True and recursive=True
        pass
