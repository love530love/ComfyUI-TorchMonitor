/* ComfyUI-TorchMonitor 固定标题栏版 */
import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ComfyUI.TorchMonitor",
    setup() {
        const mon = document.createElement("button");
        mon.id = "torch-monitor";
        mon.style.cssText = `
            display:inline-flex;align-items:center;gap:6px;
            padding:6px 12px;margin:0 4px;
            background:transparent;border:2px solid rgba(255,255,255,0.3);
            border-radius:8px;cursor:default;font-size:13px;color:#00ff88;
            font-weight:500;text-shadow:1px 1px 2px rgba(0,0,0,0.8);
        `;
        mon.textContent = "TorchMonitor Loading...";

        /* 等待 AITechLab 按钮出现，插到它前面 */
        const wait = () => {
            const ref = document.querySelector("#dapao-main-button");
            if (!ref) { setTimeout(wait, 200); return; }
            ref.parentNode.insertBefore(mon, ref);
        };
        wait();

        /* 轮询 JSON（官方 /extensions 已存在） */
        async function poll() {
            try {
                const j = await fetch("/extensions/torch_monitor.json?t=" + Date.now()).then(r => r.json());
                mon.textContent = `CPU ${j.cpu} | RAM ${j.ram} | ${j.gpu}`;
            } catch {}
        }
        setInterval(poll, 2000); poll();
    }
});
