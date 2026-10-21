import { SKULL_GROUP, skullItems, skullParts, skullItem, skullDescription, skullViews, skullStart } from './skull';
import { learningStorage, fixtureMode } from './learning-storage';
import StudyPanel, { type StudyDiagnostics } from "./study-panel";
import { studyPacks, type StudyPack } from "./study-packs";
import SavedScenesPanel from "./saved-scenes-panel";
import { validateScene, type SavedScene } from "./saved-scenes";
import { matchesAnatomyQuery } from "./search";
import {
  REFERENCE_DATASETS,
  referenceDataset,
  referenceDescription,
  datasetLabel,
  defaultDatasetScene,
} from "./reference-datasets";
import { assetUrl } from "./asset-url";
import CoveragePanel from "./coverage-panel";
import { loadAtlas } from "./load-atlas";
import { flushSync, createPortal } from "react-dom";
import { registerAtlasTools } from "./agent-tools";
import { getRepresentationNote } from "./atlas-metadata";
import { selectionVariant } from "./reviewed-selections";
import { explorerConcepts, relationshipsFor, knowledgeSource, representationFor, relationshipScopeNotes } from "./knowledge";
import { lazy, Suspense, useEffect, useMemo, useRef, useState } from "react";
import {
  Activity,
  ArrowUpRight,
  ChevronRight,
  Focus,
  Info,
  Layers3,
  Pause,
  RotateCcw,
  RotateCw,
  Search,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Sheet, SheetContent, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import {
  Combobox,
  ComboboxInput,
  ComboboxContent,
  ComboboxList,
  ComboboxItem,
  ComboboxEmpty,
} from "@/components/ui/combobox";
import AnatomyScene from "./scene";
import {
  DEFAULT_VISIBLE,
  SYSTEMS,
  EXPLANATIONS,
  explanation,
  type Atlas,
  type DatasetId,
  type Concept,
  type SceneState,
  type SystemId,
  type View,
  type CameraPose,
} from "./anatomy";
const DevQaPanel = import.meta.env.DEV ? lazy(() => import('./dev-qa-panel')) : null;
const initial: SceneState = {
  explode: 0,
  visible: DEFAULT_VISIBLE,
  selected: [],
  isolate: false,
  view: "three-quarter",
  rotate: false,
  reset: 0,
  hidden: [],
  focused: false,
  ghost: false,
};
type ExplorerSnapshot = { dataset: DatasetId; state: SceneState; chosen: Concept | null; details: boolean;
  panel: "layers" | "search" | null; language: "tr" | "en" | "la"; camera: CameraPose | null;
  history: { state: SceneState; chosen: Concept | null; details: boolean; camera: CameraPose | null }[] };
export default function Home() {
  const qaSlowLoad = useRef(false);
  const qaStudy = useRef<StudyDiagnostics | null>(null);
  const [studying, setStudying] = useState(false);
  const [activePack, setActivePack] = useState<StudyPack>(studyPacks[0]);
  const [learningOpen, setLearningOpen] = useState(false);
  const [scenesOpen, setScenesOpen] = useState(false);
  const [pendingScene, setPendingScene] = useState<SavedScene | null>(null);
  const [sceneNotice, setSceneNotice] = useState('');
  const [pendingPack, setPendingPack] = useState<StudyPack | null>(null);
  const [lastPack, setLastPack] = useState(() => {
    try { return learningStorage().getItem('atlas.last-study-pack') ?? ''; } catch { return ''; }
  });
  const studyReturn = useRef<(() => void) | null>(null);
  const launchSnapshot = useRef<ExplorerSnapshot | null>(null);
  const [returnSnapshot, setReturnSnapshot] = useState<ExplorerSnapshot | null>(null);
  const detailTitle = useRef<HTMLHeadingElement>(null);
  const guideAction = useRef<(() => void) | null>(null);
  const guideSearchHandoff = useRef(false);
  const guideTitle = useRef<HTMLHeadingElement>(null);
  const camera = useRef<CameraPose | null>(null);
  const history = useRef<
    { state: SceneState; chosen: Concept | null; details: boolean; camera: CameraPose | null }[]
  >([]);
  const [historySize, setHistorySize] = useState(0),
    [language, setLanguage] = useState<"tr" | "en" | "la">("tr");
  const [dataset, setDataset] = useState<DatasetId>("male-body");
  const [loadAttempt, setLoadAttempt] = useState(0);
  const reference = referenceDataset(dataset);
  const [atlas, setAtlas] = useState<Atlas | null>(null),
    [state, setState] = useState(initial),
    [progress, setProgress] = useState(0),
    [error, setError] = useState(""),
    [panel, setPanel] = useState<"layers" | "search" | null>(null),
    [details, setDetails] = useState(false),
    [about, setAbout] = useState(false),
    [coverageOpen, setCoverageOpen] = useState(false),
    [query, setQuery] = useState(""),
    [chosen, setChosen] = useState<Concept | null>(null);
  useEffect(() => {
    const abort = new AbortController();
    setProgress(0);
    setError("");
    setAtlas(null);
    setChosen(null);
    setDetails(false);
    setPanel(null);
    setAbout(false);
    setCoverageOpen(false);
    setQuery("");
    history.current = [];
    camera.current = null;
    setHistorySize(0);
    setState({ ...initial, visible: DEFAULT_VISIBLE });
    loadAtlas(abort.signal, dataset)
      .then(async (loaded) => {
        if (import.meta.env.DEV && fixtureMode() && qaSlowLoad.current) await new Promise(resolve => setTimeout(resolve, 1500));
        if (!abort.signal.aborted) {
          setState({
            ...initial,
            ...defaultDatasetScene(loaded),
          });
          setAtlas(loaded);
        }
      })
      .catch((e) => {
        if (!abort.signal.aborted) {
          setError(e instanceof Error ? e.message : "Model yüklenemedi. Lütfen yeniden deneyin.");
          setPendingPack(null); setPendingScene(null);
        }
      });
    return () => abort.abort();
  }, [dataset, loadAttempt]);
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if (
        !studying && e.key === "/" &&
        !(e.target instanceof HTMLInputElement) &&
        !(e.target instanceof HTMLTextAreaElement)
      ) {
        e.preventDefault();
        setPanel("search");
        setDetails(false);
      }
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [studying]);
  const parts = useMemo(() => new Map(atlas?.parts.map((p) => [p.id, p])), [atlas]);
  const concepts = useMemo(() => (atlas ? explorerConcepts(atlas) : []), [atlas]);
  const conceptMap = useMemo(() => new Map(concepts.map((c) => [c.id, c])), [concepts]);
  const relations = useMemo(
    () => (chosen ? relationshipsFor(chosen.id, conceptMap, dataset) : []),
    [chosen, conceptMap, dataset],
  );
  const anchorMap = useMemo(() => new Map(atlas?.anchors?.map((a) => [a.conceptId, a])), [atlas]);
  const variant = chosen && !reference ? selectionVariant(chosen.id) : undefined;
  const variantConcept = variant ? conceptMap.get(variant.id) : undefined;
  const chosenAnchor = chosen ? anchorMap.get(chosen.id) : undefined;
  const label = (c: { id: string; name: string }) => datasetLabel(dataset, c.id, c.name, language);
  const remember = () => {
    history.current = [
      ...history.current.slice(-29),
      { state, chosen, details, camera: camera.current },
    ];
    setHistorySize(history.current.length);
  };
  const goBack = () => {
    const previous = history.current.pop();
    if (!previous) return;
    setState({ ...previous.state, restoreCamera: previous.camera ?? undefined, rotate: false });
    setChosen(previous.chosen);
    setDetails(previous.details);
    setPanel(null);
    setHistorySize(history.current.length);
  };
  const counts = useMemo(
    () =>
      Object.fromEntries(
        SYSTEMS.map((s) => [s.id, atlas?.parts.filter((p) => p.system === s.id).length ?? 0]),
      ),
    [atlas],
  );
  const activeSystems = SYSTEMS.filter((s) => counts[s.id] > 0);
  const selectedParts = state.selected.map((id) => parts.get(id)).filter((p) => !!p),
    selected = selectedParts[0],
    system = SYSTEMS.find((s) => s.id === selected?.system);
  const visibleCount =
    atlas?.parts.filter(
      (p) =>
        (!state.skull || skullParts.includes(p.id)) && !state.hidden?.includes(p.id) &&
        (state.isolate
          ? state.selected.includes(p.id)
          : state.visible.includes(p.system) || state.selected.includes(p.id)),
    ).length ?? 0;
  const results = useMemo(() => {
    if (!atlas) return [];
    const term = query.trim();
    if (!term && reference) return concepts;
    if (!term)
      return [
        "heart",
        "brain",
        "liver",
        "stomach",
        "spleen",
        "pancreas",
        "urinary bladder",
        "trachea",
      ]
        .map((name) => atlas.concepts.find((c) => c.name.toLowerCase() === name))
        .filter((x): x is Concept => !!x);
    return concepts
      .filter((c) => matchesAnatomyQuery(dataset, c, term))
      .sort((a, b) => a.name.length - b.name.length)
      .slice(0, 80);
  }, [atlas, concepts, query, dataset, reference]);
  const choose = (c: Concept, preserveIsolation = false, fromCanvas = false) => {
    const anchor = anchorMap.get(c.id);
    const skullSelection = dataset === 'male-body' && (c.id === SKULL_GROUP || !!skullItem(c.id));
    const retainSkull = !!state.skull && skullSelection;
    remember();
    setChosen(c);
    setState((s) => ({
      ...s,
      ...(skullSelection && !s.skull ? skullStart(s) : {}),
      skull: skullSelection ? (s.skull ?? {}) : undefined,
      selected: c.elements,
      anchor: anchor ? { ...anchor, label: label(c) } : undefined,
      ghost: anchor ? true : s.ghost,
      isolate: retainSkull || preserveIsolation ? s.isolate : false,
      focused: skullSelection ? (retainSkull ? s.focused : false) : fromCanvas && s.explode === 0 ? s.focused : c.elements.length > 0 || !!anchor,
      explode: 0,
      rotate: false,
      hidden: skullSelection && !s.skull ? [] : s.hidden?.filter((id) => !c.elements.includes(id)),
      restoreCamera: (retainSkull && !s.isolate) || (fromCanvas && s.explode === 0) ? camera.current ?? undefined : undefined,
    }));
    setDetails(true);
    setPanel(null);
  };
  const chooseLatest = useRef(choose);
  chooseLatest.current = choose;
  useEffect(() => {
    if (!atlas || studying) return;
    return registerAtlasTools({ ...atlas, concepts }, (c) =>
      flushSync(() => chooseLatest.current(c)),
    );
  }, [atlas, concepts, studying]);
  const choosePart = (id: string, fromCanvas = false) => {
    const p = parts.get(id);
    if (!p) return;
    choose({ id: p.conceptId, name: p.name, elements: [id] }, false, fromCanvas);
  };
  const setLayers = (visible: SystemId[]) => {
    remember();
    setDetails(false);
    setChosen(null);
    setState((s) => ({
      ...s,
      visible,
      skull: undefined,
      selected: [],
      anchor: undefined,
      focused: false,
      isolate: false,
      ghost: false,
      restoreCamera: undefined,
    }));
  };
  const toggle = (id: SystemId) =>
    setLayers(
      state.visible.includes(id) ? state.visible.filter((x) => x !== id) : [...state.visible, id],
    );
  const reset = () => {
    remember();
    setState((s) => ({
      ...initial,
      ...(atlas ? defaultDatasetScene(atlas) : { visible: DEFAULT_VISIBLE }),
      reset: s.reset + 1,
    }));
    setChosen(null);
    setDetails(false);
    setPanel(null);
  };
  const skullAction = (action: 'assemble' | 'separate' | 'start') => {
    remember();
    if (action === 'start') {
      setChosen(conceptMap.get(SKULL_GROUP) ?? null);
      setState(s => skullStart(s)); setDetails(true); return;
    }
    setState(s => ({ ...s, skull: { separated: action === 'separate' ? s.selected[0] : undefined },
      isolate: studying ? s.isolate : false, focused: false, explode: 0, rotate: false, restoreCamera: undefined }));
  };
  const skullView = (view: View) => { remember(); setState(s => ({ ...s, view, reset: s.reset + 1, rotate: false, restoreCamera: undefined })); };
  const openPanel = (next: "layers" | "search") => {
    setDetails(false);
    setPanel((p) => (p === next ? null : next));
  };
  const snapshot = (): ExplorerSnapshot => ({ dataset, state, chosen, details, panel, language, camera: camera.current, history: [...history.current] });
  const applySnapshot = (saved: ExplorerSnapshot) => {
    setState({ ...saved.state, rotate: false, restoreCamera: saved.camera ?? undefined });
    setChosen(saved.chosen); setDetails(saved.details); setPanel(saved.panel); setLanguage(saved.language);
    history.current = saved.history; setHistorySize(saved.history.length);
  };
  const startSession = (pack: StudyPack) => {
    const saved = launchSnapshot.current ?? snapshot();
    launchSnapshot.current = null;
    studyReturn.current = () => {
      if (saved.dataset !== pack.datasetId) { setReturnSnapshot(saved); setDataset(saved.dataset); }
      else applySnapshot(saved);
    };
    setActivePack(pack); setLearningOpen(false);
    setLastPack(pack.id);
    try { learningStorage().setItem('atlas.last-study-pack', pack.id); } catch { /* Panel reports durable storage availability. */ }
    setPanel(null); setDetails(false); setStudying(true);
  };
  const requestStudy = (pack: StudyPack) => {
    launchSnapshot.current ??= snapshot();
    if (dataset === pack.datasetId && atlas?.datasetId === pack.datasetId && progress === 100) startSession(pack);
    else { setPendingPack(pack); setDataset(pack.datasetId); }
  };
  const changeReference = (next: DatasetId) => {
    setPendingPack(null); setPendingScene(null); setReturnSnapshot(null);
    launchSnapshot.current = null; setDataset(next);
  };
  useEffect(() => {
    if (!returnSnapshot || atlas?.datasetId !== returnSnapshot.dataset || progress !== 100) return;
    applySnapshot(returnSnapshot); setReturnSnapshot(null);
  }, [returnSnapshot, atlas, progress]);
  const restoreScene = (scene: SavedScene) => {
    if (!atlas || dataset !== scene.dataset || atlas.datasetId !== scene.dataset || progress !== 100) { setPendingScene(scene); setDataset(scene.dataset); return; }
    const invalid = validateScene(scene, atlas, conceptMap);
    if (invalid) { setSceneNotice(invalid); return; }
    remember();
    const restored = scene.chosenId ? conceptMap.get(scene.chosenId) ?? null : null;
    const anchor = atlas.anchors?.find(a => a.conceptId === scene.chosenId);
    setState(s => ({ ...scene.state, rotate: false, reset: s.reset + 1,
      restoreCamera: scene.camera ?? undefined,
      anchor: anchor && restored ? { ...anchor, label: datasetLabel(dataset, restored.id, restored.name, scene.language) } : undefined }));
    setChosen(restored); setDetails(scene.details); setLanguage(scene.language);
    setScenesOpen(false); setLearningOpen(false); setPanel(null); setSceneNotice('Sahne geri yüklendi.');
  };
  useEffect(() => {
    if (!pendingScene || !atlas || atlas.datasetId !== pendingScene.dataset || dataset !== pendingScene.dataset || progress !== 100) return;
    restoreScene(pendingScene); setPendingScene(null);
  }, [pendingScene, atlas, dataset, progress, conceptMap]);
  useEffect(() => {
    if (!pendingPack || dataset !== pendingPack.datasetId || !atlas || atlas.datasetId !== pendingPack.datasetId || progress !== 100) return;
    if (!pendingPack.items.every(it => conceptMap.get(it.conceptId)?.elements.length === 1)) {
      setError('Çalışma kaynağı bu sürümle eşleşmiyor.'); setPendingPack(null); return;
    }
    startSession(pendingPack); setPendingPack(null);
  }, [pendingPack, dataset, atlas, progress, conceptMap]);
  return (
    <main className={`studio ${reference ? "regional-reference" : ""} ${state.skull ? "skull-workspace" : ""}`}>
      {atlas && (
        <AnatomyScene
          key={dataset}
          atlas={atlas}
          state={{
            ...state,
            anchor: state.anchor && chosen ? { ...state.anchor, label: label(chosen) } : undefined,
            inspectorOpen: studying || (details && !!chosen),
            concealLabels: studying,
          }}
          onCameraChange={(pose) => {
            camera.current = pose;
          }}
          onSelect={studying ? () => {} : id => choosePart(id, true)}
          onProgress={(n) => {
            setProgress(n);
            if (n === 100) setError("");
          }}
          onError={(message) => { setError(message); setPendingPack(null); setPendingScene(null); setReturnSnapshot(null); launchSnapshot.current = null; }}
        />
      )}
      <div className="vignette" />
      {error && (
        <div className="loading glass error" role="alert">
          <p>{error}</p>
          <Button variant="ghost" onClick={() => setLoadAttempt(attempt => attempt + 1)}>
            Yeniden dene
          </Button>
        </div>
      )}

      {import.meta.env.DEV && DevQaPanel && <Suspense fallback={null}><DevQaPanel
        read={() => ({ atlas, dataset, state, chosenId: chosen?.id ?? null, language,
          camera: camera.current, progress, error, studying, activePack, historySize, liveStudy: qaStudy.current,
          pending: { pack: pendingPack?.id ?? null, scene: pendingScene?.id ?? null, returning: !!returnSnapshot } })}
        controls={{ explode: value => setState(s => ({ ...s, explode: value, isolate: false, focused: false, restoreCamera: undefined })), study: requestStudy, reference: changeReference, slowLoad: value => { qaSlowLoad.current = value; },
          exit: () => { studyReturn.current?.(); setStudying(false); },
          select: id => { const c = conceptMap.get(id); if (c) choose(c); },
          language: setLanguage, restore: restoreScene,
          isolate: () => setState(s => ({ ...s, isolate: true, focused: true, explode: 0, restoreCamera: undefined })),
        }} /></Suspense>}

      {studying ? <StudyPanel key={activePack.id} pack={activePack} onDiagnostics={import.meta.env.DEV ? value => { qaStudy.current = value; } : undefined} blocked={!!error || progress !== 100} skullControls={activePack.id === 'whole-skull-v1' ? <div className="skull-tools"><label>Bakış <select aria-label="Kafatası bakışı" value={state.view} onChange={e => skullView(e.target.value as View)}>{skullViews.map(v => <option key={v.id} value={v.id}>{v.label}</option>)}</select></label><button onClick={() => skullAction(state.skull?.separated ? 'assemble' : 'separate')}>{state.skull?.separated ? 'Kemiği yerine döndür' : 'Seçili kemiği ayır'}</button><p>Sağ/sol bireye aittir. Ayırma eğitim düzenidir; doğal hareket değildir.</p></div> : undefined} language={language} concepts={conceptMap} reveal={(id, isolated) => {
        const c = conceptMap.get(id);
        if (!c) return;
        choose(c);
        setDetails(false);
        setState(s => ({ ...s, ghost: true, isolate: isolated, anchor: undefined, visible: ["skeletal"], hidden: [], skull: activePack.id === 'whole-skull-v1' ? (s.skull ?? {}) : undefined, focused: activePack.id !== 'whole-skull-v1', restoreCamera: undefined }));
      }} exit={() => { studyReturn.current?.(); setStudying(false); }} /> : <>
      <div className="study-entry">{dataset === 'male-body' && <button disabled={!atlas || progress !== 100} onClick={() => { const c = conceptMap.get(SKULL_GROUP); if (c) choose(c); }}>Kafatası · 22 kemik</button>}<button onClick={() => { if (learningOpen) setPendingPack(null); launchSnapshot.current = learningOpen ? null : snapshot(); setLearningOpen(v => !v); setScenesOpen(false); setDetails(false); setPanel(null); }}>Çalışma ve tekrar</button><button disabled={!atlas || progress !== 100} onClick={() => { setScenesOpen(v => !v); setLearningOpen(false); setSceneNotice(''); }}>Kayıtlı sahneler</button></div>
      {sceneNotice && createPortal(<div className="scene-notice" role="status">{sceneNotice}<button aria-label="Bildirimi kapat" onClick={() => setSceneNotice('')}>×</button></div>, document.body)}
      {scenesOpen && atlas && progress === 100 && <SavedScenesPanel atlas={atlas} dataset={dataset} state={state} camera={() => camera.current} chosenId={chosen?.id ?? null} details={details} language={language} onRestore={restoreScene} onClose={() => setScenesOpen(false)} />}
      {learningOpen && <section className="detail-sheet study-panel" aria-label="Çalışma modülleri">
        <button onClick={() => { setLearningOpen(false); setPendingPack(null); launchSnapshot.current = null; }}>Kapat</button>
        <h2>Kaynak modelle çalış</h2>
        <p>İncele, hatırla, düzelt ve zamanı gelen soruları tekrar et. İlerleme bu tarayıcıda saklanır.</p>
        {studyPacks.map(pack => <div key={pack.id}>
          <h3>{pack.title}</h3><p>{pack.scope}</p>
          <button disabled={!!pendingPack} onClick={() => requestStudy(pack)}>{lastPack === pack.id ? 'Devam et' : 'Çalışmaya başla'} · {pack.items.length} yapı</button>
        </div>)}
        {pendingPack && <p role="status">Referans yükleniyor…</p>}
      </section>}
      <header className="identity">
        <div className="eyebrow">
          <span className="status-dot" /> INTERACTIVE ANATOMY
        </div>
        <h1>
          {reference?.heading ?? "Human Atlas"}
          <Badge variant="outline" className="edition">
            3D
          </Badge>
        </h1>
        <div className="identity-meta">
          {atlas ? atlas.parts.length.toLocaleString() : "—"} modeled pieces <span>·</span>{" "}
          {reference?.identity ?? "Erkek · BodyParts3D + Z-Anatomy"}
        </div>
        <select
          className="dataset-select"
          aria-label="Anatomi referansı"
          value={dataset}
          onChange={(e) => {
            setAtlas(null);
            changeReference(e.target.value as DatasetId);
          }}
        >
          <option value="male-body">Erkek vücut</option>
          {Object.entries(REFERENCE_DATASETS).map(([id, config]) => (
            <option key={id} value={id}>
              {config.title}
            </option>
          ))}
        </select>
      </header>
      <nav className="top-actions" aria-label="Explorer panels">
        <select
          className="language-select"
          aria-label="Anatomik ad dili"
          value={language}
          onChange={(e) => setLanguage(e.target.value as "tr" | "en" | "la")}
        >
          <option value="tr">TR</option>
          <option value="en">EN</option>
          <option value="la">LA</option>
        </select>
        <Button
          variant="ghost"
          aria-label="Önceki görünüme dön"
          disabled={!historySize}
          onClick={goBack}
        >
          ← Geri
        </Button>
        <Button
          variant="ghost"
          className={panel === "search" ? "active" : ""}
          onClick={() => openPanel("search")}
          aria-label="Anatomi ara"
        >
          <Search size={18} />
          <span>Yapı bul</span>
          <kbd>/</kbd>
        </Button>
        <Button
          variant="ghost"
          className="guide-trigger"
          aria-label="Başlangıç rehberi ve kaynaklar"
          onClick={() => {
            setDetails(false);
            setPanel(null);
            guideSearchHandoff.current = false;
            setAbout(true);
          }}
        >
          <Info size={18} />
          <span>Rehber</span>
        </Button>
      </nav>
      <section
        className={`layers-panel glass ${panel === "layers" ? "mobile-open" : ""}`}
        aria-label="Anatomical layers"
      >
        <div className="panel-heading">
          <span>Systems</span>
          <Button
            variant="ghost"
            className="mobile-only icon-button"
            onClick={() => setPanel(null)}
            aria-label="Close systems"
          >
            <X size={18} />
          </Button>
          <Badge variant="secondary" className="desktop-only small-number">
            {activeSystems.length}
          </Badge>
        </div>
        <div className="layer-presets">
          <Button
            variant="ghost"
            aria-pressed={activeSystems.every((x) => state.visible.includes(x.id))}
            onClick={() => setLayers(activeSystems.map((x) => x.id))}
          >
            All
          </Button>
          <Button
            variant="ghost"
            aria-pressed={state.visible.length === 1 && state.visible[0] === "skeletal"}
            onClick={() => setLayers(["skeletal"])}
          >
            Skeleton
          </Button>
          <Button
            variant="ghost"
            aria-pressed={
              state.visible.length === 6 &&
              ["cardiac", "respiratory", "digestive", "urinary", "endocrine", "reproductive"].every(
                (id) => state.visible.includes(id as SystemId),
              )
            }
            onClick={() =>
              setLayers([
                "cardiac",
                "respiratory",
                "digestive",
                "urinary",
                "endocrine",
                "reproductive",
              ])
            }
          >
            Organs
          </Button>
        </div>
        {!reference && (
          <>
            <div className="region-shortcuts">
              <span>Bölgeye git</span>
              <select
                aria-label="Anatomik bölge"
                value=""
                onChange={(e) => {
                  const c = conceptMap.get(e.target.value);
                  if (c) choose(c);
                }}
              >
                <option value="">Bir bölge seç…</option>
                {[
                  ["FMA7154", "Baş"],
                  ["FMA7155", "Boyun"],
                  ["FMA9576", "Toraks"],
                  ["FMA9577", "Abdomen"],
                  ["FMA9578", "Pelvis"],
                  ["FMA7186", "Sol üst ekstremite"],
                  ["FMA7185", "Sağ üst ekstremite"],
                  ["FMA7188", "Sol alt ekstremite"],
                  ["FMA7187", "Sağ alt ekstremite"],
                ].map(([id, name]) => (
                  <option key={id} value={id}>
                    {name}
                  </option>
                ))}
              </select>
            </div>
            <Button
              className="coverage-open"
              variant="ghost"
              onClick={() => {
                setCoverageOpen(true);
                setPanel(null);
              }}
            >
              Bölgesel yapı listesi ve kapsam
            </Button>
          </>
        )}
        {reference && <p className="reference-scope">{reference.scope}</p>}
        <div className="system-list">
          {activeSystems.map((s) => (
            <div
              className={`system-row ${state.visible.includes(s.id) ? "enabled" : ""}`}
              key={s.id}
            >
              <Button
                variant="ghost"
                className="system-name"
                title={`Show only ${s.name.toLowerCase()}`}
                onClick={() => setLayers([s.id])}
              >
                <span className="system-dot" style={{ background: s.color }} />
                {s.name}
                <span className="system-count">{counts[s.id]}</span>
              </Button>
              <Switch
                checked={state.visible.includes(s.id)}
                onCheckedChange={() => toggle(s.id)}
                aria-label={`Show ${s.name.toLowerCase()}`}
              />
            </div>
          ))}
        </div>
        <div className="panel-foot">
          <span>{visibleCount.toLocaleString()} pieces visible</span>
          <Button variant="ghost" onClick={() => setLayers([])}>
            Hide all
          </Button>
        </div>
      </section>
      {panel === "search" && (
        <section className="search-panel glass" aria-label="Anatomi ara">
          <div className="panel-heading">
            <span>Yapı bul</span>
            <Button
              variant="ghost"
              className="icon-button"
              onClick={() => setPanel(null)}
              aria-label="Aramayı kapat"
            >
              <X size={18} />
            </Button>
          </div>
          <Combobox<Concept>
            items={results}
            value={null}
            onValueChange={(value) => {
              if (value) choose(value);
            }}
            inputValue={query}
            onInputValueChange={setQuery}
            itemToStringLabel={label}
            filter={null}
            open
            onOpenChange={(open) => {
              if (!open) setPanel(null);
            }}
          >
            <ComboboxInput
              autoFocus
              placeholder={reference?.placeholder ?? "Biceps, skapula, musculocutaneous…"}
              aria-label="Anatomik yapı ara"
              showTrigger={false}
            />
            <ComboboxContent className="anatomy-search-results">
              <ComboboxEmpty>Eşleşen yapı yok.</ComboboxEmpty>
              <ComboboxList>
                {(c: Concept) => (
                  <ComboboxItem key={c.id} value={c}>
                    <span className="search-result-name">{label(c)}</span>
                    <span className="small-number">
                      {anchorMap.has(c.id) ? "Yüzey işareti" : `${c.elements.length} parça`}
                    </span>
                  </ComboboxItem>
                )}
              </ComboboxList>
            </ComboboxContent>
          </Combobox>
          <p className="search-note">
            {query
              ? "En çok 80 sonuç. Türkçe, Latince veya İngilizce adla arayabilirsiniz."
              : reference
                ? "Bu referanstaki yapıları Türkçe, İngilizce, Latince veya kaynak adıyla arayın."
                : "Bir yapı seçin. Çok dilli adlandırma seçilmiş bölgelerde mevcuttur."}
          </p>
        </section>
      )}
      <nav className="view-controls glass" aria-label="Camera controls">
        {(["three-quarter", "front", "side", "back"] as View[]).map((v, i) => (
          <Button
            variant="ghost"
            key={v}
            className={state.view === v ? "active" : ""}
            aria-pressed={state.view === v}
            disabled={state.explode > 0.8 && v !== "front"}
            onClick={() =>
              setState((s) => ({
                ...s,
                view: v,
                reset: s.reset + 1,
                rotate: false,
                restoreCamera: undefined,
              }))
            }
            title={`${v} view`}
            aria-label={`${v} view`}
          >
            <span>{["¾", "F", "S", "B"][i]}</span>
          </Button>
        ))}
        <i />
        <Button
          variant="ghost"
          disabled={state.explode >= 0.4}
          aria-label={state.rotate ? "Pause rotation" : "Rotate body"}
          title="Auto rotate"
          className={state.rotate ? "active" : ""}
          onClick={() => setState((s) => ({ ...s, rotate: !s.rotate }))}
        >
          {state.rotate ? <Pause size={17} /> : <RotateCw size={18} />}
        </Button>
        <Button variant="ghost" aria-label="Görünümü ve katmanları sıfırla" title="Reset" onClick={reset}>
          <RotateCcw size={17} />
        </Button>
      </nav>
      <div className="scene-caption">
        <span className="caption-line" />
        <span>
          {state.isolate
            ? chosen
              ? label(chosen)
              : "SELECTED STRUCTURE"
            : state.explode > 0.95
              ? "ANATOMICAL INVENTORY"
              : state.explode > 0.05
                ? "SEPARATED STRUCTURES"
                : (state.skull ? "KAFATASI · 22 KEMİK" : reference?.title ?? "ADULT HUMAN · MALE")}
        </span>
        <span className="caption-line" />
      </div>
      <div className="bottom-dock glass">
        <Button
          variant="ghost"
          className="mobile-only dock-layers"
          onClick={() => openPanel("layers")}
          aria-label="Open system layers"
        >
          <Layers3 size={20} />
          <span>Systems</span>
        </Button>
        {state.skull ? <div className="skull-dock"><button onClick={() => { setDetails(true); setPanel(null); if (!chosen) setChosen(conceptMap.get(SKULL_GROUP) ?? null); }}>22 kemik · çalışma düzeni</button><button onClick={() => skullAction('start')}>Başlangıç düzeni</button></div> : <div className="explode-control">
          <div className="explode-label">
            <label id="explode-label">Explode anatomy</label>
            <output>
              {Math.round(state.explode * 100)}
              <span>%</span>
            </output>
          </div>
          <Slider
            aria-labelledby="explode-label"
            min={0}
            max={100}
            step={1}
            value={[state.explode * 100]}
            onValueChange={(v) =>
              setState((s) => ({
                ...s,
                explode: (Array.isArray(v) ? v[0] : v) / 100,
                view: (Array.isArray(v) ? v[0] : v) > 80 ? "front" : s.view,
                rotate: false,
              }))
            }
          />
          <div className="slider-endpoints">
            <span>Assembled</span>
            <span>Every piece</span>
          </div>
        </div>
        }<Button
          variant="ghost"
          className="dock-reset"
          onClick={reset}
          aria-label="Birleştir ve sıfırla"
        >
          <RotateCcw size={18} />
          <span>Reset</span>
        </Button>
      </div>
      {(state.hidden?.length ?? 0) > 0 && (
        <Button
          className="restore-hidden glass"
          variant="ghost"
          onClick={() => {
            remember();
            setState((s) => ({ ...s, hidden: [] }));
          }}
        >
          {state.hidden?.length} gizli parçayı göster
        </Button>
      )}
      <footer className="studio-footer">
        <span>
          {state.skull ? "Sürükle: döndür · Kaydır: yakınlaştır · Dokun: seç" : <>{state.explode > 0.8 ? "Drag to pan" : "Drag to orbit"} <b>·</b> Pinch to zoom <b>·</b> Tap to inspect</>}
        </span>
        <Button
          variant="ghost"
          onClick={() => {
            setDetails(false);
            setPanel(null);
            guideSearchHandoff.current = false;
            setAbout(true);
          }}
        >
          Rehber ve kaynaklar <ArrowUpRight size={12} />
        </Button>
      </footer>
      {progress < 100 && !error && (
        <div className="loading glass" role="status">
          <Activity size={18} />
          <div>
            <strong>Preparing the anatomy</strong>
            <span>
              {progress}% · Loading {atlas?.parts.length.toLocaleString() ?? "—"} pieces
            </span>
            <div className="loading-track">
              <i style={{ width: `${progress}%` }} />
            </div>
          </div>
        </div>
      )}
      <Sheet
        open={details && !!chosen}
        modal={false}
        disablePointerDismissal
        onOpenChange={setDetails}
      >
        <SheetContent
          initialFocus={detailTitle}
          className={`detail-sheet glass ${state.isolate ? "is-isolated" : ""} ${state.skull ? "skull-detail" : ""}`}
          showCloseButton={true}
        >
          <div className="detail-header">
            <div className="detail-learning-actions">
              <button onClick={() => { setScenesOpen(true); setLearningOpen(false); setSceneNotice(''); }}>Sahneyi kaydet</button>
              <button onClick={() => { if (state.skull) requestStudy(studyPacks.find(p => p.id === 'whole-skull-v1')!); else { launchSnapshot.current = snapshot(); setLearningOpen(true); setDetails(false); } }}>Çalışma</button>
            </div>
            <div className="detail-accent" style={{ background: system?.color }} />
            <div className="eyebrow">
              {new Set(selectedParts.map((p) => p.system)).size > 1
                ? "Bileşik yapı"
                : (state.skull ? "KAFATASI" : system?.name ?? "ANATOMİ")}
            </div>
            <SheetTitle ref={detailTitle} tabIndex={-1} className="structure-title">
              {chosen ? label(chosen) : null}
            </SheetTitle>
          </div>
          <div className="detail-scroll" key={`${chosen?.id}-${state.isolate}`}>
            {state.skull && <section className="skull-tools" aria-label="Kafatası çalışma düzeni">
              <label>Kemik seç · 22 <select aria-label="Kafatası kemiği" value={skullItem(chosen?.id) ? chosen!.id : ''} onChange={e => { const c = conceptMap.get(e.target.value || SKULL_GROUP); if (c) choose(c); }}>
                <option value="">Bütün kafatası</option>{skullItems.map(it => <option key={it.id} value={it.conceptId}>{label(conceptMap.get(it.conceptId) ?? { id: it.conceptId, name: it.sourceObject })}</option>)}
              </select></label>
              <label>Bakış <select aria-label="Kafatası bakışı" value={state.view} onChange={e => skullView(e.target.value as View)}>{skullViews.map(v => <option key={v.id} value={v.id}>{v.label}</option>)}</select></label>
              <div><button disabled={state.selected.length !== 1} onClick={() => skullAction('separate')}>Seçili kemiği ayır</button><button disabled={!state.skull.separated} onClick={() => skullAction('assemble')}>Kemiği yerine döndür</button></div>
              <button onClick={() => { remember(); setState(s => ({ ...s, isolate: false, focused: false, ghost: false, refit: (s.refit ?? 0) + 1, restoreCamera: undefined })); }}>Bütün kafatasını göster</button>
              <button onClick={() => skullAction('start')}>Kafatası başlangıç düzeni</button>
              <p>Sağ/sol bireye aittir. Ayırma eğitim düzenidir; doğal hareket değildir. Küçük kemikler için listeden seçip yalnız gösterin.</p>
              <details><summary>Kaynak ve kapsam</summary><p>BodyParts3D 4.0 · mevcut 22 kemik. İnce ayrıntı ve uzman onayı yoktur.</p><a href="https://anatomy.ttuhscep.edu/anatomytables/bones_head_neck.html" target="_blank" rel="noreferrer">Kemik konumları: TTUHSC</a></details>
            </section>}
            {chosenAnchor && (
              <p className="anchor-note">
                Tutunma yüzeyinden alınmış referans noktasıdır; yapının sınırlarını göstermez.
              </p>
            )}
            {chosen && !reference && representationFor(chosen.id)?.representationLimits && (
              <details className="context-note">
                <summary>Referans noktasının kaynak sınırları</summary>
                {representationFor(chosen.id)?.representationLimits?.map((note: string) => <p key={note}>{note}</p>)}
                <p>Kaynak yüzeyinden alınan tek noktadır; tam yüzey veya uzman kabulü değildir.</p>
              </details>
            )}
            {variantConcept && variant && (
              <Button variant="outline" onClick={() => choose(variantConcept, true)}>
                {variant.source ? "Ham kaynak seçimini göster" : "İncelenmiş seçime dön"}
              </Button>
            )}
            <SheetDescription className="structure-description">
              {state.skull ? skullDescription(chosen?.id) : reference
                ? referenceDescription(dataset, chosen?.id)
                : chosen && getRepresentationNote(chosen.id)
                  ? getRepresentationNote(chosen.id)
                  : chosenAnchor
                    ? "Kemik üzerindeki kaynaklı yüzey işareti."
                    : !selected
                      ? "Bu yapının bağımsız geometrisi veya etiket konumu henüz eklenmedi. Kaynaklı bağlantılarını aşağıdan inceleyebilirsiniz."
                      : new Set(selectedParts.map((p) => p.system)).size > 1
                        ? "Bu bileşik yapı, modelde birden fazla sisteme ait parçaları bir araya getirir. Alt parçaları ve kaynaklı bağlantıları inceleyebilirsiniz."
                        : chosen
                          ? explanation(chosen.name, selected.system)
                          : ""}
            </SheetDescription>
            {!reference && !state.skull &&
              chosen &&
              selected &&
              !getRepresentationNote(chosen.id) &&
              !EXPLANATIONS[chosen.name.toLowerCase()] && (
                <span className="context-note">
                  Genel sistem bilgisi · yapıya özel açıklama değildir
                </span>
              )}
            {chosen && (!reference || dataset === "lower-limb-nerve-reference" || dataset === "upper-limb-nerve-reference") && (
              <section className="relationship-list" aria-label="Anatomik bağlantılar">
                <h3>
                  Anatomik bağlantılar <span>{relations.length}</span>
                </h3>
                {relations.length === 0 ? (
                  <p>Bu yapı için kaynaklı bağlantı henüz eklenmedi.</p>
                ) : (
                  relations.map((relation) => {
                    const target = conceptMap.get(relation.otherId);
                    return (
                      <div className="relationship-row" key={relation.id}>
                        <Button
                          variant="ghost"
                          disabled={!target}
                          onClick={() => {
                            if (target) choose(target);
                          }}
                        >
                          <span>
                            <small>{relation.label}</small>
                            <strong>{target ? label(target) : relation.name}</strong>
                            {relation.divisionLabel && <em>{relation.divisionLabel}</em>}
                            {relation.attachmentNoteTr && <em>{relation.attachmentNoteTr}</em>}
                            {target && !target.elements.length && (
                              <em>
                                {anchorMap.has(target.id)
                                  ? "Yüzey işareti"
                                  : "Geometri / konum bekleniyor"}
                              </em>
                            )}
                          </span>
                          <ChevronRight size={15} />
                        </Button>
                        <details>
                          <summary>Kaynak</summary>
                          {relation.evidence.map((e, i) => {
                            const source = knowledgeSource(e.sourceId, dataset);
                            return source ? (
                              <a key={i} href={source.url} target="_blank" rel="noreferrer">
                                {source.title}
                              </a>
                            ) : null;
                          })}
                          {relationshipScopeNotes(relation.qualifiers).map(note => <p key={note}>{note}</p>)}
                          <p>Kaynakla destekleniyor; uzman incelemesi bekliyor.</p>
                        </details>
                      </div>
                    );
                  })
                )}
              </section>
            )}
            <div className="structure-meta">
              <span>
                Yapı kimliği<strong>{chosen?.id}</strong>
              </span>
              <span>
                Seçili parça<strong>{state.selected.length.toLocaleString()}</strong>
              </span>
            </div>
            {selectedParts.length > 1 && (
              <div className="member-list">
                <h3>İçerdiği yapılar</h3>
                {selectedParts.slice(0, 50).map((p) => (
                  <Button variant="ghost" key={p.id} onClick={() => choosePart(p.id)}>
                    <span>{label({ id: p.conceptId, name: p.name })}</span>
                    <ChevronRight size={14} />
                  </Button>
                ))}
                {selectedParts.length > 50 && (
                  <p>And {selectedParts.length - 50} more modeled pieces.</p>
                )}
              </div>
            )}
            {(selectedParts.length > 0 || chosenAnchor) && (
              <a
                className="source-link"
                href={
                  chosenAnchor
                    ? "https://github.com/Z-Anatomy/Models-of-human-anatomy"
                    : (selectedParts.find((p) => p.sourceUrl)?.sourceUrl ??
                      (typeof atlas?.source === "object" ? atlas.source.url : undefined) ??
                      "https://lifesciencedb.jp/bp3d/")
                }
                target="_blank"
                rel="noreferrer"
              >
                Model kaynağı <ArrowUpRight size={14} />
              </a>
            )}
          </div>
          <div className="detail-actions">
            <div className="inspection-tools">
              <Button
                variant="ghost"
                disabled={!selected && !chosenAnchor}
                onClick={() => {
                  remember();
                  setState((s) => ({
                    ...s,
                    focused: true,
                    explode: 0,
                    refit: (s.refit ?? 0) + 1,
                    rotate: false,
                    restoreCamera: undefined,
                  }));
                }}
              >
                Odaklan
              </Button>
              <Button
                variant="ghost"
                disabled={!selected && !chosenAnchor}
                aria-pressed={!!state.ghost}
                onClick={() => {
                  remember();
                  setState((s) => ({ ...s, ghost: !s.ghost, isolate: false }));
                }}
              >
                Çevreyi {state.ghost ? "göster" : "saydamlaştır"}
              </Button>
              <Button
                variant="ghost"
                disabled={!selected}
                onClick={() => {
                  remember();
                  setState((s) => ({
                    ...s,
                    hidden: [...new Set([...(s.hidden ?? []), ...s.selected])],
                    selected: [],
                    anchor: undefined,
                    focused: false,
                    isolate: false,
                    ghost: false,
                  }));
                  setDetails(false);
                }}
              >
                Parçayı gizle
              </Button>
            </div>
            <Button
              disabled={!selected}
              className={`primary-action ${state.isolate ? "active" : ""}`}
              onClick={() => {
                remember();
                setState((s) => ({
                  ...s,
                  isolate: !s.isolate,
                  focused: true,
                  explode: 0,
                  restoreCamera: undefined,
                }));
              }}
            >
              <Focus size={18} />
              {state.isolate ? "Çevreyi göster" : "Yapıyı yalnız göster"}
              <ChevronRight size={16} />
            </Button>
            <Button
              variant="ghost"
              className="secondary-action"
              onClick={() => {
                setState((s) => ({
                  ...s,
                  selected: [],
                  anchor: undefined,
                  isolate: false,
                  focused: false,
                  ghost: false,
                }));
                setDetails(false);
              }}
            >
              Seçimi temizle
            </Button>
          </div>
        </SheetContent>
      </Sheet>
      {!reference && (
        <CoveragePanel
          open={coverageOpen}
          onOpenChange={setCoverageOpen}
          onOpenReference={(next: DatasetId) => {
            setCoverageOpen(false);
            setAtlas(null);
            changeReference(next);
          }}
          concepts={conceptMap}
          onChoose={(c) => {
            setCoverageOpen(false);
            choose(c);
          }}
        />
      )}
      <Sheet open={about} onOpenChange={setAbout} onOpenChangeComplete={(open) => {
        if (!open && guideAction.current) {
          const action = guideAction.current;
          guideAction.current = null;
          action();
        }
      }}>
        <SheetContent className="about-sheet glass" initialFocus={guideTitle} finalFocus={() => !guideSearchHandoff.current}>
          <div className="eyebrow">HUMAN ATLAS · BAŞLANGIÇ REHBERİ</div>
          <SheetTitle ref={guideTitle} tabIndex={-1} className="structure-title">Anatomiyi keşfederek öğren.</SheetTitle>
          <SheetDescription>
            Kaynak modelleri incele, yapıların bağlamını gör ve kısa çalışma modüllerini dene.
          </SheetDescription>
          <ol className="visitor-steps">
            <li><span className="visitor-step-number" aria-hidden="true">01</span><div>
              <h3>Bir yapı bul</h3>
              <p><strong>Yapı bul</strong> ile {reference ? 'bu referanstaki bir yapıyı' : '“kalp” veya “skapula” gibi bir adı'} ara. Sonucu seç; odak ve izolasyon kontrolleriyle incele. <strong>Geri</strong> önceki görünümü getirir.</p>
            </div></li>
            <li><span className="visitor-step-number" aria-hidden="true">02</span><div>
              <h3>Bütün ile parçayı karşılaştır</h3>
              <p><strong>Erkek vücut</strong> referansında <strong>Kafatası · 22 kemik</strong> seçeneğini aç. Bir kemik seçip ayır; farklı bakışlardan incele ve yerine döndür.</p>
            </div></li>
            <li><span className="visitor-step-number" aria-hidden="true">03</span><div>
              <h3>Kendini dene</h3>
              <p><strong>Çalışma ve tekrar</strong> içinden bir modül seç. İncele, hatırla ve geri bildirimle tekrar et. İlerleme yalnız bu tarayıcıda saklanır.</p>
            </div></li>
          </ol>
          <Button className="visitor-start" disabled={!atlas || progress !== 100 || !!error} onClick={() => {
            // The close-complete callback precedes focus-manager cleanup. Keep return focus
            // suppressed through that cleanup so it cannot blur and dismiss the new search.
            guideSearchHandoff.current = true;
            guideAction.current = () => { setLearningOpen(false); setScenesOpen(false); setDetails(false); setQuery(''); setPanel('search'); };
            setAbout(false);
          }}>Yapı bul ile başla <ArrowUpRight size={16} /></Button>
          <p className="visitor-controls">Sürükle: döndür · Kaydır veya iki parmak: yakınlaştır · Tıkla/dokun: seç. TR / EN / LA, anatomik adların dilini değiştirir; bazı adlar henüz çevrilmemiştir.</p>
          <section className="visitor-scope" aria-label="Proje ve kapsam">
            <h3>Gelişen bir eğitim prototipi</h3>
            <p>Bu sürüm kaynaklı 3B keşif ve sınırlı yapı tanıma alıştırmaları sunar. Tam bir anatomi müfredatı değildir; anatomik uzman incelemesi bekler. Ayrı bölgesel referanslar aynı bedenin parçaları olarak birleştirilmez.</p>
            <p>Özgün Human Atlas uygulaması üzerine geliştirilen bu çalışma; Türkçe bölgesel adlar, kaynaklı ilişkiler, ayrı referanslar ve çalışma akışları ekler.</p>
            <div className="visitor-project-links">
              <a href="https://github.com/ismailatilan-44/human-atlas" target="_blank" rel="noreferrer">Proje ve geliştirme kayıtları <ArrowUpRight size={14} /></a>
              <a href="https://github.com/ashemag/human-atlas" target="_blank" rel="noreferrer">Özgün uygulama · ashemag · MIT <ArrowUpRight size={14} /></a>
            </div>
          </section>
          <details className="visitor-sources">
            <summary>Model kaynakları, lisanslar ve kapsam</summary>
            <p className="visitor-current-reference">Açık referans: {reference?.title ?? 'Erkek vücut'}</p>
          <div className="about-copy">
            {reference ? (
              <>
                <p>
                  <strong>{reference.sourceName}</strong>
                  <br />
                  {atlas?.parts.length ?? "—"} kaynak parçası · {reference.title}
                </p>
                <p>{atlas?.scope}</p>
                <p>
                  Bu bağımsız sahnenin model konumları kaynak referansa aittir. Ana erkek vücut
                  modeliyle birleştirilmez. Görünmeyen yapılara ilişkin tamlık iddiası taşımaz.
                </p>
                {typeof atlas?.source === "object" && (
                  <>
                    <a href={atlas.source.url} target="_blank" rel="noreferrer">
                      Model kaynağı <ArrowUpRight size={14} />
                    </a>
                    {atlas.source.attribution && (
                      <a href={assetUrl(atlas.source.attribution)} target="_blank" rel="noreferrer">
                        Kaynaklar, lisans ve atıflar <ArrowUpRight size={14} />
                      </a>
                    )}
                    {atlas.source.license && <p>{atlas.source.license}</p>}
                  </>
                )}
              </>
            ) : (
              <>
                <p>
                  <strong>Erkek vücut · BodyParts3D + Z-Anatomy</strong>
                  <br />
                  {atlas?.parts.length.toLocaleString() ?? '—'} paketli model parçası. Temel BodyParts3D referansı ve ek kaynak paketleri kendi kimliklerini ve lisanslarını korur.
                </p>
                <p>
                  Bu referans her insan yapısını veya varyasyonunu içermez. Bir adlandırılmış
                  seçim birden çok model parçası içerebilir; parça sayısı anatomik tamlık ölçüsü değildir.
                </p>
                <p>
                  Renkler ve sistem grupları keşfi kolaylaştırır. Geometri ve kısa açıklamalar
                  eğitim amaçlıdır; tanı veya cerrahi planlama için kullanılmaz. Kafatası ayırma
                  görünümü bir eğitim düzenidir, doğal hareketi göstermez.
                </p>
                <h3>Ek modeller ve yüzey işaretleri</h3>
                <p>
                  {atlas?.parts.filter((p) => p.sourceUrl).length ?? 0} ek parça ve{" "}
                  {atlas?.anchors?.length ?? 0} yüzey işareti Z-Anatomy ve BodyParts3D 4.3 kaynak
                  geometrilerinden aktarılmıştır. Anatomik ilişkiler ve geometri uyumu uzman
                  incelemesi bekler.
                </p>
                <a
                  href={assetUrl("/models/extensions/ATTRIBUTION.md")}
                  target="_blank"
                  rel="noreferrer"
                >
                  Z-Anatomy kaynak ve atıfları
                </a>
                <a
                  href={assetUrl("/models/extensions/KNEE-ATTRIBUTION.md")}
                  target="_blank"
                  rel="noreferrer"
                >
                  Diz modelleri: kaynak ve atıflar
                </a>
                <a
                  href={assetUrl("/models/extensions/SCIATIC-ATTRIBUTION.md")}
                  target="_blank"
                  rel="noreferrer"
                >
                  Siyatik sinirler: kaynak ve atıflar
                </a>
                <a
                  href={assetUrl("/models/extensions/BRACHIAL-PLEXUS-ATTRIBUTION.md")}
                  target="_blank"
                  rel="noreferrer"
                >
                  Brakiyal pleksus: kaynak, atıflar ve kapsam
                </a>
                <a
                  href={assetUrl("/models/extensions/THYROID-BP3D43-ATTRIBUTION.md")}
                  target="_blank"
                  rel="noreferrer"
                >
                  Tiroid lobları: BodyParts3D 4.3 kaynak ve atıfları
                </a>
                <a
                  href={assetUrl("/models/extensions/SPINAL-CORD-BP3D43-ATTRIBUTION.md")}
                  target="_blank"
                  rel="noreferrer"
                >
                  Omurilik dokusu: BodyParts3D 4.3 kaynak ve atıfları
                </a>
                <a href={assetUrl("/models/extensions/LEFT-CORDS-BP3D43-ATTRIBUTION.md")} target="_blank" rel="noreferrer">
                  İki sol pleksus kordu: kaynak, lisans ve kapsam
                </a>
                <a href={assetUrl("/models/extensions/LUNG-BP3D43-ATTRIBUTION.md")} target="_blank" rel="noreferrer">
                  Akciğer doku yüzeyleri: kaynak, lisans ve kapsam
                </a>
                <h3>Temel BodyParts3D kaynağı</h3>
                <p>
                  BodyParts3D, © The Database Center for Life Science licensed under CC Attribution
                  4.0 International.
                </p>
                <a
                  href="https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html"
                  target="_blank"
                  rel="noreferrer"
                >
                  Dataset license <ArrowUpRight size={14} />
                </a>
                <a
                  href="https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html"
                  target="_blank"
                  rel="noreferrer"
                >
                  Original geometry & metadata <ArrowUpRight size={14} />
                </a>
                <a
                  href="https://academic.oup.com/nar/article/37/suppl_1/D782/1000752"
                  target="_blank"
                  rel="noreferrer"
                >
                  Read the source publication <ArrowUpRight size={14} />
                </a>
              </>
            )}
          </div>
          </details>
        </SheetContent>
      </Sheet>
      </>}
    </main>
  );
}
