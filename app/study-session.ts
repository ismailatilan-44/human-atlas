/** In-memory practice; attempts are immutable after submission until explicit Next. */
export type StudySession = {
  phase: 'inspect' | 'recall' | 'feedback' | 'summary';
  index: number; queue: number[]; retry: boolean;
  first: Record<number, 'correct' | 'wrong' | 'skip'>;
  success: number[]; answer?: string | null;
};
export function startStudy(count: number): StudySession {
  return { phase: 'inspect', index: 0, queue: Array.from({ length: count }, (_, i) => i), retry: false, first: {}, success: [] };
}
export type StudyAction = { type: 'next' } | { type: 'answer'; value: string | null; correct: boolean } | { type: 'retry' };
export function studyTransition(s: StudySession, a: StudyAction): StudySession {
  if (a.type === 'answer') {
    if (s.phase !== 'recall') return s;
    const item = s.queue[s.index];
    return { ...s, phase: 'feedback', answer: a.value,
      first: s.retry ? s.first : { ...s.first, [item]: a.value === null ? 'skip' : a.correct ? 'correct' : 'wrong' },
      success: a.correct ? [...new Set([...s.success, item])] : s.success };
  }
  if (a.type === 'retry') {
    if (s.phase !== 'summary') return s;
    const queue = Object.keys(s.first).map(Number).filter(i => !s.success.includes(i));
    return queue.length ? { ...s, phase: 'recall', queue, index: 0, retry: true, answer: undefined } : s;
  }
  if (s.phase === 'inspect') return s.index + 1 < s.queue.length
    ? { ...s, index: s.index + 1 } : { ...s, phase: 'recall', index: 0 };
  if (s.phase !== 'feedback') return s;
  return s.index + 1 < s.queue.length ? { ...s, phase: 'recall', index: s.index + 1, answer: undefined }
    : { ...s, phase: 'summary', answer: undefined };
}
