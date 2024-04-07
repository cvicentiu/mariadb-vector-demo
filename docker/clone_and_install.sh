#!/bin/bash
git clone https://github.com/MariaDB/server.git

cd server && git checkout bb-11.4-vec-vicentiu && cmake . -DCMAKE_BUILD_TYPE=RelWithDebug -DWITHOUT_CONNECT=True -DWITHOUT_ROCKSDB=True -DWITHOUT_SPIDER=True -DWITHOUT_MROONGA=True && make -j9

rm -rf ./data
scripts/mariadb-install-db --datadir=./data --skip-name-resolve
sql/mariadbd --datadir=./data --user=root &
