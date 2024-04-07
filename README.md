This repo has a Dockerfile with MariaDB build dependencies to build bb-11.4-vec-vicentiu branch.

That will compile mariadb, then expose the socket and port.

docker build -t mariadb-vector -f docker/Dockerfile docker/

docker run -v ./socket:/tmp/ -v ./server:/mariadb/server -p 3306:3306 -it mariadb-vector bash

From within container run ./docker/clone_and_install.sh and ./docker/prepare_data.sh.

Create python venv locally with the requirements.txt.
run load_embeddings.py
run q_and_a.py -> Ask a question, get an answer
