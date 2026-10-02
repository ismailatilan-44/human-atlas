---
name: anatomy-imaging-to-mesh
description: Derive or assess anatomical 3D structures from licensed CT, MRI, or cadaveric image stacks using segmentation, registration, and expert review. Use when existing mesh sources lack a required structure.
---

# Anatomy imaging to mesh

Use this workflow only for a named gap with required detail and an image source whose permitted use and subject context are recorded. Keep source image, segmentation mask, corrected mask, registered surface, and web export as distinct versions. Preserve modality, voxel spacing, orientation, subject/donor, and coordinate transforms; never align a donor-specific organ to another body by appearance alone.

Use 3D Slicer for slice-by-slice inspection and corrections. TotalSegmentator or MONAI Label can generate a candidate mask where their task and license fit; the output still needs anatomical review. Register images or surfaces with an explicit transform and check multiple landmarks, not just one view. Export a surface only after inspecting continuity, boundaries, neighboring structures, and laterality in the original slices.

Record the segmentation method, source series, software/model version, corrections, transformation, uncertainty, and expert acceptance. If image resolution cannot support the requested detail, report that limit rather than generating a precise-looking structure. Educational model acceptance is not a clinical validation claim.
