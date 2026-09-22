import coverage from "../data/anatomy/coverage.json";
import { anatomyLabel, getRepresentationNote } from "./atlas-metadata";
import type { Concept, DatasetId } from "./anatomy";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTitle, SheetDescription } from "@/components/ui/sheet";

const states: Record<string, string> = {
  existing: "Mevcut",
  partial: "Kısmi",
  missing: "Eksik",
  unverified: "İnceleme bekliyor",
};
function separateDataset(target: object): DatasetId | null {
  const reference =
    "separateReference" in target
      ? (target.separateReference as { datasetId?: string } | undefined)
      : undefined;
  return reference?.datasetId === "female-pelvis" || reference?.datasetId === "inner-ear-reference"
    ? reference.datasetId
    : null;
}
export default function CoveragePanel({
  open,
  onOpenChange,
  concepts,
  onChoose,
  onOpenReference,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  concepts: Map<string, Concept>;
  onChoose: (concept: Concept) => void;
  onOpenReference: (dataset: DatasetId) => void;
}) {
  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="coverage-sheet glass">
        <SheetTitle>Bölgesel yapı listesi</SheetTitle>
        <SheetDescription>
          İlk sürüm için izlenen yapı grupları. Bu liste tüm anatominin veya müfredatın eksiksiz
          olduğu anlamına gelmez.
        </SheetDescription>
        <div className="coverage-regions">
          {coverage.regions.map((region) => (
            <details key={region.id} open={region.id === "upper-limb"}>
              <summary>
                {region.nameTr}
                <span>{region.targets.length} hedef</span>
              </summary>
              {region.targets.map((target) => {
                const reference = separateDataset(target);
                return (
                  <div className="coverage-target" key={target.id}>
                    <div>
                      <strong>{target.nameTr}</strong>
                      <span className={`coverage-state ${target.state}`}>
                        {states[target.state]}
                      </span>
                    </div>
                    {target.state !== "existing" && (
                      <p>
                        {target.state === "partial"
                          ? (getRepresentationNote(target.currentBindings[0]?.conceptId ?? "") ??
                            "Bu yapı yalnız kısmen temsil ediliyor.")
                          : target.state === "missing"
                            ? "Bu yapının modeli henüz eklenmedi."
                            : "Konumu henüz doğrulanmadı; kayıtlı ilişkilerini inceleyebilirsiniz."}
                      </p>
                    )}
                    {"representation" in target && target.representation === "surface_anchor" && (
                      <p>Kemik üzerinde tutunma yüzeyini gösteren referans noktası.</p>
                    )}
                    <div className="coverage-bindings">
                      {reference && (
                        <Button variant="ghost" onClick={() => onOpenReference(reference)}>
                          {reference === "female-pelvis" ? "Kadın pelvis" : "İç kulak"} referansını
                          aç →
                        </Button>
                      )}
                      {target.currentBindings.map((binding) => {
                        const concept = concepts.get(binding.conceptId);
                        return concept ? (
                          <Button
                            key={binding.conceptId}
                            variant="ghost"
                            onClick={() => onChoose(concept)}
                          >
                            {anatomyLabel(binding.conceptId, binding.sourceName, "tr")} →
                          </Button>
                        ) : null;
                      })}
                    </div>
                  </div>
                );
              })}
            </details>
          ))}
        </div>
      </SheetContent>
    </Sheet>
  );
}
