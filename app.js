const SUPABASE_URL = "https://rlmrgjxvuddexupkobpc.supabase.co";
const SUPABASE_KEY = "sb_publishable_Rx3oyuq56eAo7b_xxWrUaw_LKQKXA59";
const EPISODE_SLUG = "last-53-days-rome";

const headers = {
  apikey: SUPABASE_KEY,
  Authorization: `Bearer ${SUPABASE_KEY}`,
};

async function getJSON(path) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, { headers });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Supabase ${res.status}: ${body}`);
  }
  return res.json();
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function renderEpisode(ep) {
  document.title = `${ep.title} — Echoes of Empires`;
  document.getElementById("episode-title").textContent = ep.title;
  document.getElementById("episode-logline").textContent = ep.logline || "";

  const meta = document.getElementById("episode-meta");
  meta.innerHTML = "";
  const chips = [
    ["Status", ep.status],
    ["Runtime", ep.runtime],
    ["Format", "Full-length animated history"],
    ["Voice", "Human narrator"],
  ];
  for (const [k, v] of chips) {
    const c = el("span", "chip" + (k === "Status" ? " status" : ""));
    c.append(`${k}: `);
    const strong = el("strong", "", v || "—");
    c.append(strong);
    meta.append(c);
  }
}

function renderStats(scenes) {
  const words = scenes.reduce((n, s) => n + (s.narration || "").split(/\s+/).filter(Boolean).length, 0);
  const estMin = Math.round(words / 165);
  const stats = document.getElementById("stats");
  stats.innerHTML = "";
  const items = [
    [String(scenes.length), "Scenes"],
    [String(words.toLocaleString()), "Narration words"],
    [`~${estMin} min`, "Estimated voice runtime"],
    ["53", "Days of the siege"],
  ];
  for (const [num, label] of items) {
    const box = el("div", "stat");
    box.append(el("div", "num", num));
    box.append(el("div", "label", label));
    stats.append(box);
  }
}

function renderScenes(scenes) {
  const wrap = document.getElementById("scenes");
  wrap.innerHTML = "";
  for (const s of scenes) {
    const card = el("article", "scene");

    const time = el("div", "scene-time", s.timecode || "");

    const body = el("div");
    const head = el("div", "scene-head");
    head.append(el("span", "scene-order", `SCENE ${String(s.scene_order).padStart(2, "0")}`));
    if (s.chapter) head.append(el("span", "scene-chapter", s.chapter));
    if (s.title) head.append(el("span", "scene-title", s.title));
    body.append(head);

    if (s.narration) body.append(el("div", "narration", s.narration));

    const tags = el("div", "tags");
    if (s.captions) {
      const t = el("span", "tag");
      t.append("CAPTIONS: ");
      t.append(el("b", "", s.captions));
      tags.append(t);
    }
    if (s.visual) {
      const t = el("span", "tag");
      t.append("VISUAL: ");
      t.append(document.createTextNode(s.visual));
      tags.append(t);
    }
    if (s.audio) {
      const t = el("span", "tag");
      t.append("AUDIO: ");
      t.append(document.createTextNode(s.audio));
      tags.append(t);
    }
    body.append(tags);

    card.append(time, body);
    wrap.append(card);
  }
}

function renderSources(sources) {
  const wrap = document.getElementById("sources");
  wrap.innerHTML = "";
  for (const s of sources) {
    const row = el("div", "source");
    row.append(el("span", "kind", s.label || "Source"));
    const detail = el("div");
    detail.append(el("div", "", s.detail || ""));
    if (s.url) {
      const a = document.createElement("a");
      a.href = s.url;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = s.url;
      detail.append(a);
    }
    row.append(detail);
    wrap.append(row);
  }
}

async function main() {
  const scenesEl = document.getElementById("scenes");
  scenesEl.innerHTML = `<div class="loading">Loading production data…</div>`;
  try {
    const [episodes, scenes, sources] = await Promise.all([
      getJSON(`yt_episodes?slug=eq.${EPISODE_SLUG}&select=*`),
      getJSON(`yt_scenes?episode_slug=eq.${EPISODE_SLUG}&order=scene_order.asc&select=*`),
      getJSON(`yt_sources?episode_slug=eq.${EPISODE_SLUG}&select=*`),
    ]);

    if (!episodes.length) throw new Error("Episode not found.");
    renderEpisode(episodes[0]);
    renderStats(scenes);
    renderScenes(scenes);
    renderSources(sources);
  } catch (err) {
    scenesEl.innerHTML = "";
    scenesEl.append(el("div", "error", `Could not load production data. ${err.message}`));
    console.error(err);
  }
}

main();
