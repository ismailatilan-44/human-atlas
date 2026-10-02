# Browser performance measurement contract

The optional `?qa=1` query adds a local, noninteractive diagnostic output. No account, telemetry request, GPU fingerprint or persisted measurement is created. Normal rendering retains draw-on-change behavior; the measurement timer and render timestamps are absent without the flag. Changing reference destroys the prior report and starts a new measurement.

Read the visible `output[data-testid="webgl-performance"]` or its `data-metrics` JSON through the browser DOM. Pair metrics with a screenshot demonstrating loaded anatomy and selection/focus/isolation/return. A metric alone is not visual acceptance.

| Metric | Meaning and limit |
| --- | --- |
| `firstModelFrameMs` | Scene mount through first draw after all geometry chunks load; includes fetch, decoding, assembly and WebGL submission. Excludes preceding manifest/UI fetch and does not prove GPU completion. Record cold/warm cache explicitly. |
| `drawCalls`, `triangles` | Three.js counters from the last submitted frame. Shader-hidden triangles can remain in batches; counts are not the number of visible anatomical structures. |
| `renderCpuP95Ms` | p95 CPU time within `renderer.render`, rolling last 180 fully loaded frames. Excludes picking/React work and asynchronous GPU time. |
| `activeFrameIntervalP95Ms` | p95 interval between fully loaded submitted frames, excluding gaps of 250ms or longer. Idle draw-on-change gaps are intentionally excluded. Not a continuous FPS claim. |
| `sampleCount`, `frames` | Loaded-frame CPU sample count, and total submitted frames including initial loading. Record sample count with timing. |
| `contextLost`, `viewport`, `pixelRatio` | Actual context-loss observation, canvas-host CSS dimensions, and renderer pixel ratio. Desktop browser viewport emulation is not physical-device evidence. |

For bounded technical QA, use the existing authorized Mac Chrome at desktop, 390×844 and 320×568. Load each selected reference, perform search → selection → focus/context → relationship where supported → return, then orbit for at least three seconds and record the report after one second. Repeat a warm load once to separate network/cache effects. Record browser/environment, exact source revision and final URL alongside results.

The production transfer gate is **450,000 gzip bytes for all built JavaScript**, checked after a fresh build with `node scripts/check-performance-budget.mjs`. This limits growth from the approximately 384KB integration baseline; geometry transfer is separate and unchanged. Runtime investigation budgets on the recorded Mac browser are **≤20 seconds to fully loaded first submission**, **≤50ms CPU render p95**, **≤100ms active frame interval p95**, and **no context loss**. Runtime budgets flag investigation; they do not establish phone battery, touch latency, memory pressure or frame rate. Record a failure rather than lowering the budget to match a result.

Physical phone/tablet acceptance still requires an actual supplied device: repeat the same paths with real pinch/two-finger gestures, portrait/landscape changes, background/resume, and a ten-minute study session; record device/OS/browser, heat, tab reload/context loss, target readability and touch problems. No physical-device result is inferred from Mac Chrome.
