export CUDA_VISIBLE_DEVICES=0
docker build -t zebincai/llava:latest -f artifacts/dev.Dockerfile .
