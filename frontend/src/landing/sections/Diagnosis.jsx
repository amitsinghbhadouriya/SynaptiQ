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
