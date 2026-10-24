// Landing-page copy, taken from the SynaptiQ README / project documentation.

export const TAGLINE = 'Evaluate with Evidence. Diagnose with Intelligence. Improve with Confidence.';

export const FAILURES = [
  {
    key: 'retrieval',
    title: 'Retrieval failure',
    body: 'The relevant passage was not retrieved, was ranked too low, or was split poorly across chunks.',
    tag: 'Retriever'
  },
  {
    key: 'generation',
    title: 'Generation failure',
    body: 'The right passage was retrieved, but the model ignored it, misread it, contradicted it or added unsupported claims.',
    tag: 'Generator'
  },
  {
    key: 'pipeline',
    title: 'Pipeline interaction',
    body: 'Each part works on its own, yet prompt construction, context limits or ordering break the combined system.',
    tag: 'End-to-end'
  },
  {
    key: 'data',
    title: 'Evaluation-data failure',
    body: 'An ambiguous synthetic question or a wrong reference answer produces a misleading score.',
    tag: 'Test set'
  }
];

export const LOOP = [
  { step: '01', title: 'Evaluate', body: 'Test retrieval, generation and the full pipeline independently on the same reviewed questions.' },
  { step: '02', title: 'Diagnose', body: 'Combine the three results with source evidence to name the likely cause — or say it is uncertain.' },
  { step: '03', title: 'Recommend', body: 'Turn the diagnosis into one targeted change: chunk size, overlap, top-k, embedding model or prompt.' },
  { step: '04', title: 'Verify', body: 'Re-run the identical test set with the change and compare measured metrics, latency and cost.' }
];

export const MODES = [
  { title: 'Retriever-only', body: 'Question → retriever. Returned chunks are compared with labeled evidence.' },
  { title: 'Generator-only', body: 'Question + known-correct evidence → generator, bypassing retrieval.' },
  { title: 'End-to-end', body: 'Normal retrieval plus generation, scored against the reference and the sources.' }
];

export const FEATURES = [
  {
