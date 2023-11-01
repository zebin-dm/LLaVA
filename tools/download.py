from huggingface_hub import snapshot_download

model_path = "/mnt/nas/share-map/common/models/llm/llava/test"
cache_path = "/mnt/nas/share-all/caizebin/07.cache/hf_home"

snapshot_download(
    repo_id="liuhaotian/llava-v1.5-13b",
    local_dir=model_path,
    resume_download=True,
    etag_timeout=1000,
)
