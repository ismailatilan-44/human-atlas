# Upper-limb BodyParts3D 4.3 bounded intake v1

Observed HEAD: `0ac477f2a686991bcb4f4d2a72267c9243547433`. Inspected/acquired 2026-10-02. This directory is the sole write scope. No active main identifiers, registry, labels, relationships, app, public assets or Git state were changed. Root owns subsequent selection and integration; geometry/registration/anatomical acceptance remain pending.

## Decision

**The left medial and lateral cord alternatives have materially better independent source identity evidence.** Actual official OBJ files name the lateral cord FJ4274/BP29122/FMA45239 and medial cord FJ4275/BP29196/FMA45241. Fresh official FMA 3.0 `is_a` rows for those concepts each contain the corresponding one FJ object. This is stronger evidence than trying to reinterpret Startup.blend terminal nerve endpoints as absent separately named cords. It does not establish source anatomy, continuity or registration to the existing atlas.

**C5–T1 root contributions remain unresolved.** Five actual source OBJ files carry separate C5/C6/C7/C8/first-thoracic nerve-trunk names and specific returned IDs. These improve spinal-level identification, but a spinal nerve trunk is not automatically its ventral ramus or its isolated brachial-plexus contribution. No root labels or branch relations are proposed from their positions, names or connectivity.

The 17 acquired neural FJ IDs do not occur among active BodyParts3D 4.0 mesh IDs. Candidate352 target links retain existing representations as comparison evidence; the new source files are an unregistered dataset candidate, not substitutions for active IDs. No right-side counterpart is positively identified or acquired in this bounded catalog audit; this is not a source-wide or anatomical absence claim and does not authorize mirroring.

## Phase1: selected neural objects

Normal public selected-object download retrieved 17 OBJ files in a 550,225-byte ZIP. `phase1-intake.json` preserves the completed first-phase snapshot before context acquisition; current `proposal.json` adds context and later audit qualifiers. Original OBJ bytes and source ZIP remain unchanged.

| FJ | Returned BP / FMA | Official returned name | Vertices / faces | Index components |
|---|---|---|---|---|
| FJ4171 | BP29488 / FMA37074 | Left axillary nerve | 481 / 654 | 10 |
| FJ4172 | BP29806 / FMA37071 | Left radial nerve | 327 / 576 | 6 |
| FJ4185 | BP29040 / FMA65908 | Left second intercostobrachial nerve | 1388 / 1568 | 81 |
| FJ4222 | BP29235 / FMA79667 | Trunk of left long thoracic nerve | 930 / 1560 | 8 |
| FJ4223 | BP29528 / FMA65295 | Left medial pectoral nerve | 1871 / 2300 | 76 |
| FJ4240 | BP29806 / FMA37071 | Left radial nerve | 2280 / 4474 | 7 |
| FJ4242 | BP29426 / FMA65306 | Left superior subscapular nerve | 730 / 916 | 31 |
| FJ4243 | BP29488 / FMA37074 | Left axillary nerve | 310 / 360 | 18 |
| FJ4245 | BP29808 / FMA7023 | Trunk of left first thoracic nerve | 256 / 344 | 5 |
| FJ4256 | BP29546 / FMA65292 | Left thoracodorsal nerve | 1472 / 2068 | 36 |
| FJ4258 | BP29812 / FMA37321 | Left ulnar nerve | 2242 / 4406 | 3 |
| FJ4264 | BP29324 / FMA24105 | Trunk of left fifth cervical nerve | 1005 / 1926 | 2 |
| FJ4265 | BP29315 / FMA7011 | Trunk of left sixth cervical nerve | 621 / 1106 | 9 |
| FJ4266 | BP29366 / FMA7013 | Trunk of left seventh cervical nerve | 525 / 956 | 3 |
| FJ4267 | BP29406 / FMA7015 | Trunk of left eighth cervical nerve | 559 / 970 | 7 |
| FJ4274 | BP29122 / FMA45239 | Lateral cord of left brachial nerve plexus | 209 / 348 | 5 |
| FJ4275 | BP29196 / FMA45241 | Medial cord of left brachial nerve plexus | 913 / 1708 | 11 |

Source mesh checks establish actual nonempty file availability: finite vertices, valid face indices, source-millimetre bounds, catalog vertex/face count parity and version-matched concept memberships. They do not establish quality or full anatomical extent. The cord files have 5 and 11 index-connected components; this may reflect disconnected pieces or source seams and requires geometry audit. Component counts are never assigned to named anatomical branches.

Radial nerve uses two distinct files, and axillary nerve two distinct files. Duplicate source names/shared BP concepts do not make those files interchangeable. Returned radial FMA37071 has a five-object `part_of` membership, including three digital-branch files beyond the two acquired here; the selection is not called a complete radial nerve model. Long thoracic is explicitly a trunk file. Intercostobrachial is explicitly the second nerve; it is not generalized to all intercostobrachial branches.

Ten further matching catalog rows, including source plexus trunks/posterior cord, radial digital branches and subclavian nerve trunk, remain `catalogOnlyObservations`. Their exact rows and 4.3 membership are recorded, but no downloaded-mesh availability or geometry claim is made. Bounded target query records include named collateral/cutaneous requirements even where no positive downloaded binding emerged.

## Requested versus returned identity

All 17 retained catalog FMA values differ from the official OBJ headers. This reflects broad/unsided source-catalog assignments such as FMA11195 or FMA55665; those values must not override the actual returned header and corresponding official membership rows. Four representation IDs also differ: FJ4172/FJ4240 radial BP29538→BP29806, FJ4245 first-thoracic trunk BP29286→BP29808, and FJ4258 ulnar BP29523→BP29812. Full request/catalog/returned values are kept for every file. The returned English names match retained catalog names; the identity discrepancy is not hidden by renaming.

Fresh `FMA2Obj.txt` declares Data Version 4.3, Objects set 4.3 and FMA 3.0. Extracted payload SHA256 `c3d16c891016da13447de2fc3241d05d92e8f9dc460e363233c03f420b935d4f` exactly matches the retained mapping. Source ZIP timestamps may vary, so individual OBJ hashes are the stable member-byte evidence. No 4.0 FMA naming table was used to reinterpret 4.3 source identities.

## Phase2: bounded same-source bone context

Root requested this separate phase after the 17-object intake. Six files were fetched through the same official endpoint; three C5/C6/C7 vertebrae were reused byte-for-byte from the retained official thyroid-reference ZIP, whose original retrieval is documented as 2026-09-22. Each reused file independently passes its 4.3 compatibility header and fresh mapping check. These are inspected cached files, not fresh downloads.

| FJ | Returned BP / FMA | Name | Acquisition |
|---|---|---|---|
| FJ3158 | BP23701 / FMA9165 | First thoracic vertebra | fresh_official_selected_download |
| FJ3167 | BP23524 / FMA12523 | Fifth cervical vertebra | reused_retained_official_source_zip |
| FJ3170 | BP24077 / FMA12524 | Sixth cervical vertebra | reused_retained_official_source_zip |
| FJ3172 | BP23626 / FMA12525 | Seventh cervical vertebra | reused_retained_official_source_zip |
| FJ3228 | BP22221 / FMA7987 | Left first rib | fresh_official_selected_download |
| FJ3229 | BP22527 / FMA8012 | Left second rib | fresh_official_selected_download |
| FJ3237 | BP23283 / FMA13323 | Left clavicle | fresh_official_selected_download |
| FJ3262 | BP24066 / FMA23131 | Left humerus | fresh_official_selected_download |
| FJ3279 | BP23279 / FMA13396 | Left scapula | fresh_official_selected_download |

The context is left scapula/clavicle/humerus, left first/second ribs and C5/C6/C7/T1 vertebrae. C8 denotes a spinal nerve, not a fabricated eighth cervical vertebra. Retained catalog duplicate-name clavicle/humerus companion FJ objects were not substituted or silently treated as the selected components; selected source membership is recorded exactly.

All nine context files have nonzero finite mesh coordinates and source `Bounds(mm)` headers. Same FJ IDs also exist in main 4.0 and their current metadata are recorded for a future actual geometry/frame comparison. Shared IDs and plausible bounds do not prove identical geometry, common pose, fit, or registration. No conversion, fit, rotation, mirroring, topology edit or anatomical contact inference was performed.

## Provenance, rights and checks

[BodyParts3D / DBCLS](https://lifesciencedb.jp/bp3d/) is the official source. The [live license page](https://lifesciencedb.jp/bp3d/info_en/license/index.html) was independently read and captured on 2026-10-02; it identifies [CC BY-SA 2.1 Japan](https://creativecommons.org/licenses/by-sa/2.1/jp/) and requires source credit. Captured license SHA256 `63d46abcf1b112da9f2d587677d0f4edb7d1654a3c9a8a2bfd1c3d080340512e` matches the prior source review. See `ATTRIBUTION.md`. This intake preserves original source bytes and attribution; no public derivative is activated. Source frame/demographic detail beyond the OBJ metadata is not established here.

Requests used the documented public viewer session followed by `download.cgi` POST with exact FJ/representation lists. No authentication or restriction bypass occurred. `source-fetch.json` and `context-fetch.json` record URLs, successful status, dates, byte counts and hashes; request files preserve exact fields. `fetch.py` and `fetch-context.py` are bounded acquisition scripts and refuse source-archive overwrite. `build.py` has no network calls.

Validation run: deterministic generation and `python3 data/model-candidates/upper-limb-bp3d43-intake-v1/build.py --check`; 17 exact requested neural files; 9 exact requested/reused context files; nonempty meshes, finite coordinates, index ranges, declared mm and 4.3 versions; catalog count/name parity; official returned FMA membership including exact declared `is_a`/`part_of` logic; input/member hashes; candidate 352 target endpoints; active 4.0 FJ comparison. These are basic file and metadata checks only. Mesh quality/visual review, registration, anatomical expert acceptance, labels, relations and release acceptance are zero/pending. Timing and identity-discrepancy rework are in `timing.json`.

Next: geometry owner audits the left cord and terminal nerve components with these exact source-frame bones, explicitly testing extent/continuity and 4.0 coordinate compatibility. Root chooses an accepted candidate only after that evidence; isolated C5–T1 contributions remain a separate unresolved decision.
