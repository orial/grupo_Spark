from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster

cluster = Cluster()
cluster.connection_class = LibevConnection
session = cluster.connect()