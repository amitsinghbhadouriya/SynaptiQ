"""Scroll Expand Media component for Python & Streamlit.

Converted from scroll-expansion-hero and demo.tsx.
Zero node_modules or npm required.
"""

from __future__ import annotations

import streamlit.components.v1 as components


def render_scroll_expansion_demo(height: int = 650) -> None:
    """Renders the scroll-expansion hero demo in Streamlit."""
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          background: #090d16;
          color: #f1f5f9;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          overflow-x: hidden;
        }

        .scroll-container {
          position: relative;
          width: 100%;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 2rem 1rem;
        }

        .tabs {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 1.5rem;
          background: rgba(255, 255, 255, 0.08);
          padding: 4px;
          border-radius: 9999px;
        }

        .tab-btn {
          border: none;
          background: transparent;
          color: #94a3b8;
          padding: 8px 20px;
          border-radius: 9999px;
          cursor: pointer;
          font-weight: 500;
          font-size: 14px;
          transition: all 0.2s ease;
        }

        .tab-btn.active {
          background: #3b82f6;
          color: #ffffff;
        }

        .hero-card {
          position: relative;
          width: 80%;
          max-width: 900px;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
          transition: width 0.3s ease, border-radius 0.3s ease;
        }

        .media-box {
          position: relative;
          width: 100%;
          height: 380px;
          overflow: hidden;
        }

        .media-box img, .media-box video {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
        }

        .media-overlay {
          position: absolute;
          inset: 0;
          background: linear-gradient(to top, rgba(9, 13, 22, 0.95), transparent 60%);
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          padding: 24px 32px;
        }

        .date-badge {
          display: inline-block;
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: #38bdf8;
          margin-bottom: 6px;
        }

        .title {
          font-size: 26px;
          font-weight: 700;
          color: #ffffff;
          margin-bottom: 10px;
        }

        .about-section {
          padding: 24px 32px;
          background: rgba(15, 23, 42, 0.6);
          border-top: 1px solid rgba(255, 255, 255, 0.08);
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .about-overview {
          font-size: 14px;
          line-height: 1.6;
          color: #cbd5e1;
        }

        .about-conclusion {
          font-size: 13.5px;
          line-height: 1.6;
          color: #94a3b8;
          font-style: italic;
        }

        .slider-controls {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-top: 16px;
          font-size: 13px;
          color: #94a3b8;
        }

        .slider-controls input {
          width: 200px;
        }
      </style>
    </head>
    <body>
      <div class="scroll-container">
        <div class="tabs">
          <button class="tab-btn active" id="btn-video" onclick="switchMedia('video')">Video Mode</button>
          <button class="tab-btn" id="btn-image" onclick="switchMedia('image')">Image Mode</button>
        </div>

        <div class="hero-card" id="heroCard">
          <div class="media-box" id="mediaBox">
            <video id="videoEl" autoplay loop muted playsinline poster="https://cdn.21st.dev/assets/localized/5bb1be92440e920def3eb36ad5a610d609240616cd8b11c0effe6b92bcafe06e.jpg">
              <source src="https://me7aitdbxq.ufs.sh/f/2wsMIGDMQRdYuZ5R8ahEEZ4aQK56LizRdfBSqeDMsmUIrJN1" type="video/mp4">
            </video>
            <img id="imageEl" src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1920&q=80" style="display:none;" alt="Showcase">
            <div class="media-overlay">
              <span class="date-badge" id="dateBadge">Cosmic Journey</span>
              <h2 class="title" id="titleText">Immersive Video Experience</h2>
            </div>
          </div>
          <div class="about-section">
            <p class="about-overview" id="overviewText">
              This is a demonstration of the ScrollExpandMedia component. As you interact, the media expands to fill more of the screen, creating an immersive experience.
            </p>
            <p class="about-conclusion" id="conclusionText">
              The component provides a unique way to engage users with your content through interactive expansion.
            </p>
          </div>
        </div>

        <div class="slider-controls">
          <span>Expand Preview:</span>
          <input type="range" id="sizeRange" min="70" max="100" value="80" oninput="updateExpand(this.value)">
          <span id="rangeLabel">80%</span>
        </div>
      </div>

      <script>
        const content = {
          video: {
            title: "Immersive Video Experience",
            date: "Cosmic Journey",
            overview: "This is a demonstration of the ScrollExpandMedia component with a video. As you scroll, the video expands to fill more of the screen, creating an immersive experience.",
            conclusion: "The ScrollExpandMedia component provides a unique way to engage users with your content through interactive scrolling."
          },
          image: {
            title: "Dynamic Image Showcase",
            date: "Underwater Adventure",
            overview: "This is a demonstration of the ScrollExpandMedia component with an image. The same smooth expansion effect works beautifully with static images.",
            conclusion: "The component works equally well with images and videos, maintaining an engaging user experience."
          }
        };

        function switchMedia(type) {
          document.getElementById('btn-video').classList.toggle('active', type === 'video');
          document.getElementById('btn-image').classList.toggle('active', type === 'image');

          const videoEl = document.getElementById('videoEl');
          const imageEl = document.getElementById('imageEl');
          const dateBadge = document.getElementById('dateBadge');
          const titleText = document.getElementById('titleText');
          const overviewText = document.getElementById('overviewText');
          const conclusionText = document.getElementById('conclusionText');

          if (type === 'video') {
            videoEl.style.display = 'block';
            imageEl.style.display = 'none';
          } else {
            videoEl.style.display = 'none';
            imageEl.style.display = 'block';
          }

          dateBadge.textContent = content[type].date;
          titleText.textContent = content[type].title;
          overviewText.textContent = content[type].overview;
          conclusionText.textContent = content[type].conclusion;
        }

        function updateExpand(val) {
          const card = document.getElementById('heroCard');
          card.style.width = val + '%';
          card.style.maxWidth = val === '100' ? '100%' : '900px';
          document.getElementById('rangeLabel').textContent = val + '%';
        }
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

