```
docker pull lmsysorg/sglang:dev-cu13
```

```
docker run -it --rm --name qwen3.5 --gpus all -p 9250:30000 -v D:/Python/Models:/root/models lmsysorg/sglang:dev-cu13 python3 -m sglang.launch_server --model-path /root/models/Qwen/Qwen3.5-9B-AWQ-4bit --host 0.0.0.0 --port 30000 --mem-fraction-static 0.7 --context-length 131072 --tp-size 1
```

