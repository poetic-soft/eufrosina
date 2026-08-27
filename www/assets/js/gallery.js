(() => {
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const behavior = prefersReduced ? "instant" : "smooth";

  const viewportOf = (el) => {
    const root = el.closest("[data-gallery]");
    return root ? root.querySelector("[data-gallery-viewport]") : null;
  };

  const step = (viewport, dir) => {
    viewport.scrollBy({ left: dir * viewport.clientWidth, behavior });
  };

  document.addEventListener("click", (event) => {
    const next = event.target.closest("[data-gallery-next]");
    const prev = event.target.closest("[data-gallery-prev]");
    if (!next && !prev) return;

    const viewport = viewportOf(next || prev);
    if (!viewport) return;

    event.preventDefault();
    step(viewport, next ? 1 : -1);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;

    const viewport = event.target.closest("[data-gallery-viewport]");
    if (!viewport) return;

    event.preventDefault();
    step(viewport, event.key === "ArrowRight" ? 1 : -1);
  });
})();
