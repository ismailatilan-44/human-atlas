/** Static hosts may serve .gz as a compressed response or as a gzip file.
 * Fetch already decodes Content-Encoding; inspect the payload to avoid decoding twice.
 */
export async function decodeModelResponse(
  response: Response,
  expectedBytes: number,
  compressed: boolean,
): Promise<ArrayBuffer> {
  if (!response.ok) throw new Error('An anatomy file could not be loaded.');
  const payload = await response.arrayBuffer();
  const signature = new Uint8Array(payload, 0, Math.min(2, payload.byteLength));
  const gzip = compressed && signature[0] === 0x1f && signature[1] === 0x8b;
  const buffer = gzip
    ? await new Response(new Blob([payload]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer()
    : payload;
  if (buffer.byteLength !== expectedBytes)
    throw new Error('An anatomy file was incomplete. Please try loading it again.');
  return buffer;
}

/** A failed or abandoned atlas must stop every worker, including queued chunks. */
export async function loadModelChunks(
  count: number,
  signal: AbortSignal,
  load: (index: number, signal: AbortSignal) => Promise<void>,
): Promise<void> {
  const abort = new AbortController();
  const cancel = () => abort.abort(signal.reason);
  if (signal.aborted) cancel();
  else signal.addEventListener('abort', cancel, { once: true });
  let cursor = 0;
  try {
    abort.signal.throwIfAborted();
    await Promise.all(Array.from({ length: Math.min(3, count) }, async () => {
      try {
        while (cursor < count) {
          abort.signal.throwIfAborted();
          await load(cursor++, abort.signal);
          // Decoding may finish after fetch has already delivered its response.
          abort.signal.throwIfAborted();
        }
      } catch (error) {
        abort.abort(error);
        throw error;
      }
    }));
  } finally {
    signal.removeEventListener('abort', cancel);
  }
}
