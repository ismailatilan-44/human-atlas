import CoveragePanel from "./coverage-panel";
import { loadAtlas } from "./load-atlas";
import { flushSync } from "react-dom";
import { registerAtlasTools } from "./agent-tools";
import { getRepresentationNote, anatomyLabel, anatomySearchTerms } from "./atlas-metadata";
import { explorerConcepts, relationshipsFor, knowledgeSources } from "./knowledge";
import { useEffect, useMemo, useRef, useState } from "react";
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
  type Concept,
  type SceneState,
  type SystemId,
  type View,
  type CameraPose,
} from "./anatomy";
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
export default function Home() {
  const detailTitle = useRef<HTMLHeadingElement>(null);
  const camera = useRef<CameraPose | null>(null);
  const history = useRef<
    { state: SceneState; chosen: Concept | null; details: boolean; camera: CameraPose | null }[]
  >([]);
  const [historySize, setHistorySize] = useState(0),
    [language, setLanguage] = useState<"tr" | "en" | "la">("tr");
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
    setState({ ...initial, visible: DEFAULT_VISIBLE });
    loadAtlas(abort.signal)
      .then(setAtlas)
      .catch((e) => {
        if (e.name !== "AbortError") setError(e.message);
      });
    return () => abort.abort();
  }, []);
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if (
        e.key === "/" &&
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
  }, []);
  const parts = useMemo(() => new Map(atlas?.parts.map((p) => [p.id, p])), [atlas]);
  const concepts = useMemo(() => (atlas ? explorerConcepts(atlas) : []), [atlas]);
  const conceptMap = useMemo(() => new Map(concepts.map((c) => [c.id, c])), [concepts]);
  const relations = useMemo(() => (chosen ? relationshipsFor(chosen.id) : []), [chosen]);
  const anchorMap = useMemo(() => new Map(atlas?.anchors?.map((a) => [a.conceptId, a])), [atlas]);
  const chosenAnchor = chosen ? anchorMap.get(chosen.id) : undefined;
  const label = (c: { id: string; name: string }) => anatomyLabel(c.id, c.name, language);
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
        !state.hidden?.includes(p.id) &&
        (state.isolate
          ? state.selected.includes(p.id)
          : state.visible.includes(p.system) || state.selected.includes(p.id)),
    ).length ?? 0;
  const results = useMemo(() => {
    if (!atlas) return [];
    const term = query.toLowerCase().trim();
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
      .filter(
        (c) =>
          anatomySearchTerms(c.id, c.name).some(
            (name) =>
              name.toLocaleLowerCase("tr").includes(term.toLocaleLowerCase("tr")) ||
              name.toLowerCase().includes(term),
          ) || c.id.toLowerCase().includes(term),
      )
      .sort((a, b) => a.name.length - b.name.length)
      .slice(0, 80);
  }, [atlas, concepts, query]);
  const choose = (c: Concept) => {
    const anchor = anchorMap.get(c.id);
    remember();
    setChosen(c);
    setState((s) => ({
      ...s,
      selected: c.elements,
      anchor: anchor ? { ...anchor, label: label(c) } : undefined,
      ghost: anchor ? true : s.ghost,
      isolate: false,
      focused: c.elements.length > 0 || !!anchor,
      explode: 0,
      rotate: false,
      hidden: s.hidden?.filter((id) => !c.elements.includes(id)),
      restoreCamera: undefined,
    }));
    setDetails(true);
    setPanel(null);
  };
  const chooseLatest = useRef(choose);
  chooseLatest.current = choose;
  useEffect(() => {
    if (!atlas) return;
    return registerAtlasTools(atlas, (c) => flushSync(() => chooseLatest.current(c)));
  }, [atlas]);
  const choosePart = (id: string) => {
    const p = parts.get(id);
    if (!p) return;
    choose({ id: p.conceptId, name: p.name, elements: [id] });
  };
  const toggle = (id: SystemId) => {
    setDetails(false);
    setState((s) => ({
      ...s,
      selected: [],
      anchor: undefined,
      focused: false,
      ghost: false,
      restoreCamera: undefined,
      isolate: false,
      visible: s.visible.includes(id) ? s.visible.filter((x) => x !== id) : [...s.visible, id],
    }));
  };
  const reset = () => {
    remember();
    setState((s) => ({ ...initial, visible: DEFAULT_VISIBLE, reset: s.reset + 1 }));
    setChosen(null);
    setDetails(false);
    setPanel(null);
  };
  const openPanel = (next: "layers" | "search") => {
    setDetails(false);
    setPanel((p) => (p === next ? null : next));
  };
  return (
    <main className="studio">
      {atlas && (
        <AnatomyScene
          atlas={atlas}
          state={{
            ...state,
            anchor: state.anchor && chosen ? { ...state.anchor, label: label(chosen) } : undefined,
            inspectorOpen: details && !!chosen,
          }}
          onCameraChange={(pose) => {
            camera.current = pose;
          }}
          onSelect={choosePart}
          onProgress={(n) => {
            setProgress(n);
            if (n === 100) setError("");
          }}
          onError={setError}
        />
      )}
      <div className="vignette" />
      <header className="identity">
        <div className="eyebrow">
          <span className="status-dot" /> INTERACTIVE ANATOMY
        </div>
        <h1>
          Human Atlas
          <Badge variant="outline" className="edition">
            3D
          </Badge>
        </h1>
        <div className="identity-meta">
          {atlas ? atlas.parts.length.toLocaleString() : "2,234"} modeled pieces <span>·</span>{" "}
          BodyParts3D + Z-Anatomy
        </div>
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
          aria-label="Search anatomy"
        >
          <Search size={18} />
          <span>Find a structure</span>
          <kbd>/</kbd>
        </Button>
        <Button
          variant="ghost"
          className="icon-button"
          aria-label="About this atlas"
          onClick={() => {
            setDetails(false);
            setPanel(null);
            setAbout(true);
          }}
        >
          <Info size={18} />
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
            onClick={() =>
              setState((s) => ({
                ...s,
                selected: [],
                anchor: undefined,
                focused: false,
                ghost: false,
                restoreCamera: undefined,
                isolate: false,
                visible: activeSystems.map((x) => x.id),
              }))
            }
          >
            All
          </Button>
          <Button
            variant="ghost"
            aria-pressed={state.visible.length === 1 && state.visible[0] === "skeletal"}
            onClick={() =>
              setState((s) => ({
                ...s,
                selected: [],
                anchor: undefined,
                focused: false,
                ghost: false,
                restoreCamera: undefined,
                isolate: false,
                visible: ["skeletal"],
              }))
            }
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
              setState((s) => ({
                ...s,
                selected: [],
                anchor: undefined,
                focused: false,
                ghost: false,
                restoreCamera: undefined,
                isolate: false,
                visible: [
                  "cardiac",
                  "respiratory",
                  "digestive",
                  "urinary",
                  "endocrine",
                  "reproductive",
                ],
              }))
            }
          >
            Organs
          </Button>
        </div>
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
                onClick={() =>
                  setState((v) => ({
                    ...v,
                    visible: [s.id],
                    isolate: false,
                    selected: [],
                    anchor: undefined,
                    focused: false,
                    ghost: false,
                    restoreCamera: undefined,
                  }))
                }
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
          <Button
            variant="ghost"
            onClick={() =>
              setState((s) => ({
                ...s,
                visible: [],
                selected: [],
                isolate: false,
                anchor: undefined,
                focused: false,
                ghost: false,
                restoreCamera: undefined,
              }))
            }
          >
            Hide all
          </Button>
        </div>
      </section>
      {panel === "search" && (
        <section className="search-panel glass" aria-label="Find anatomy">
          <div className="panel-heading">
            <span>Find a structure</span>
            <Button
              variant="ghost"
              className="icon-button"
              onClick={() => setPanel(null)}
              aria-label="Close search"
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
              placeholder="Biceps, skapula, musculocutaneous…"
              aria-label="Search named anatomical structures"
              showTrigger={false}
            />
            <ComboboxContent className="anatomy-search-results">
              <ComboboxEmpty>No structures match your search.</ComboboxEmpty>
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
              : "Bir yapı seçin. Türkçe ve Latince adlandırma omuz–kol örneğiyle genişliyor."}
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
        <Button variant="ghost" aria-label="Reset view and layers" title="Reset" onClick={reset}>
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
                : "ADULT HUMAN · MALE"}
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
        <div className="explode-control">
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
        <Button
          variant="ghost"
          className="dock-reset"
          onClick={reset}
          aria-label="Assemble and reset"
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
          {state.explode > 0.8 ? "Drag to pan" : "Drag to orbit"} <b>·</b> Pinch to zoom <b>·</b>{" "}
          Tap to inspect
        </span>
        <Button
          variant="ghost"
          onClick={() => {
            setDetails(false);
            setPanel(null);
            setAbout(true);
          }}
        >
          Source & credits <ArrowUpRight size={12} />
        </Button>
      </footer>
      {progress < 100 && !error && (
        <div className="loading glass" role="status">
          <Activity size={18} />
          <div>
            <strong>Preparing the anatomy</strong>
            <span>
              {progress}% · Loading {atlas?.parts.length.toLocaleString() ?? "2,234"} pieces
            </span>
            <div className="loading-track">
              <i style={{ width: `${progress}%` }} />
            </div>
          </div>
        </div>
      )}
      {error && (
        <div className="loading glass error" role="alert">
          <p>{error}</p>
          <Button variant="ghost" onClick={() => location.reload()}>
            Reload viewer
          </Button>
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
          className={`detail-sheet glass ${state.isolate ? "is-isolated" : ""}`}
          showCloseButton={true}
        >
          <div className="detail-header">
            <div className="detail-accent" style={{ background: system?.color }} />
            <div className="eyebrow">
              {new Set(selectedParts.map((p) => p.system)).size > 1
                ? "Bileşik yapı"
                : (system?.name ?? "ANATOMİ")}
            </div>
            <SheetTitle ref={detailTitle} tabIndex={-1} className="structure-title">
              {chosen ? label(chosen) : null}
            </SheetTitle>
          </div>
          <div className="detail-scroll" key={`${chosen?.id}-${state.isolate}`}>
            {chosenAnchor && (
              <p className="anchor-note">
                İşaret, kaynak modeldeki kas tutunma yüzeyinin merkezini gösterir; yapının
                sınırlarını temsil etmez. Konum, kaynak modeller arasında aktarılmıştır ve anatomik
                uzman incelemesi bekliyor.
              </p>
            )}
            {chosen && (
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
                            const source = knowledgeSources.get(e.sourceId);
                            return source ? (
                              <a key={i} href={source.url} target="_blank" rel="noreferrer">
                                {source.title}
                              </a>
                            ) : null;
                          })}
                          <p>Kaynakla destekleniyor; uzman incelemesi bekliyor.</p>
                        </details>
                      </div>
                    );
                  })
                )}
              </section>
            )}
            <SheetDescription className="structure-description">
              {chosen && getRepresentationNote(chosen.id)
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
            {chosen &&
              selected &&
              !getRepresentationNote(chosen.id) &&
              !EXPLANATIONS[chosen.name.toLowerCase()] && (
                <span className="context-note">
                  Genel sistem bilgisi · yapıya özel açıklama değildir
                </span>
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
                <h3>Included structures</h3>
                {selectedParts.slice(0, 50).map((p) => (
                  <Button variant="ghost" key={p.id} onClick={() => choosePart(p.id)}>
                    <span>{anatomyLabel(p.conceptId, p.name, language)}</span>
                    <ChevronRight size={14} />
                  </Button>
                ))}
                {selectedParts.length > 50 && (
                  <p>And {selectedParts.length - 50} more modeled pieces.</p>
                )}
              </div>
            )}
            <a
              className="source-link"
              href={
                chosenAnchor || chosen?.id.includes("musculocutaneous")
                  ? "https://github.com/Z-Anatomy/Models-of-human-anatomy"
                  : "https://lifesciencedb.jp/bp3d/"
              }
              target="_blank"
              rel="noreferrer"
            >
              Model kaynağı <ArrowUpRight size={14} />
            </a>
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
                    reset: s.reset + 1,
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
      <CoveragePanel
        open={coverageOpen}
        onOpenChange={setCoverageOpen}
        concepts={conceptMap}
        onChoose={(c) => {
          setCoverageOpen(false);
          choose(c);
        }}
      />
      <Sheet open={about} onOpenChange={setAbout}>
        <SheetContent className="about-sheet glass">
          <div className="eyebrow">SOURCE & SCOPE</div>
          <SheetTitle className="structure-title">A body, revealed.</SheetTitle>
          <SheetDescription>
            Explore the adult male reference anatomy from BodyParts3D.
          </SheetDescription>
          <div className="about-copy">
            <p>
              <strong>Male · BodyParts3D</strong>
              <br />
              2,234 individual meshes and 3,432 named concepts from an adult male reference anatomy.
            </p>
            <p>
              This reference does not contain every human structure or variation. Named concepts can
              contain multiple pieces; each source mesh is rendered once.
            </p>
            <p>
              Colors and system groupings are designed for exploration. The geometry is simplified
              for the web, and short explanations provide general educational context. This is an
              anatomical reference, not a diagnostic or surgical tool.
            </p>
            <h3>Ek sinir modelleri</h3>
            <p>
              Sağ ve sol musculocutaneous sinirler Z-Anatomy kaynak geometrisinden aktarılmıştır.
              Anatomik ilişkiler ve geometri uyumu uzman incelemesi bekler.
            </p>
            <a href="/models/extensions/ATTRIBUTION.md" target="_blank" rel="noreferrer">
              Z-Anatomy kaynak ve atıfları
            </a>
            <h3>Source</h3>
            <p>
              BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0
              International.
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
          </div>
        </SheetContent>
      </Sheet>
    </main>
  );
}
