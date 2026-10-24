import { useState } from 'react';
import { Copy, Check, Terminal, FileCode2, Info } from 'lucide-react';

import ScrollReveal from '../../components/reactbits/ScrollReveal.jsx';
import { DIAGNOSIS_RULES } from '../content.js';
import { SectionHeading } from '../shared.jsx';

const CODE_RAW = `def diagnose(retrieval, generator, end_to_end):
    # three-state inputs: True, False or None (not measured)

    if retrieval is False and generator is True:
        return "LIKELY_RETRIEVAL_FAILURE"

    if retrieval is True and generator is False:
        return "LIKELY_GENERATION_FAILURE"

    if retrieval is False and end_to_end is False:
        return "LIKELY_COMBINED_FAILURE"

    if retrieval and generator:
        return "PASS" if end_to_end else "PIPELINE_INTERACTION"

    return "UNCERTAIN_REQUIRES_REVIEW"`;

const CODE = [
  ['k', 'def '], ['f', 'diagnose'], ['p', '(retrieval, generator, end_to_end):'],
  ['n', ''],
  ['c', '    # three-state inputs: True, False or None (not measured)'],
  ['n', ''],
  ['k', '    if '], ['p', 'retrieval '], ['k', 'is '], ['v', 'False '], ['k', 'and '], ['p', 'generator '], ['k', 'is '], ['v', 'True'], ['p', ':'],
  ['n', ''],
  ['k', '        return '], ['s', '"LIKELY_RETRIEVAL_FAILURE"'],
  ['n', ''],
  ['k', '    if '], ['p', 'retrieval '], ['k', 'is '], ['v', 'True '], ['k', 'and '], ['p', 'generator '], ['k', 'is '], ['v', 'False'], ['p', ':'],
  ['n', ''],
  ['k', '        return '], ['s', '"LIKELY_GENERATION_FAILURE"'],
  ['n', ''],
  ['k', '    if '], ['p', 'retrieval '], ['k', 'is '], ['v', 'False '], ['k', 'and '], ['p', 'end_to_end '], ['k', 'is '], ['v', 'False'], ['p', ':'],
  ['n', ''],
  ['k', '        return '], ['s', '"LIKELY_COMBINED_FAILURE"'],
  ['n', ''],
  ['k', '    if '], ['p', 'retrieval '], ['k', 'and '], ['p', 'generator:'],
  ['n', ''],
  ['k', '        return '], ['s', '"PASS" '], ['k', 'if '], ['p', 'end_to_end '], ['k', 'else '], ['s', '"PIPELINE_INTERACTION"'],
  ['n', ''],
  ['k', '    return '], ['s', '"UNCERTAIN_REQUIRES_REVIEW"']
];

const DIAGNOSIS_BADGES = {
  'Retrieval failure': { color: '#0ea5e9', bg: 'rgba(14, 165, 233, 0.12)', border: 'rgba(14, 165, 233, 0.3)' },
  'Generation failure': { color: '#a855f7', bg: 'rgba(168, 85, 247, 0.12)', border: 'rgba(168, 85, 247, 0.3)' },
  'Combined failure': { color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.12)', border: 'rgba(244, 63, 94, 0.3)' },
  'Correct but ungrounded': { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.12)', border: 'rgba(245, 158, 11, 0.3)' },
  'Needs review': { color: '#94a3b8', bg: 'rgba(148, 163, 184, 0.12)', border: 'rgba(148, 163, 184, 0.3)' }
};

export default function Diagnosis() {
  const [copied, setCopied] = useState(false);
  const [selectedDiagnosis, setSelectedDiagnosis] = useState(null);

  const copyCode = () => {
    navigator.clipboard?.writeText(CODE_RAW);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="section section--alt" id="diagnosis">
      <div className="section__inner">
        <SectionHeading eyebrow="04 — Root-cause logic">Diagnoses you can audit</SectionHeading>
        <ScrollReveal containerClassName="lead-reveal" textClassName="lead-reveal__text" baseOpacity={0.12} baseRotation={2}>
          A diagnosis is a likely cause supported by reproducible evidence, not a black-box guess. Missing measurements are never
          treated as failures, and ambiguous test results are flagged for human review.
        </ScrollReveal>

        <div className="diagnosis">
          <div className="diagnosis__table" role="table" aria-label="Root-cause diagnosis rules">
            <div className="diagnosis__row diagnosis__row--head" role="row">
              <span role="columnheader">Observed evidence</span>
              <span role="columnheader">Likely diagnosis</span>
              <span role="columnheader">Targeted next action</span>
            </div>
            {DIAGNOSIS_RULES.map(rule => {
              const badgeStyle = DIAGNOSIS_BADGES[rule.diagnosis] || DIAGNOSIS_BADGES['Needs review'];
              const isSelected = selectedDiagnosis === rule.diagnosis;

              return (
                <div
                  key={rule.diagnosis}
                  className={`diagnosis__row cursor-target${isSelected ? ' diagnosis__row--active' : ''}`}
                  role="row"
                  data-cursor-label={rule.diagnosis}
                  onMouseEnter={() => setSelectedDiagnosis(rule.diagnosis)}
                  onMouseLeave={() => setSelectedDiagnosis(null)}
                >
                  <span role="cell" className="diagnosis__evidence">
                    {rule.evidence}
                  </span>
                  <span role="cell" className="diagnosis__cell-badge">
                    <span
                      className="diagnosis__badge"
                      style={{
                        color: badgeStyle.color,
                        backgroundColor: badgeStyle.bg,
                        borderColor: badgeStyle.border
                      }}
                    >
                      <span className="diagnosis__badge-dot" style={{ backgroundColor: badgeStyle.color }} />
                      {rule.diagnosis}
                    </span>
                  </span>
                  <span role="cell" className="diagnosis__action">
                    {rule.action}
                  </span>
                </div>
              );
