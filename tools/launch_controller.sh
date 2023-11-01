set -e
source ./set_env.sh
python -m llava.serve.controller --host 0.0.0.0 --port 10000