set -e
source ./tools/set_env.sh
mkdir -p output
pkill -9 -f llava.serve
model_path=/mnt/nas/share-map/common/models/llm/llava/llava-v1.5-13b
python -m llava.serve.controller --host 0.0.0.0 --port 10000 > output/controller.log 2>&1 &
sleep 30
python -m llava.serve.model_worker --host 0.0.0.0 --controller http://0.0.0.0:10000 --port 40000 --worker http://0.0.0.0:40000 --model-path ${model_path} --load-4bit > output/worker.log 2>&1 &
