# BodyParts3D 4.3 thyroid candidate attribution

BodyParts3D, Copyright © The Database Center for Life Science, licensed by Creative Commons Attribution-Share Alike 2.1 Japan (CC BY-SA 2.1 JP).

- Official live dataset: https://lifesciencedb.jp/bp3d/?lng=en
- Official live license: https://lifesciencedb.jp/bp3d/info_en/license/index.html
- License deed: https://creativecommons.org/licenses/by-sa/2.1/jp/deed.en
- Source download: https://lifesciencedb.jp/bp3d/download.cgi
- Versioned source mapping: https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list

This separate derivative retains the live dataset's stated CC BY-SA 2.1 Japan license. The archive website's newer CC BY 4.0 statement is not used to silently relicense these live 4.3 files. The source ZIP, official mapping, license capture, hashes and retrieval recipe are preserved in `data/model-candidates/thyroid-bp3d43/`.

Source surfaces: FJ3671 (FMA13369, left thyroid lobe), FJ3672 (FMA13368, right thyroid lobe), FJ3670 (FMA49178, thyroid isthmus). Their union is FMA9603 in the official 4.3 part-of mapping.

Changes: convert millimetres/Z-up to the existing atlas's metre/Y-up frame, derive display normals at coincident positions, encode Float32 positions / Int16 normals / Uint32 triangle indices and gzip. Original positions and triangles are retained subject to Float32 encoding; no anatomical reshaping, added subdivision or decimation. Separate review images color the three parts and show actual BodyParts3D atlas neck context. These images are also CC BY-SA 2.1 Japan.

This is a source-preserving candidate for anatomy education review. Expert acceptance is pending. It does not include parathyroids, vessels, nerves, fascia or a pyramidal lobe, and does not claim universal normal morphology or clinical accuracy.
