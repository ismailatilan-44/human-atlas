import type { WebGLRenderer } from "three";

/** Opt-in, local diagnostics. CPU submission timing is not GPU time or device acceptance. */
export function createPerformanceReport(host: HTMLElement, datasetId: string, started: number) {
  if (new URLSearchParams(location.search).get("qa") !== "1") return null;
  const panel = document.createElement("output");
  panel.dataset.testid = "webgl-performance";
  panel.setAttribute("aria-label", "WebGL QA metrics");
  panel.style.cssText = "position:fixed;left:4px;bottom:4px;z-index:100;max-width:calc(100vw - 8px);padding:3px 5px;border-radius:4px;background:#fffE;color:#14232d;font:10px/1.3 monospace;pointer-events:none;white-space:pre-wrap";
  host.appendChild(panel);
  let firstModelFrame: number | null = null;
  let frames = 0;
  let lastFrame = 0;
  let contextLost = false;
  let calls = 0;
  let triangles = 0;
  let pixelRatio = 0;
  const cpuSamples: number[] = [];
  const activeIntervals: number[] = [];
  const p95 = (samples: number[]) => {
    const sorted = [...samples].sort((a, b) => a - b);
    return sorted.length ? Number(sorted[Math.ceil(sorted.length * 0.95) - 1].toFixed(2)) : null;
  };
  const publish = () => {
    const metrics = {
      datasetId, frames, firstModelFrameMs: firstModelFrame,
      drawCalls: calls, triangles, pixelRatio,
      renderCpuP95Ms: p95(cpuSamples), activeFrameIntervalP95Ms: p95(activeIntervals),
      sampleCount: cpuSamples.length, contextLost,
      viewport: `${host.clientWidth}x${host.clientHeight}`,
    };
    panel.dataset.metrics = JSON.stringify(metrics);
    panel.textContent = `QA ${datasetId} | ${metrics.viewport} @${pixelRatio}\nmodel ${firstModelFrame ?? "loading"}ms | draws ${calls} | triangles ${triangles}\nCPU p95 ${metrics.renderCpuP95Ms ?? "—"}ms | active interval p95 ${metrics.activeFrameIntervalP95Ms ?? "—"}ms | frames ${frames}${contextLost ? " | CONTEXT LOST" : ""}`;
  };
  publish();
  const timer = window.setInterval(publish, 1000);
  return {
    rendered(renderer: WebGLRenderer, cpuMs: number, allChunksLoaded: boolean) {
      const now = performance.now();
      frames++;
      calls = renderer.info.render.calls;
      triangles = renderer.info.render.triangles;
      pixelRatio = renderer.getPixelRatio();
      if (allChunksLoaded) {
        if (firstModelFrame === null) firstModelFrame = Math.round(now - started);
        cpuSamples.push(cpuMs);
        // Exclude deliberate draw-on-change idle gaps; this is not a continuous FPS claim.
        if (lastFrame && now - lastFrame < 250) activeIntervals.push(now - lastFrame);
        if (cpuSamples.length > 180) cpuSamples.shift();
        if (activeIntervals.length > 180) activeIntervals.shift();
        lastFrame = now;
      }
    },
    contextLost() { contextLost = true; publish(); },
    dispose() { window.clearInterval(timer); panel.remove(); },
  };
}
