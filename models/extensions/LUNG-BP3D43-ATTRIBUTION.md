# BodyParts3D 4.3 lung parenchyma surfaces

Source: **BodyParts3D, © 2008 Database Center for Life Science (DBCLS)**.

- Official project: https://lifesciencedb.jp/bp3d/?lng=en
- Source OBJ download: https://lifesciencedb.jp/bp3d/download.cgi
- Official 4.3 concept mapping: https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list
- Reviewed live-source license page: https://lifesciencedb.jp/bp3d/info/license/index.html
- License: **Creative Commons Attribution-ShareAlike 2.1 Japan (CC BY-SA 2.1 JP)**, https://creativecommons.org/licenses/by-sa/2.1/jp/

This derivative geometry package follows that live 4.3 source license. It does not reinterpret a differently versioned archive's license as permission to relicense these files. The separate Atlas application and other source packages retain their own terms.

Included source objects: **FJ6595–FJ6612** (18 actual source OBJ surfaces, 17 distinct source parenchyma concepts). Source object headers and per-object hashes are retained in the manifest. FJ6595 and FJ6597 are two distinct source surfaces assigned to the same apicoposterior concept; neither was duplicated by Atlas.

Atlas preparation: converted source millimeters/Z-up to the established main Atlas meters/Y-up frame; packed original source positions and triangle indices into binary; generated signed 16-bit vertex normals by averaging face normals only at identical source positions. No deformation, fitted registration, smoothing, simplification, inferred envelope, source-vessel replacement or anatomical reconstruction. No source degenerate triangles were removed. Two used source positions with zero averaged normals receive finite fallback normals. Source ZIP is retained under `data/model-candidates/lung-surfaces/`.

Five lobe, two lung and 17 existing bronchopulmonary segment memberships follow the official 4.3 `part_of` mapping restricted to the included source surfaces. Three narrower source parenchyma aggregate mappings conflict with these memberships and are not exported or silently repaired: FMA27364 and FMA31242 omit FJ6598; FMA27363 omits FJ6608/FJ6609. The 17 direct segment parents are independently corroborated by official FMA 3.0 relation evidence pinned to cb_id=5, ci_id=1, md_id=1, mv_id=6, mr_id=1. Existing bronchi and vessels must remain in their original lung/lobe/segment concepts when merging this package.

Quality limits: an individual male source reference; visible segment seams; four non-manifold edges in FJ6598 after exact-position weld. This is not a clinical segmentation, guaranteed watertight manifold, complete microscopic parenchyma model, or anatomical expert certification.

Captured source evidence (SHA-256):

- Source ZIP: `ac848958f321318aa87cb0f8d2ca7cc590637ce52b3ba063f90a4b7e2c46baa4`
- Thoracic reference ZIP: `a688d2c76d1622cc999b7040f28a8a870dac643ba51fe91866bdf813e814dd40`
- Official mapping ZIP: `fa6e9d5c92ed1e5bb86dcabfc5f5e039fdd9130ce28f05f1c33c71699e8f768a`
- Extracted mapping payload: `c3d16c891016da13447de2fc3241d05d92e8f9dc460e363233c03f420b935d4f`
- License HTML: `63d46abcf1b112da9f2d587677d0f4edb7d1654a3c9a8a2bfd1c3d080340512e`
