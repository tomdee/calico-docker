from etcd import EtcdResult, EtcdKeyNotFound, EtcdAlreadyExist, EtcdNotFile
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NotEmptyError

# TODO?
# Reads comes from zk
# Writes go to etcd and zk

class Client(object):

    def __init__(self, host=None, port=None):
        # self.etcd_client = etcd.Client(host=host, port=int(port))
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()
        self.zk = zk

    def _get_more(self, key):
        result = {}
        for child in self.zk.get_children(key):
            full_path = "%s/%s" % (key, child)
            (value, node) = self.zk.get(full_path)
            if node.numChildren > 0 and node.dataLength == 0:
                result.update(self._get_more(full_path))
            else:
                result[full_path] = value
        return result

    def read(self, key, recursive=False):
        # Return an etcdresult
        try:
            # Convert a ZK thing to an etcd thing
            if not recursive:
                (value, node) = self.zk.get(key)
                print "node %s" % str(node)
                result = EtcdResult(node={"value":value})
            else:
                # Make sure I pass in children to EtcdResult()
                # Set dir=True and nodes to the raw data
                result_dict = self._get_more(key)
                children = []
                for key, value in result_dict.iteritems():
                    children.append({"key": key, "value":
                        value})

                result = EtcdResult(node={"value": None, "dir": True,
                                          "nodes": children})
        except NoNodeError:
            raise EtcdKeyNotFound()

        return result

    def write(self, path, value, append=False, dir=False):
        path = path.rstrip('/')
        self.zk.ensure_path(path)
        if dir:
            self.zk.ensure_path(path)
        elif append:
            # TODO I think the sequence/append semantics are different....
            self.zk.create(path+"/append", value, sequence=append)
        else:
            # Try to update it and if it doesn't exist then create it.
            try:
                self.zk.set(path, value)
                print "Setting %s to %s" % (path, value)
            except NoNodeError:
                # I think it's safe to always set makepath to true,
                # but check... TODO
                self.zk.create(path, value, makepath=True)
        # TODO - ignoring prevValue - But it's possible to do in ZK

    def delete(self, host_path, recursive=False, dir=None):
        # dir=True and recursive=True
        # TODO - I'm just ignoring dir - I think that's fine.
        try:
            self.zk.delete(host_path, recursive=recursive)
        except NoNodeError:
            raise EtcdKeyNotFound()
        except NotEmptyError:
            raise EtcdNotFile()
