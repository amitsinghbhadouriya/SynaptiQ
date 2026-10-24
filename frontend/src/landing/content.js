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
    key: 'ingest',
    title: 'Document ingestion',
    short: 'Ingestion',
    body: 'Upload PDF, DOCX or TXT. SynaptiQ extracts the text, keeps filenames, pages and headings, and reports clear errors for empty, scanned or damaged files.',
    points: ['PyMuPDF for PDF pages', 'python-docx for headings and tables', 'Size and type validation']
  },
  {
    key: 'chunk',
    title: 'Chunking & vector index',
    short: 'Indexing',
    body: 'Sentence-aware chunks with configurable size and overlap, stable IDs and exact character offsets, embedded with Sentence Transformers and stored in ChromaDB.',
    points: ['Stable, reproducible chunk IDs', 'Offsets link chunks to evidence', 'Index reused per configuration']
  },
  {
    key: 'tests',
    title: 'Synthetic test sets',
    short: 'Test sets',
    body: 'Generate factual, numerical, multi-hop and unanswerable questions with reference answers and evidence spans — then review them before they count.',
    points: ['Evidence located in the source', 'Human review: approve or reject', 'Import your own reviewed sets']
  },
  {
    key: 'modes',
    title: 'Three-mode evaluation',
    short: 'Three modes',
    body: 'Retriever-only, generator-only with reference evidence, and end-to-end tests run as separate modes with a common result schema.',
    points: ['Hit@k, recall, precision, MRR', 'Correctness, faithfulness, relevancy', 'Abstention on unanswerable questions']
  },
  {
    key: 'evidence',
    title: 'Evidence inspection',
    short: 'Evidence',
    body: 'For every question see the reference answer, the supporting passage, each retrieved chunk with its rank and whether it contains the evidence, and the generated answers.',
    points: ['Per-chunk evidence coverage', 'Answers from both generation modes', 'Latency and cost when measured']
  },
  {
    key: 'diagnose',
    title: 'Root-cause report',
    short: 'Diagnosis',
    body: 'Transparent rules classify each question as a retrieval, generation, combined or pipeline failure, correct-but-ungrounded, or needs review — with the reason shown.',
    points: ['Three-state inputs, never guessed', 'Rationale and next action', 'Uncertain when evidence is thin']
  },
  {
    key: 'recommend',
    title: 'Fix recommendations',
    short: 'Recommendations',
    body: 'Diagnoses become concrete experiments: the exact rank of missing evidence suggests a top-k, partial coverage suggests chunking, over-abstention suggests a threshold.',
    points: ['One change at a time', 'Hypotheses, not promises', 'One click to test it']
  },
  {
    key: 'compare',
    title: 'Before / after experiments',
    short: 'Experiments',
    body: 'Run the same questions against two configurations and compare raw scores, fixed and regressed questions, latency and cost — with warnings for small samples.',
    points: ['Same question IDs enforced', 'Config diff recorded', 'CSV / JSON export and SQLite history']
  }
];

export const DIAGNOSIS_RULES = [
  { evidence: 'Supporting chunk is absent from the retrieved results', diagnosis: 'Retrieval failure', action: 'Inspect chunking, embedding model, top-k and ranking' },
  { evidence: 'Evidence supplied directly, yet the generator answer is wrong or unsupported', diagnosis: 'Generation failure', action: 'Inspect prompt, model and context handling' },
  { evidence: 'Retrieval misses the evidence and the final answer is unsupported', diagnosis: 'Combined failure', action: 'Fix retrieval first, then repeat generation tests' },
  { evidence: 'Final answer is correct but the retrieved evidence is irrelevant', diagnosis: 'Correct but ungrounded', action: 'Do not treat the answer as evidence-grounded' },
  { evidence: 'Metrics conflict or the reference is ambiguous', diagnosis: 'Needs review', action: 'Inspect the source and the test question' }
];

export const PIPELINE = [
  'Upload document',
  'Validate type & size',
  'Extract text + metadata',
  'Chunk & assign IDs',
  'Embed & index in ChromaDB',
  'Generate / import questions',
  'Human review',
  'Run three test modes',
  'Diagnose likely cause',
  'Recommend a change',
  'Re-run the same set',
  'Compare & export'
];

export const STACK = [
  { name: 'Python', role: 'Core logic & pipeline', glyph: 'Py' },
  { name: 'Streamlit', role: 'Web UI & dashboard host', glyph: 'St' },
  { name: 'FastAPI', role: 'REST API', glyph: 'Fa' },
  { name: 'PyMuPDF', role: 'PDF extraction', glyph: 'Mu' },
  { name: 'python-docx', role: 'DOCX extraction', glyph: 'Dx' },
  { name: 'Sentence Transformers', role: 'Embeddings', glyph: 'ST' },
  { name: 'ChromaDB', role: 'Vector index & metadata', glyph: 'Ch' },
  { name: 'Ragas', role: 'RAG evaluation metrics', glyph: 'Ra' },
  { name: 'Pandas', role: 'Results tables', glyph: 'Pd' },
  { name: 'Plotly', role: 'Charts', glyph: 'Pl' },
  { name: 'SQLite', role: 'Run history', glyph: 'SQ' },
  { name: 'Pytest', role: 'Automated tests', glyph: 'Pt' }
];
