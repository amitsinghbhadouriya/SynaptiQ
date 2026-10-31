"""Magic UI Animated Terminal component for Python & Streamlit.

Runs with ZERO node_modules or npm dependencies.
Embeds directly into any Streamlit app using standard Streamlit components.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


def render_terminal_demo(height: int = 440) -> None:
    """Renders the Magic UI Terminal demo inside Streamlit without Node.js."""
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          background-color: transparent;
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 10px;
        }

        .terminal-container {
          width: 100%;
          max-width: 580px;
          background: #090d16;
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 12px;
          box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 24px 0 rgba(14, 165, 233, 0.12);
          overflow: hidden;
          color: #e2e8f0;
          font-size: 13.5px;
        }

        .terminal-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 10px 16px;
          background: rgba(255, 255, 255, 0.02);
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .terminal-dots {
          display: flex;
          gap: 7px;
          align-items: center;
        }

        .terminal-dot {
          width: 11px;
          height: 11px;
          border-radius: 50%;
        }

        .dot-red { background: #ef4444; }
        .dot-yellow { background: #eab308; }
        .dot-green { background: #22c55e; }

        .terminal-title {
          font-size: 11.5px;
          color: #64748b;
          letter-spacing: 0.04em;
        }

        .terminal-body {
          padding: 16px 20px;
          display: flex;
          flex-direction: column;
          gap: 6px;
          line-height: 1.5;
          min-height: 320px;
        }

        .terminal-line {
          display: flex;
          align-items: center;
          opacity: 0;
          transform: translateY(-4px);
          transition: opacity 0.28s ease, transform 0.28s ease;
        }

        .terminal-line.visible {
          opacity: 1;
          transform: translateY(0);
        }

        .text-green-500 {
          color: #22c55e;
        }

        .text-blue-500 {
          color: #3b82f6;
        }

        .text-muted-foreground {
          color: #94a3b8;
        }

        .pl-2 {
          padding-left: 10px;
        }

        .typing-cursor {
          display: inline-block;
          width: 7px;
          height: 14px;
          margin-left: 3px;
          vertical-align: middle;
          background: #38bdf8;
          animation: blink 1s step-start infinite;
        }

        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
      </style>
    </head>
    <body>
      <div class="terminal-container">
        <div class="terminal-header">
          <div class="terminal-dots">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
          </div>
          <span class="terminal-title">bash — 80x24</span>
        </div>
        <div class="terminal-body" id="terminal-body">
          <div class="terminal-line visible" id="cmd-line">
            <span id="cmd-text"></span>
            <span class="typing-cursor" id="cmd-cursor"></span>
          </div>

          <div class="terminal-line text-green-500" id="step-0">✔ Preflight checks.</div>
          <div class="terminal-line text-green-500" id="step-1">✔ Verifying framework. Found Next.js.</div>
          <div class="terminal-line text-green-500" id="step-2">✔ Validating Tailwind CSS.</div>
          <div class="terminal-line text-green-500" id="step-3">✔ Validating import alias.</div>
          <div class="terminal-line text-green-500" id="step-4">✔ Writing components.json.</div>
          <div class="terminal-line text-green-500" id="step-5">✔ Checking registry.</div>
          <div class="terminal-line text-green-500" id="step-6">✔ Updating tailwind.config.ts</div>
          <div class="terminal-line text-green-500" id="step-7">✔ Updating app/globals.css</div>
          <div class="terminal-line text-green-500" id="step-8">✔ Installing dependencies.</div>

          <div class="terminal-line text-blue-500" id="step-9">
            <span>ℹ Updated 1 file:</span>
            <span class="pl-2">- lib/utils.ts</span>
          </div>

          <div class="terminal-line text-muted-foreground" id="step-10">
            <span id="success-1"></span>
          </div>
          <div class="terminal-line text-muted-foreground" id="step-11">
            <span id="success-2"></span>
          </div>
        </div>
      </div>

      <script>
        const command = "> pnpm dlx shadcn@latest init";
        const success1 = "Success! Project initialization completed.";
        const success2 = "You may now add components.";

        let charIndex = 0;
        const cmdTextEl = document.getElementById("cmd-text");
        const cursorEl = document.getElementById("cmd-cursor");

        function typeCommand() {
          if (charIndex < command.length) {
            cmdTextEl.textContent += command.charAt(charIndex);
            charIndex++;
            setTimeout(typeCommand, 38);
          } else {
            cursorEl.style.display = "none";
            startSpans();
          }
        }

        function startSpans() {
          const spansCount = 10; // steps 0 to 9
          let step = 0;

          function nextSpan() {
            if (step < spansCount) {
              const el = document.getElementById("step-" + step);
              if (el) el.classList.add("visible");
              step++;
              setTimeout(nextSpan, 180);
            } else {
              typeSuccess1();
            }
          }
          setTimeout(nextSpan, 200);
        }

        function typeSuccess1() {
          const el = document.getElementById("step-10");
          el.classList.add("visible");
          const textEl = document.getElementById("success-1");
          let i = 0;

          function typeChar() {
            if (i < success1.length) {
              textEl.textContent += success1.charAt(i);
              i++;
              setTimeout(typeChar, 30);
            } else {
              setTimeout(typeSuccess2, 200);
            }
          }
          typeChar();
        }

        function typeSuccess2() {
          const el = document.getElementById("step-11");
          el.classList.add("visible");
          const textEl = document.getElementById("success-2");
          let i = 0;

          function typeChar() {
            if (i < success2.length) {
              textEl.textContent += success2.charAt(i);
              i++;
              setTimeout(typeChar, 30);
            }
          }
          typeChar();
        }

        // Start animation
        setTimeout(typeCommand, 300);
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)


def render_synaptiq_terminal(height: int = 440) -> None:
    """Renders the SynaptiQ RAG Diagnostic Terminal demo inside Streamlit."""
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          background-color: transparent;
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
          display: flex; justify-content: center; align-items: center; padding: 10px;
        }
        .terminal-container {
          width: 100%; max-width: 580px; background: #090d16;
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 12px;
          box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 24px 0 rgba(14, 165, 233, 0.12);
          overflow: hidden; color: #e2e8f0; font-size: 13.5px;
        }
        .terminal-header {
          display: flex; align-items: center; justify-content: space-between;
          padding: 10px 16px; background: rgba(255, 255, 255, 0.02);
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .terminal-dots { display: flex; gap: 7px; align-items: center; }
        .terminal-dot { width: 11px; height: 11px; border-radius: 50%; }
        .dot-red { background: #ef4444; }
        .dot-yellow { background: #eab308; }
        .dot-green { background: #22c55e; }
        .terminal-title { font-size: 11.5px; color: #64748b; }
        .terminal-body {
          padding: 16px 20px; display: flex; flex-direction: column;
          gap: 6px; line-height: 1.5; min-height: 300px;
        }
        .terminal-line {
          display: flex; align-items: center; opacity: 0; transform: translateY(-4px);
          transition: opacity 0.28s ease, transform 0.28s ease;
        }
        .terminal-line.visible { opacity: 1; transform: translateY(0); }
        .text-green-500 { color: #22c55e; }
        .text-blue-500 { color: #3b82f6; }
        .text-muted-foreground { color: #94a3b8; }
        .pl-2 { padding-left: 10px; }
        .typing-cursor {
          display: inline-block; width: 7px; height: 14px; margin-left: 3px;
          vertical-align: middle; background: #38bdf8;
          animation: blink 1s step-start infinite;
        }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
      </style>
    </head>
    <body>
      <div class="terminal-container">
        <div class="terminal-header">
          <div class="terminal-dots">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
          </div>
          <span class="terminal-title">synaptiq-cli — zsh</span>
        </div>
        <div class="terminal-body">
          <div class="terminal-line visible">
            <span id="cmd-text"></span>
            <span class="typing-cursor" id="cmd-cursor"></span>
          </div>
          <div class="terminal-line text-green-500" id="s0">✔ Initializing ChromaDB vector embeddings.</div>
          <div class="terminal-line text-green-500" id="s1">✔ Ingesting handbook.pdf (chunk size: 280, top_k: 1).</div>
          <div class="terminal-line text-green-500" id="s2">✔ Running independent Retriever & Generator tests.</div>
          <div class="terminal-line text-blue-500" id="s3">
            <span>ℹ Diagnosis: LIKELY_RETRIEVAL_FAILURE (Pass rate: 71%)</span>
            <span class="pl-2">- Recommended tuning: Increase top_k to 2</span>
          </div>
          <div class="terminal-line text-green-500" id="s4">✔ Verifying candidate fix on identical question benchmark.</div>
          <div class="terminal-line text-green-500" id="s5">✔ Verification passed! Pass rate improved 71% → 86%.</div>
          <div class="terminal-line text-muted-foreground" id="s6">
            <span id="finish-text"></span>
          </div>
        </div>
      </div>
      <script>
        const cmd = "> streamlit run app.py --demo";
        const finish = "Benchmark verified: 0 regressions, delta +15.0%.";
        let c = 0;
        const cmdEl = document.getElementById("cmd-text");
        const curEl = document.getElementById("cmd-cursor");

        function typeCmd() {
          if (c < cmd.length) {
            cmdEl.textContent += cmd.charAt(c);
            c++;
            setTimeout(typeCmd, 38);
          } else {
            curEl.style.display = "none";
            startSteps();
          }
        }

        function startSteps() {
          let s = 0;
          function nxt() {
            if (s <= 5) {
              const el = document.getElementById("s" + s);
              if (el) el.classList.add("visible");
              s++;
              setTimeout(nxt, 220);
            } else {
              typeFinish();
            }
          }
          setTimeout(nxt, 200);
        }

        function typeFinish() {
          const el = document.getElementById("s6");
          el.classList.add("visible");
          const ft = document.getElementById("finish-text");
          let i = 0;
          function tf() {
            if (i < finish.length) {
              ft.textContent += finish.charAt(i);
              i++;
              setTimeout(tf, 30);
            }
          }
          tf();
        }

        setTimeout(typeCmd, 300);
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

