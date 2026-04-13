拉取镜像

```
docker pull vllm/vllm-openai:cu130-nightly
```

运行模型

```
docker run -it --rm --name qwen3.5 --gpus all -p 9250:8000 -v D:/Python/Models:/root/models vllm/vllm-openai:cu130-nightly --model /root/models/Qwen/Qwen3.5-9B-AWQ-4bit --host 0.0.0.0 --port 8000 --gpu_memory_utilization 0.7 --max_model_len 131072 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3

```

