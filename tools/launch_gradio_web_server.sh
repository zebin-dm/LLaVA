set -e
source ./set_env.sh
python -m llava.serve.gradio_web_server --controller http://localhost:10000 --model-list-mode reload