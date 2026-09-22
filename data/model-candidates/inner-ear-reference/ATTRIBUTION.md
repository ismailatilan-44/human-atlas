# Independent inner-ear reference — retained source licenses

Source objects: `Cochlea.l/.r`, `Vestibule.l/.r`, and `Temporal bone.l/.r` from `Z-Anatomy/Startup.blend` in the [Z-Anatomy source archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip). Source blend SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

The package is restricted to **noncommercial use**, preserving each component's attribution and share-alike terms. Its separate temporal-bone meshes are not relicensed under the inner-ear license.

## Inner-ear surfaces

The upstream [license and attribution file](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/License.txt) identifies the University of Dundee School of Medicine's **Anatomy of the Inner Ear** as referenced/included/adapted under **CC BY-NC-SA 4.0**. This package conservatively assigns that narrower scope to `Cochlea.l/.r` and `Vestibule.l/.r`.

This association is **an inference from archive-level component attribution**. The individual objects contain no source-author or license certificate. It is not proof that these exact meshes were independently verified by Dundee, nor commercial-use clearance.

[Dundee's primary source](https://www.dundee.ac.uk/tilt/medical-illustration/anatomy-inner-ear) credits Annie Campbell (medical artist), Dr Patrick Spielmann (content expert), and Dr Penny Lockwood and Dr David Stewart (reviewers). It identifies its model as a derivative of **3D Ear** by W. Robert J. Funnell, Sam Daniel and Daren Nicolson at McGill University, under CC BY-NC-SA 1.0; Dundee licenses its derivative under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Temporal-bone context

**Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA 4.0**; Gauthier Kervyn (design, 3D, anatomy), with Z-Anatomy contributors. Underlying attribution retained as requested upstream: **BodyParts3D — The Database Center for Life Science — CC BY-SA 2.1 Japan**; Kousaku Okubo (original BodyParts3D model). The two temporal-bone meshes retain the archive's general [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) declaration. No object-specific source lineage is supplied upstream.

## Adaptations

Authored viewport subdivision was evaluated for the four ear objects. The two temporal bones have no modifiers. Source world transforms were applied, mirrored winding corrected, polygons triangulated, smooth normals calculated and quantized, and positions packed as float32 with gzip compression. Original base geometry is also retained as source-world OBJ files. All objects retain their original shared world coordinates; there is no scaling, recentering, registration to another skull, local deformation or additional smoothing. QA renders alter colors/transparency for visibility only. No additional anatomy was created.

Keep this notice and UPSTREAM-LICENSE.txt with all redistributed copies and derived renders.
