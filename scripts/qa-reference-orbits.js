async (page) => {
  const url = new URL(page.url());
  if (!['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) || url.searchParams.get('devqa') !== '1') throw new Error('Local devqa fixture required');
  const cases = [
    ['female-pelvis', 'Sakrum (sağrı kemiği)', 'Sol yumurtalık'],
    ['inner-ear-reference', 'Sol temporal kemik (şakak kemiği)', 'Sol koklea (salyangoz)'],
    ['lower-limb-nerve-reference', 'Sağ Kaval kemiği', 'Sağ Tibial sinir'],
    ['upper-limb-nerve-reference', 'Sağ Humerus', 'Sağ Ulnar sinir'],
  ];
  const result = [];
  const button = name => (name === 'Çevreyi göster' ? page.locator('.primary-action').filter({ hasText: name }) : page.getByRole('button', { name, exact: true })).click();
  const snap = async () => {
    await button('Snapshot');
    return JSON.parse(await page.getByTestId('qa-snapshot').textContent());
  };
  const dir = c => { const v = c.position.map((n, i) => n - c.target[i]); const l = Math.hypot(...v); return v.map(n => n / l); };
  const delta = (a, b) => Math.max(...a.map((n, i) => Math.abs(n - b[i])));
  let selectionCheckpoint = null;
  const select = async name => {
    await button('Anatomi ara');
    await page.getByRole('combobox', { name: 'Anatomik yapı ara', exact: true }).fill(name);
    await page.waitForTimeout(600); // The readable fixture snapshot refreshes every 350ms, including while search is modal.
    selectionCheckpoint = JSON.parse(await page.getByTestId('qa-snapshot').textContent());
    await page.getByRole('option', { name: `${name} 1 parça`, exact: true }).click();
    await page.waitForTimeout(350);
  };
  for (const width of [1200, 390, 320]) {
    const height = width === 1200 ? 942 : width === 390 ? 844 : 568;
    await page.setViewportSize({ width, height });
    for (const [reference, bone, structure] of cases) {
      await page.reload();
      await page.getByRole('combobox', { name: 'Anatomi referansı', exact: true }).selectOption(reference);
      await page.getByRole('button', { name: 'Kayıtlı sahneler', exact: true }).waitFor({ state: 'visible' });
      await select(bone);
      await button('DEV ONLY · QA sandbox −');
      const x = width === 1200 ? 530 : width / 2, y = width === 1200 ? 380 : width === 390 ? 280 : 230;
      await page.mouse.move(x, y); await page.mouse.down();
      await page.mouse.move(x + 45, y + 18, { steps: 12 }); await page.mouse.up();
      await page.waitForTimeout(2600);
      await button('DEV ONLY · QA sandbox +');
      const initial = await snap(), steps = [];
      const act = async (name, action, undo = true) => {
        const before = await snap(); selectionCheckpoint = null; await action(); const checkpoint = selectionCheckpoint ?? before; await page.waitForTimeout(400); const after = await snap();
        const record = { name, before, checkpoint, after, directionTolerance: name === 'bone to structure' ? 1e-3 : 1e-5, directionDelta: delta(dir(before.camera), dir(after.camera)) };
        if (undo) {
          await button('Önceki görünüme dön'); await page.waitForTimeout(400); const back = await snap();
          record.undoDelta = Math.max(delta(checkpoint.camera.position, back.camera.position), delta(checkpoint.camera.target, back.camera.target));
          record.undoMatches = checkpoint.conceptId === back.conceptId && JSON.stringify(checkpoint.visibility) === JSON.stringify(back.visibility) && JSON.stringify(checkpoint.camera.viewOffset) === JSON.stringify(back.camera.viewOffset);
          await action(); await page.waitForTimeout(400);
        }
        steps.push(record);
      };
      await act('bone to structure', () => select(structure));
      await act('isolate structure', () => button('Yapıyı yalnız göster'));
      await button('DEV ONLY · QA sandbox −');
      await page.screenshot({ path: `output/playwright/reference-structure-${reference}-${width}.png` });
      await button('DEV ONLY · QA sandbox +');
      await act('show context', () => button('Çevreyi göster'));
      await act('structure to bone', () => select(bone));
      await act('isolate bone', () => button('Yapıyı yalnız göster'));
      await act('focus', () => button('Odaklan'));
      await act('canvas pick', async () => {
        const before = await snap();
        await button('DEV ONLY · QA sandbox −');
        await page.mouse.click(width === 1200 ? 530 : width / 2, width === 1200 ? 420 : width === 390 ? 335 : reference === 'inner-ear-reference' ? 240 : 225);
        await button('DEV ONLY · QA sandbox +');
        const picked = await snap();
        if (picked.explorerHistory !== before.explorerHistory + 1) throw new Error(`No geometry picked: ${reference}/${width}`);
      });
      await button('DEV ONLY · QA sandbox −');
      await page.screenshot({ path: `output/playwright/reference-orbit-${reference}-${width}.png` });
      await button('DEV ONLY · QA sandbox +');
      const saved = await snap();
      await button('Sahneyi kaydet');
      const sceneName = 'Reference orbit fixture';
      const oldCopies = page.getByRole('button', { name: `${sceneName} kaydını sil`, exact: true });
      while (await oldCopies.count()) await oldCopies.last().click();
      await page.getByRole('textbox', { name: 'Sahne adı', exact: true }).fill(sceneName);
      await button('Bu sahneyi kaydet'); await button('Kayıtlı sahneleri kapat');
      await page.getByRole('combobox', { name: 'Anatomi referansı', exact: true }).selectOption(reference === 'female-pelvis' ? 'inner-ear-reference' : 'female-pelvis');
      await button('Kayıtlı sahneler'); await button(`Devam et · ${sceneName}`); await page.waitForTimeout(600);
      const restored = await snap();
      const restoreDelta = Math.max(delta(saved.camera.position, restored.camera.position), delta(saved.camera.target, restored.camera.target));
      const restoreMatches = saved.reference === restored.reference && saved.conceptId === restored.conceptId && JSON.stringify(saved.visibility) === JSON.stringify(restored.visibility) && JSON.stringify(saved.camera.viewOffset) === JSON.stringify(restored.camera.viewOffset);
      steps.push({name:'cross-reference saved return',before:saved,after:restored,directionDelta:delta(dir(saved.camera),dir(restored.camera)),undoDelta:restoreDelta,undoMatches:restoreMatches});
      await act('hide and return', () => button('Parçayı gizle'));
      await button('Önceki görünüme dön'); await page.waitForTimeout(400);
      await act('clear selection', () => button('Seçimi temizle'), false);
      result.push({ reference, width, initial, steps, failures: steps.filter(s => s.directionDelta > (s.directionTolerance ?? 1e-5) || s.undoDelta > 1e-5 || s.undoMatches === false).map(s => s.name) });
    }
  }
  return { passed: result.every(r => r.failures.length === 0), result };
}
