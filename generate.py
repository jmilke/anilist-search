import json
import os

with open("/tmp/anilist_tags.json") as f:
    tags_data = json.load(f)

genres_json = json.dumps(tags_data["GenreCollection"])
tags_json = json.dumps(tags_data["MediaTagCollection"])

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>AniList Advanced Filter</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="AniSearch">
  <meta name="theme-color" content="#0b1622">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' fill='%233db4f2'%3E%3Cpath d='M50 5 L95 90 L5 90 Z' fill='none' stroke='%233db4f2' stroke-width='10'/%3E%3Ccircle cx='50' cy='60' r='15' fill='%233db4f2'/%3E%3C/svg%3E">
  <style>
    :root {{
      --bg: #0b1622;
      --card-bg: #151f2e;
      --card-border: #1e293b;
      --text-main: #edf1f5;
      --text-muted: #8ba0b2;
      --accent: #3db4f2;
      --accent-hover: #2ba2e0;
      --include: #26a65b;
      --include-bg: rgba(38, 166, 91, 0.22);
      --include-border: #26a65b;
      --exclude: #ec294b;
      --exclude-bg: rgba(236, 41, 75, 0.22);
      --exclude-border: #ec294b;
      --chip-bg: #1a2738;
      --chip-border: #2a3a4e;
      --radius: 12px;
      --safe-bottom: env(safe-area-inset-bottom, 16px);
      --safe-top: env(safe-area-inset-top, 16px);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: calc(var(--safe-top) + 12px) 16px calc(var(--safe-bottom) + 100px) 16px;
      overflow-x: hidden;
    }}

    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .brand svg {{
      width: 28px;
      height: 28px;
      fill: var(--accent);
    }}

    .brand h1 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: #fff;
    }}

    .brand span {{
      color: var(--accent);
    }}

    .btn-reset {{
      background: none;
      border: 1px solid var(--chip-border);
      color: var(--text-muted);
      font-size: 0.85rem;
      padding: 6px 12px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .btn-reset:active {{
      color: var(--text-main);
      border-color: var(--text-muted);
    }}

    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 14px;
      margin-bottom: 14px;
    }}

    .segmented-control {{
      display: flex;
      background: #0f1724;
      padding: 3px;
      border-radius: 10px;
      margin-bottom: 12px;
    }}

    .segmented-btn {{
      flex: 1;
      padding: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      text-align: center;
      background: transparent;
      border: none;
      color: var(--text-muted);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .segmented-btn.active {{
      background: var(--accent);
      color: #fff;
    }}

    .search-input-wrap {{
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: #0f1724;
      border: 1px solid var(--chip-border);
      color: var(--text-main);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent);
    }}

    /* Active Filters summary section */
    .active-filters-wrap {{
      display: none;
      margin-bottom: 14px;
    }}

    .active-filters-wrap.has-items {{
      display: block;
    }}

    .active-filters-title {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }}

    .active-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .active-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 20px;
      cursor: pointer;
    }}

    .active-chip.include {{
      background: var(--include-bg);
      border: 1px solid var(--include);
      color: #79f7ab;
    }}

    .active-chip.exclude {{
      background: var(--exclude-bg);
      border: 1px solid var(--exclude);
      color: #ff869a;
    }}

    .active-chip .remove {{
      font-size: 0.95rem;
      line-height: 1;
      opacity: 0.7;
    }}

    /* Tag Section */
    .section-title {{
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--text-muted);
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .tag-search-box {{
      margin-bottom: 10px;
    }}

    .category-pills {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 10px;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }}

    .category-pills::-webkit-scrollbar {{
      display: none;
    }}

    .cat-pill {{
      white-space: nowrap;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: 14px;
      background: #0f1724;
      border: 1px solid var(--chip-border);
      color: var(--text-muted);
      cursor: pointer;
    }}

    .cat-pill.active {{
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }}

    .tags-container {{
      max-height: 260px;
      overflow-y: auto;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding-right: 4px;
      -webkit-overflow-scrolling: touch;
    }}

    .tag-chip {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 6px 11px;
      font-size: 0.8rem;
      font-weight: 500;
      background: var(--chip-bg);
      border: 1px solid var(--chip-border);
      border-radius: 8px;
      color: var(--text-main);
      cursor: pointer;
      user-select: none;
      transition: all 0.15s ease;
    }}

    .tag-chip:active {{
      transform: scale(0.97);
    }}

    .tag-chip.include {{
      background: var(--include-bg);
      border-color: var(--include);
      color: #79f7ab;
      font-weight: 600;
    }}

    .tag-chip.exclude {{
      background: var(--exclude-bg);
      border-color: var(--exclude);
      color: #ff869a;
      font-weight: 600;
    }}

    .tag-chip .badge-type {{
      font-size: 0.65rem;
      opacity: 0.5;
      text-transform: uppercase;
      margin-left: 2px;
    }}

    .hint-legend {{
      display: flex;
      gap: 12px;
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 10px;
    }}

    .hint-legend span {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    .dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}
    .dot.green {{ background: var(--include); }}
    .dot.red {{ background: var(--exclude); }}
    .dot.gray {{ background: var(--text-muted); }}

    /* Slider styling */
    .slider-wrap {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 4px;
    }}

    .slider-header {{
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      color: var(--text-main);
    }}

    .slider-val {{
      color: var(--accent);
      font-weight: 700;
    }}

    input[type=range] {{
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      background: #0f1724;
      border-radius: 4px;
      outline: none;
    }}

    input[type=range]::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--accent);
      cursor: pointer;
      box-shadow: 0 0 8px rgba(61, 180, 242, 0.4);
    }}

    /* Accordion / Secondary Filters */
    details {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      margin-bottom: 14px;
      overflow: hidden;
    }}

    details summary {{
      padding: 14px;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-main);
      cursor: pointer;
      user-select: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    details[open] summary {{
      border-bottom: 1px solid var(--card-border);
    }}

    .filter-grid {{
      padding: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    .filter-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .filter-group.full {{
      grid-column: span 2;
    }}

    .filter-group label {{
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    select, input.sub-input {{
      background: #0f1724;
      border: 1px solid var(--chip-border);
      color: var(--text-main);
      padding: 9px 10px;
      border-radius: 8px;
      font-size: 0.85rem;
      outline: none;
      width: 100%;
    }}

    select:focus, input.sub-input:focus {{
      border-color: var(--accent);
    }}

    /* Floating Sticky Action Footer */
    .sticky-footer {{
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(11, 22, 34, 0.94);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-top: 1px solid var(--card-border);
      padding: 12px 16px calc(var(--safe-bottom) + 8px) 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 100;
    }}

    .action-row {{
      display: flex;
      gap: 8px;
    }}

    .btn-search {{
      flex: 3;
      background: var(--accent);
      color: #fff;
      font-size: 1rem;
      font-weight: 700;
      border: none;
      border-radius: 12px;
      padding: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(61, 180, 242, 0.35);
      transition: all 0.2s;
    }}

    .btn-search:active {{
      transform: scale(0.98);
      background: var(--accent-hover);
    }}

    .btn-copy {{
      flex: 1;
      background: #1a2738;
      border: 1px solid var(--chip-border);
      color: var(--text-main);
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: 12px;
      padding: 14px 10px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .btn-copy:active {{
      background: #25364e;
    }}

    .url-preview {{
      font-family: monospace;
      font-size: 0.72rem;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-align: center;
    }}

    /* Toast */
    .toast {{
      position: fixed;
      top: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(-100px);
      background: #26a65b;
      color: white;
      padding: 8px 18px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: transform 0.3s ease;
      z-index: 999;
      pointer-events: none;
    }}

    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <svg viewBox="0 0 100 100">
        <path d="M50 8 L92 90 L8 90 Z" fill="none" stroke="#3db4f2" stroke-width="12" stroke-linejoin="round"/>
        <circle cx="50" cy="58" r="14" fill="#3db4f2"/>
      </svg>
      <h1>AniList <span>Search</span></h1>
    </div>
    <button class="btn-reset" onclick="resetAllFilters()">Reset All</button>
  </header>

  <!-- Media Type & Title -->
  <div class="card">
    <div class="segmented-control">
      <button class="segmented-btn active" id="btn-anime" onclick="setMediaType('anime')">Anime</button>
      <button class="segmented-btn" id="btn-manga" onclick="setMediaType('manga')">Manga</button>
    </div>
    <div class="search-input-wrap">
      <input type="text" id="title-search" class="search-input" placeholder="Title keywords (optional)..." oninput="updateUrl()">
    </div>
  </div>

  <!-- Active Filters Pills -->
  <div class="active-filters-wrap" id="active-filters-wrap">
    <div class="active-filters-title">
      <span>Active Filters (<span id="active-count">0</span>)</span>
      <span style="font-size: 0.75rem; text-decoration: underline; cursor: pointer;" onclick="clearTagFilters()">Clear tags</span>
    </div>
    <div class="active-chips" id="active-chips"></div>
  </div>

  <!-- Tags & Genres Card -->
  <div class="card">
    <div class="section-title">
      <span>Genres & Tags</span>
      <span id="tag-matches-count" style="font-size: 0.75rem; font-weight: normal; color: var(--text-muted);"></span>
    </div>

    <div class="tag-search-box">
      <input type="text" id="tag-filter-input" class="search-input" placeholder="Filter tags (e.g. Cyberpunk, Isekai)..." oninput="renderTags()">
    </div>

    <!-- Category selector -->
    <div class="category-pills" id="category-pills"></div>

    <!-- Tags grid -->
    <div class="tags-container" id="tags-container"></div>

    <div class="hint-legend">
      <span><span class="dot green"></span> Tap 1: Include</span>
      <span><span class="dot red"></span> Tap 2: Exclude</span>
      <span><span class="dot gray"></span> Tap 3: Clear</span>
    </div>
  </div>

  <!-- Tag Rank Slider Card -->
  <div class="card">
    <div class="slider-wrap">
      <div class="slider-header">
        <span>Minimum Tag Rank (Confidence)</span>
        <span class="slider-val" id="rank-display">18%</span>
      </div>
      <input type="range" id="rank-slider" min="0" max="100" value="18" oninput="onRankChange(this.value)">
      <div style="font-size: 0.7rem; color: var(--text-muted); display: flex; justify-content: space-between;">
        <span>0% (Any match)</span>
        <span>Default: 18%</span>
        <span>100% (Strict)</span>
      </div>
    </div>
  </div>

  <!-- Additional Filters Dropdown -->
  <details id="advanced-details">
    <summary>
      <span>Additional Filters (Format, Sort, Season)</span>
      <span style="font-size: 0.75rem; color: var(--accent);">Expand ▼</span>
    </summary>
    <div class="filter-grid">
      <div class="filter-group">
        <label>Sort By</label>
        <select id="sort-select" onchange="updateUrl()">
          <option value="POPULARITY_DESC">Popularity</option>
          <option value="SCORE_DESC">Average Score</option>
          <option value="TRENDING_DESC">Trending</option>
          <option value="FAVOURITES_DESC">Favorites</option>
          <option value="START_DATE_DESC">Release Date</option>
          <option value="TITLE_ROMAJI">Title</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Format</label>
        <select id="format-select" onchange="updateUrl()">
          <option value="">Any Format</option>
          <option value="TV">TV Show</option>
          <option value="MOVIE">Movie</option>
          <option value="OVA">OVA</option>
          <option value="ONA">ONA</option>
          <option value="SPECIAL">Special</option>
          <option value="TV_SHORT">TV Short</option>
          <option value="MUSIC">Music</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Season</label>
        <select id="season-select" onchange="updateUrl()">
          <option value="">Any Season</option>
          <option value="WINTER">Winter</option>
          <option value="SPRING">Spring</option>
          <option value="SUMMER">Summer</option>
          <option value="FALL">Fall</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Year</label>
        <input type="number" id="year-input" class="sub-input" placeholder="e.g. 2024" min="1940" max="2035" oninput="updateUrl()">
      </div>

      <div class="filter-group">
        <label>Status</label>
        <select id="status-select" onchange="updateUrl()">
          <option value="">Any Status</option>
          <option value="FINISHED">Finished</option>
          <option value="RELEASING">Releasing / Airing</option>
          <option value="NOT_YET_RELEASED">Not Yet Released</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Country of Origin</label>
        <select id="country-select" onchange="updateUrl()">
          <option value="">All Countries</option>
          <option value="JP">Japan (JP)</option>
          <option value="KR">South Korea (KR)</option>
          <option value="CN">China (CN)</option>
          <option value="TW">Taiwan (TW)</option>
        </select>
      </div>
    </div>
  </details>

  <!-- Sticky Mobile Action Footer -->
  <div class="sticky-footer">
    <div class="action-row">
      <button class="btn-search" onclick="openAniList()">
        <span>Open in AniList</span>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
          <polyline points="15 3 21 3 21 9"></polyline>
          <line x1="10" y1="14" x2="21" y2="3"></line>
        </svg>
      </button>
      <button class="btn-copy" onclick="copyUrl()">Copy URL</button>
    </div>
    <div class="url-preview" id="url-preview">https://anilist.co/search/anime</div>
  </div>

  <div class="toast" id="toast">Copied to clipboard!</div>

  <script>
    // Embedded Data Seed
    const RAW_GENRES = {genres_json};
    const RAW_TAGS = {tags_json};

    // Application State
    let mediaType = "anime";
    let selectedCategory = "ALL";
    let tagStates = {{}}; // {{ [tagName]: 'include' | 'exclude' }}
    let allItems = [];

    function initData() {{
      const genresList = RAW_GENRES.map(g => ({{ name: g, category: "Genre", isGenre: true }}));
      const tagsList = RAW_TAGS.map(t => ({{ name: t.name, category: t.category || "Theme", isGenre: false }}));
      allItems = [...genresList, ...tagsList];
      fetchAniListTags();
    }}

    async function fetchAniListTags() {{
      try {{
        const res = await fetch("https://graphql.anilist.co", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json", "Accept": "application/json" }},
          body: JSON.stringify({{ query: "query {{ GenreCollection MediaTagCollection {{ name category isAdult }} }}" }})
        }});
        if (res.ok) {{
          const json = await res.json();
          if (json.data && json.data.GenreCollection && json.data.MediaTagCollection) {{
            const freshGenres = json.data.GenreCollection.map(g => ({{ name: g, category: "Genre", isGenre: true }}));
            const freshTags = json.data.MediaTagCollection.map(t => ({{ name: t.name, category: t.category || "Theme", isGenre: false }}));
            allItems = [...freshGenres, ...freshTags];
            renderCategories();
            renderTags();
          }}
        }}
      }} catch (e) {{}}
    }}

    function setMediaType(type) {{
      mediaType = type;
      document.getElementById("btn-anime").classList.toggle("active", type === "anime");
      document.getElementById("btn-manga").classList.toggle("active", type === "manga");

      const formatSelect = document.getElementById("format-select");
      if (type === "manga") {{
        formatSelect.innerHTML = `
          <option value="">Any Format</option>
          <option value="MANGA">Manga</option>
          <option value="NOVEL">Light Novel</option>
          <option value="ONE_SHOT">One Shot</option>
        `;
      }} else {{
        formatSelect.innerHTML = `
          <option value="">Any Format</option>
          <option value="TV">TV Show</option>
          <option value="MOVIE">Movie</option>
          <option value="OVA">OVA</option>
          <option value="ONA">ONA</option>
          <option value="SPECIAL">Special</option>
          <option value="TV_SHORT">TV Short</option>
          <option value="MUSIC">Music</option>
        `;
      }}
      updateUrl();
    }}

    function renderCategories() {{
      const container = document.getElementById("category-pills");
      const cats = new Set(["ALL", "Genre"]);
      allItems.forEach(i => {{
        if (i.category && i.category !== "Genre") {{
          const catName = i.category.split("-")[0];
          cats.add(catName);
        }}
      }});

      container.innerHTML = "";
      cats.forEach(cat => {{
        const btn = document.createElement("button");
        btn.className = "cat-pill" + (cat === selectedCategory ? " active" : "");
        btn.textContent = cat;
        btn.onclick = () => {{
          selectedCategory = cat;
          document.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
          btn.classList.add("active");
          renderTags();
        }};
        container.appendChild(btn);
      }});
    }}

    function renderTags() {{
      const container = document.getElementById("tags-container");
      const query = document.getElementById("tag-filter-input").value.trim().toLowerCase();

      let filtered = allItems.filter(item => {{
        const matchesQuery = !query || item.name.toLowerCase().includes(query);
        let matchesCat = true;
        if (selectedCategory !== "ALL") {{
          if (selectedCategory === "Genre") {{
            matchesCat = item.isGenre;
          }} else {{
            matchesCat = item.category && item.category.startsWith(selectedCategory);
          }}
        }}
        return matchesQuery && matchesCat;
      }});

      document.getElementById("tag-matches-count").textContent = `${{filtered.length}} found`;

      container.innerHTML = "";
      filtered.forEach(item => {{
        const state = tagStates[item.name];
        const chip = document.createElement("div");
        chip.className = "tag-chip" + (state ? " " + state : "");

        let prefix = "";
        if (state === "include") prefix = "+ ";
        if (state === "exclude") prefix = "- ";

        chip.innerHTML = `${{prefix}}${{item.name}} <span class="badge-type">${{item.isGenre ? "GENRE" : ""}}</span>`;
        chip.onclick = () => toggleTag(item.name);
        container.appendChild(chip);
      }});

      renderActiveChips();
    }}

    function toggleTag(name) {{
      const current = tagStates[name];
      if (!current) {{
        tagStates[name] = "include";
      }} else if (current === "include") {{
        tagStates[name] = "exclude";
      }} else {{
        delete tagStates[name];
      }}
      renderTags();
      updateUrl();
    }}

    function removeTag(name) {{
      delete tagStates[name];
      renderTags();
      updateUrl();
    }}

    function renderActiveChips() {{
      const wrap = document.getElementById("active-filters-wrap");
      const container = document.getElementById("active-chips");
      const keys = Object.keys(tagStates);

      document.getElementById("active-count").textContent = keys.length;

      if (keys.length === 0) {{
        wrap.classList.remove("has-items");
        return;
      }}

      wrap.classList.add("has-items");
      container.innerHTML = "";

      keys.forEach(name => {{
        const state = tagStates[name];
        const chip = document.createElement("div");
        chip.className = `active-chip ${{state}}`;
        chip.innerHTML = `${{state === "include" ? "+" : "-"}} ${{name}} <span class="remove">✕</span>`;
        chip.onclick = () => removeTag(name);
        container.appendChild(chip);
      }});
    }}

    function clearTagFilters() {{
      tagStates = {{}};
      renderTags();
      updateUrl();
    }}

    function onRankChange(val) {{
      document.getElementById("rank-display").textContent = val + "%";
      updateUrl();
    }}

    function buildUrl() {{
      const baseUrl = `https://anilist.co/search/${{mediaType}}`;
      const params = new URLSearchParams();

      const keyword = document.getElementById("title-search").value.trim();
      if (keyword) params.append("search", keyword);

      const includes = Object.entries(tagStates).filter(([_, s]) => s === "include").map(([n]) => n);
      includes.forEach(tag => params.append("genres", tag));

      const excludes = Object.entries(tagStates).filter(([_, s]) => s === "exclude").map(([n]) => n);
      excludes.forEach(tag => params.append("excludeGenres", tag));

      const rank = document.getElementById("rank-slider").value;
      if (rank !== "18") {{
        params.append("minimumTagRank", rank);
      }}

      const sort = document.getElementById("sort-select").value;
      if (sort && sort !== "POPULARITY_DESC") {{
        params.append("sort", sort);
      }}

      const format = document.getElementById("format-select").value;
      if (format) params.append("format", format);

      const season = document.getElementById("season-select").value;
      if (season && mediaType === "anime") params.append("season", season);

      const year = document.getElementById("year-input").value.trim();
      if (year) params.append("year", year);

      const status = document.getElementById("status-select").value;
      if (status) params.append("status", status);

      const country = document.getElementById("country-select").value;
      if (country) params.append("countryOfOrigin", country);

      const qs = params.toString();
      return qs ? `${{baseUrl}}?${{qs}}` : baseUrl;
    }}

    function updateUrl() {{
      const url = buildUrl();
      document.getElementById("url-preview").textContent = url;
    }}

    function openAniList() {{
      const url = buildUrl();
      window.open(url, "_blank");
    }}

    function copyUrl() {{
      const url = buildUrl();
      navigator.clipboard.writeText(url).then(() => {{
        showToast();
      }}).catch(() => {{
        prompt("Copy this URL:", url);
      }});
    }}

    function showToast() {{
      const toast = document.getElementById("toast");
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 2000);
    }}

    function resetAllFilters() {{
      tagStates = {{}};
      document.getElementById("title-search").value = "";
      document.getElementById("tag-filter-input").value = "";
      document.getElementById("rank-slider").value = "18";
      document.getElementById("rank-display").textContent = "18%";
      document.getElementById("sort-select").value = "POPULARITY_DESC";
      document.getElementById("format-select").value = "";
      document.getElementById("season-select").value = "";
      document.getElementById("year-input").value = "";
      document.getElementById("status-select").value = "";
      document.getElementById("country-select").value = "";
      selectedCategory = "ALL";
      renderCategories();
      renderTags();
      updateUrl();
    }}

    window.onload = () => {{
      initData();
      renderCategories();
      renderTags();
      updateUrl();
    }};
  </script>
</body>
</html>
"""

output_path = "/Users/julianmilke/anilist-filter-app/index.html"
with open(output_path, "w") as f:
    f.write(html_content)

print(f"Generated {output_path} successfully!")
