


### Python Cassandra Driver 

https://datastax.github.io/python-driver/

```
pip install cassandra-driver
```

### Macos

```
 brew install libev
```

### Migrations: 

https://medium.com/@cobli/the-best-way-to-manage-schema-migrations-in-cassandra-92a34c834824




Summarizing, the cassandra-migrate tool has the following features:

Written in Python for easy installation
Does not require cqlsh, just the Python driver
Supports baselining an existing database into versions
Supports unique environments for multiple profiles
Supports partial advancement
Supports locking for concurrent instances using Lightweight Transactions
Verifies stored migrations against configured migrations
Stores content, checksum, date and state of every migration
Supports deploying with different keyspace configurations for different environments