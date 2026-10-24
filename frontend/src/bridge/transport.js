// One UI, two hosts.
//  * Streamlit: the app runs inside a custom-component iframe and talks to Python through the
//    Streamlit component protocol (render args in, component values out).
//  * Standalone: FastAPI serves the built site; actions go to /api/v1/ui/* over HTTP and the
//    view is picked from the URL hash (#/ or #/dashboard).

const params = new URLSearchParams(window.location.search);
export const inStreamlit = window.parent !== window && !params.has('standalone');

const post = (type, data = {}) => window.parent.postMessage({ isStreamlitMessage: true, type, ...data }, '*');

function fixIframeScrolling() {
  try {
    if (window.frameElement) {
      window.frameElement.removeAttribute('scrolling');
      window.frameElement.setAttribute('scrolling', 'yes');
      window.frameElement.style.overflow = 'auto';
    }
    if (window.parent && window.parent !== window) {
      const parentDoc = window.parent.document;
      if (parentDoc) {
        const iframes = parentDoc.querySelectorAll('iframe');
        iframes.forEach(f => {
          if (f.contentWindow === window || f.getAttribute('title')?.includes('synaptiq_ui') || f.getAttribute('data-testid') === 'stCustomComponentV1') {
            f.removeAttribute('scrolling');
            f.setAttribute('scrolling', 'yes');
            f.style.overflow = 'auto';
          }
        });
      }
    }
  } catch {
    /* ignore cross-origin restrictions */
  }
}

function streamlitBridge(onRender) {
  const onMessage = event => {
    if (event.data?.type === 'streamlit:render') onRender({ ...(event.data.args || {}) });
  };
  window.addEventListener('message', onMessage);
  post('streamlit:componentReady', { apiVersion: 1 });

  const fit = () => {
    let height = 900;
    try {
      height = window.parent.innerHeight || height;
