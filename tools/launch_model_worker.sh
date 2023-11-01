set -e
source ./tools/set_env.sh
model_path=/mnt/nas/share-map/common/models/llm/llava/llava-v1.5-13b
python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path ${model_path} --load-4bit > output/worker.log 2>&1 &