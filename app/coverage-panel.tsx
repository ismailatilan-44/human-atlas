import coverage from "../data/anatomy/coverage.json";
import { anatomyLabel, getRepresentationNote } from "./atlas-metadata";
import type { Concept } from "./anatomy";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTitle, SheetDescription } from "@/components/ui/sheet";

const states: Record<string, string> = {
  existing: "Mevcut",
  partial: "Kısmi",
  missing: "Eksik",
  unverified: "İnceleme bekliyor",
};
export default function CoveragePanel({
  open,
  onOpenChange,
  concepts,
  onChoose,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  concepts: Map<string, Concept>;
  onChoose: (concept: Concept) => void;
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
              {region.targets.map((target) => (
                <div className="coverage-target" key={target.id}>
                  <div>
                    <strong>{target.nameTr}</strong>
                    <span className={`coverage-state ${target.state}`}>{states[target.state]}</span>
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
              ))}
            </details>
          ))}
        </div>
      </SheetContent>
    </Sheet>
  );
}
