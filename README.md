
docker build -t mariadb-vector -f docker/Dockerfile docker/

docker run -v ./socket:/tmp/ -v ./server:/mariadb/server -p 3306:3306 -it mariadb-vector bash
