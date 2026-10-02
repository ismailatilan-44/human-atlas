import rightAnkle from '../data/study/right-ankle-v1.json';
import leftAnkle from '../data/study/left-ankle-v1.json';
import rightUpperLimb from '../data/study/right-upper-limb-bones-v1.json';
import type { DatasetId } from './anatomy';

export type StudyPack = {
  schemaVersion: number;
  id: string;
  /** Increment when a prompt, answer identity or its source interpretation changes. */
  version: string;
  datasetId: DatasetId;
  title: string;
  labelSource: string;
  attribution: string;
  expertReview: string;
  scope: string;
  learningGoals: string[];
  items: {
    id: string; conceptId: string; sourceObject: string;
    geometryPartId?: string;
    evidence: { sourceId: string; locator: string; scope?: string }[];
  }[];
};

// Keep the original reviewed question IDs and evidence unchanged.
export const studyPacks: StudyPack[] = [
  { ...rightAnkle, datasetId: 'lower-limb-nerve-reference', version: '1',
    scope: 'Dokuz sağ kaynak kemiğinin adını ve tarafını tanıma; tam bölge veya uzman onaylı sınav değildir.',
    learningGoals: ['Vurgulanan kaynak yüzeyini adı ve tarafıyla eşleştir.', 'Yanlış veya atlanan yanıtı kaynak kanıtıyla düzelt.'] },
  { ...leftAnkle, datasetId: 'lower-limb-nerve-reference' },
  { ...rightUpperLimb, datasetId: 'upper-limb-nerve-reference' },
];

export function studyPack(id: string): StudyPack | undefined {
  return studyPacks.find(pack => pack.id === id);
}
