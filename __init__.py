"""
ComfyUI-TorchMonitor
Zero-config, fixed position, nvidia-smi, no console spam
"""
import json, os, time, psutil, subprocess, threading, shutil
import torch
from server import PromptServer   # 仅用于挂脚本

INTERVAL = 2
JSON_FILE = os.path.join(os.path.dirname(__file__), "web", "extensions", "torch_monitor.json")
os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
_STOP = threading.Event()

def _gpu():
    if not torch.cuda.is_available():
        return {"gpu": "No GPU"}
    try:
        out = subprocess.check_output([
            "nvidia-smi", "--query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu",
            "--format=csv,noheader,nounits"
        ], encoding="utf-8", timeout=3).strip()
        used, total, util, temp = map(int, out.split(", "))
        return {"gpu": f"RTX 3090  {used}/{total}MB  {util}%  {temp}°C"}
    except Exception:
        return {"gpu": "GPU Error"}

def _write():
    while not _STOP.is_set():
        data = {
            "cpu": f"{psutil.cpu_percent(interval=None):.1f}%",
            "ram": f"{psutil.virtual_memory().percent:.1f}%",
            **_gpu()
        }
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        time.sleep(INTERVAL)

# 注册前端脚本（官方 extensions 目录已自动映射）
PromptServer.instance.app.router.add_static("/extensions", path=os.path.join(os.path.dirname(__file__), "web", "extensions"))

# 启动后台线程
threading.Thread(target=_write, daemon=True).start()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "web"
