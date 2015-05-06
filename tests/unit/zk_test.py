from etcd import EtcdKeyNotFound, EtcdAlreadyExist, EtcdNotFile
from nose.tools import *

from nose.tools import assert_equal, assert_true, assert_false
from node.adapter.ipam import SequentialAssignment, IPAMClient
import node.adapter.zketcdbridge as zk
# import etcd as zk

class TestZKBridge:
    def setup(self):
        self.client = zk.Client()
        try:
            self.client.delete("/test", recursive=True, dir=True)
        except EtcdKeyNotFound:
            pass

    @raises(EtcdKeyNotFound)
    def test_delete_missing(self):
        self.client.delete("/test")

    def test_delete(self):
        path = "/test_delete"
        value = "test"

        # Check there's nothing there
        assert_raises(EtcdKeyNotFound, self.client.read, path)

        # Set - check it doesn't raise an exceptioin
        self.client.write(path, value)
        self.client.read(path)

        # delete - check it's not there
        self.client.delete(path)
        assert_raises(EtcdKeyNotFound, self.client.read, path)

    def test_delete_recursive(self):
        basepath = "/test"
        path = "/test/recursive"
        value = "test"

        # Check there's nothing there
        assert_raises(EtcdKeyNotFound, self.client.read, basepath)

        # Set - check it doesn't raise an exception
        self.client.write(path, value)
        self.client.read(path)

        # delete - without recursive shouldn't work
        assert_raises(EtcdNotFile, self.client.delete, basepath)
        self.client.read(path)

        # delete - with recursive should work
        self.client.delete(basepath, recursive=True)
        assert_raises(EtcdKeyNotFound, self.client.read, path)

    def test_write_read(self):
        path = "/test"
        value = "value"
        self.client.write(path, value)
        result = self.client.read(path)
        assert_equal(value, result.value)


    def test_recursive_read(self):
        path1 = "/test/key1"
        path2 = "/test/key2"
        path3 = "/test/directory/key1"
        path4 = "/test/directory/key2"

        value1 = "value1"
        value2 = "value2"
        value3 = "value3"
        value4 = "value4"

        self.client.write(path1, value1)
        self.client.write(path2, value2)
        self.client.write(path3, value3)
        self.client.write(path4, value4)
        assert_equal(value1, self.client.read(path1).value)
        assert_equal(value2, self.client.read(path2).value)
        assert_equal(value3, self.client.read(path3).value)
        assert_equal(value4, self.client.read(path4).value)

        leaves = list(self.client.read("/test", recursive=True).leaves)
        clean = {}
        for leaf in leaves:
            clean[leaf.key] = leaf.value


        assert_equal(4, len(leaves))
        assert_equal(clean[path1], value1)
        assert_equal(clean[path2], value2)
        assert_equal(clean[path3], value3)
        assert_equal(clean[path4], value4)
        
        leaves = list(self.client.read("/test/directory", 
                                       recursive=True).leaves)
        clean = {}
        for leaf in leaves:
            clean[leaf.key] = leaf.value


        assert_equal(2, len(leaves))
        assert_equal(clean[path3], value3)
        assert_equal(clean[path4], value4)

    def test_append(self):
        path = "/test"
        value1 = "value1"
        value2 = "value2"
        self.client.write(path, None, dir=True)
        self.client.write(path, value1, append=True)
        self.client.write(path, value2, append=True)

        leaves = list(self.client.read("/test",
                                       recursive=True).leaves)
        clean = {}
        for leaf in leaves:
            clean[leaf.key] = leaf.value
        print clean
