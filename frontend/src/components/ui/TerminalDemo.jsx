import {
  AnimatedSpan,
  Terminal,
  TypingAnimation,
} from "@/registry/magicui/terminal";

export function TerminalDemo() {
  return (
    <Terminal>
      <TypingAnimation>&gt; pnpm dlx shadcn@latest init</TypingAnimation>

      <AnimatedSpan className="text-green-500">
        ✔ Preflight checks.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Verifying framework. Found Next.js.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Validating Tailwind CSS.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Validating import alias.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Writing components.json.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Checking registry.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Updating tailwind.config.ts
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Updating app/globals.css
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Installing dependencies.
      </AnimatedSpan>

      <AnimatedSpan className="text-blue-500">
        <span>ℹ Updated 1 file:</span>
        <span className="pl-2">- lib/utils.ts</span>
      </AnimatedSpan>

      <TypingAnimation className="text-muted-foreground">
        Success! Project initialization completed.
      </TypingAnimation>

      <TypingAnimation className="text-muted-foreground">
        You may now add components.
      </TypingAnimation>
    </Terminal>
  );
}

/**
 * SynaptiQ specialized terminal demo showing RAG ingestion, evaluation & diagnosis
 */
export function SynaptiqTerminalDemo() {
  return (
    <Terminal title="synaptiq-cli — zsh">
      <TypingAnimation>&gt; streamlit run app.py --demo</TypingAnimation>

      <AnimatedSpan className="text-green-500">
        ✔ Initializing ChromaDB vector embeddings.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Ingesting handbook.pdf (chunk size: 280, top_k: 1).
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Running independent Retriever & Generator tests.
      </AnimatedSpan>

      <AnimatedSpan className="text-blue-500">
        <span>ℹ Diagnosis: LIKELY_RETRIEVAL_FAILURE (Pass rate: 71%)</span>
        <span className="pl-2">- Recommended tuning: Increase top_k to 2</span>
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Verifying candidate fix on identical question benchmark.
      </AnimatedSpan>

      <AnimatedSpan className="text-green-500">
        ✔ Verification passed! Pass rate improved 71% → 86%.
      </AnimatedSpan>

      <TypingAnimation className="text-muted-foreground">
        Benchmark verified: 0 regressions, delta +15.0%.
      </TypingAnimation>
    </Terminal>
  );
}

export default TerminalDemo;

