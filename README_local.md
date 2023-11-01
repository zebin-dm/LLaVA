# start contariner
bash artifacts/create_container.sh
# install depency
pip install -e .
# start server
bash tools/start.sh
# stop server
bash tools/stop.sh