#!/usr/bin/env python3
"""Generate, render and validate the structured article publication."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "articles.json"
SITE_URL = "https://jaizanuar.com"
IMAGE_MODEL = "gpt-image-2-2026-04-21"
IMAGE_SIZE = (1600, 900)
MAX_IMAGE_BYTES = 550_000


def load_content() -> dict:
    return json.loads(CONTENT.read_text(encoding="utf-8"))


def save_content(data: dict) -> None:
    CONTENT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def image_prompt(article: dict) -> str:
    image = article["image"]
    headings = re.findall(r"<h2[^>]*>(.*?)</h2>", article["body_html"], flags=re.I | re.S)
    headings = [re.sub(r"<[^>]+>", "", value).strip() for value in headings[:4]]
    return "\n".join(
        [
            "Use case: stylized-concept",
            "Asset type: 16:9 editorial hero for an independent cybersecurity publication",
            f"Article title: {article['title']}",
            f"Article argument: {article['lead']}",
            f"Primary visual concept: {image['visual_concept']}",
            f"Required content-relevance concepts: {', '.join(image['relevance_terms'])}",
            f"Key sections: {'; '.join(headings)}",
            "Style/medium: premium editorial technology illustration with realistic depth, conceptually precise rather than generic stock imagery",
            "Composition/framing: wide landscape, one coherent scene, clear focal point, edge-safe for responsive cropping",
            "Lighting/mood: thoughtful, intelligent, controlled",
            "Color palette: deep navy, cobalt blue, restrained cyan highlights, minimal amber risk accents",
            "Constraints: professional publication quality; no embedded words, letters, numbers, logos, watermark, hooded hacker, floating padlock, generic shield, or illegible interface text",
        ]
    )


def ensure_image_contract(article: dict) -> bool:
    if article.get("image"):
        return False
    meaningful = [word for word in re.findall(r"[A-Za-z][A-Za-z-]{4,}", article["title"]) if word.lower() not in {"about", "become", "because", "every", "isn’t", "their", "there", "these", "those"}]
    terms = list(dict.fromkeys(article.get("categories", []) + meaningful[:3]))[:4]
    concept = f"An editorial visual expressing the central argument of “{article['title']}”: {article['lead']}"
    article["image"] = {
        "path": f"assets/images/articles/{article['slug']}.webp",
        "alt": concept,
        "visual_concept": concept,
        "relevance_terms": terms,
        "status": "pending",
        "width": IMAGE_SIZE[0],
        "height": IMAGE_SIZE[1],
    }
    return True


def openai_image(prompt: str) -> bytes:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required to generate a missing article image")
    payload = json.dumps(
        {
            "model": IMAGE_MODEL,
            "prompt": prompt,
            "size": "2048x1152",
            "quality": "medium",
            "output_format": "webp",
            "output_compression": 88,
        }
    ).encode()
    request = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Image generation failed ({error.code}): {detail}") from error
    return base64.b64decode(result["data"][0]["b64_json"])


def save_webp(source: bytes | Path, destination: Path) -> None:
    if isinstance(source, Path):
        image = Image.open(source)
    else:
        image = Image.open(io.BytesIO(source))
    with image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image = ImageOps.fit(image, IMAGE_SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, "WEBP", quality=84, method=6)


def normalise_existing(data: dict) -> None:
    converted = 0
    for article in data["articles"]:
        destination = ROOT / article["image"]["path"]
        source = destination.with_suffix(".png")
        if source.exists():
            save_webp(source, destination)
            converted += 1
    print(f"Normalised {converted} article images to {IMAGE_SIZE[0]}x{IMAGE_SIZE[1]} WebP")


def generate_missing(data: dict) -> None:
    changed = False
    generated = 0
    for article in data["articles"]:
        changed |= ensure_image_contract(article)
        image = article["image"]
        destination = ROOT / image["path"]
        if destination.exists() and image.get("status") == "approved":
            continue
        image["status"] = "generating"
        save_content(data)
        raw = openai_image(image_prompt(article))
        save_webp(raw, destination)
        approve_image(article, destination)
        image["generated_at"] = datetime.now(timezone.utc).isoformat()
        image["model"] = IMAGE_MODEL
        image["prompt_sha256"] = hashlib.sha256(image_prompt(article).encode()).hexdigest()
        image["status"] = "approved"
        save_content(data)
        generated += 1
        changed = True
        print(f"Generated and approved {article['slug']}")
    if changed:
        save_content(data)
    print(f"Generated {generated} missing article images")


def approve_image(article: dict, path: Path) -> None:
    with Image.open(path) as image:
        if image.size != IMAGE_SIZE:
            raise ValueError(f"{article['slug']}: expected {IMAGE_SIZE}, found {image.size}")
        if image.format != "WEBP":
            raise ValueError(f"{article['slug']}: publication image must be WebP")
        image.verify()
    if path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError(f"{article['slug']}: image exceeds {MAX_IMAGE_BYTES // 1000} KB")
    contract = " ".join(
        [article["title"], article["lead"], article["body_html"], article["image"]["alt"], article["image"]["visual_concept"]]
    ).casefold()
    missing = []
    for term in article["image"]["relevance_terms"]:
        tokens = [token.casefold() for token in re.findall(r"[A-Za-z][A-Za-z-]{3,}", term)]
        if not tokens or not any(token in contract for token in tokens):
            missing.append(term)
    if missing:
        raise ValueError(f"{article['slug']}: relevance terms are not grounded in the article contract: {missing}")


def meta_line(article: dict) -> str:
    return " · ".join([article["display_date"], *article["categories"], article["reading_time"]])


def article_page(article: dict) -> str:
    title = escape(article["title"])
    description = escape(article["description"], quote=True)
    lead = escape(article["lead"])
    image = article["image"]
    image_rel = f"../{image['path']}"
    image_abs = f"{SITE_URL}/{image['path']}"
    page_url = f"{SITE_URL}/articles/{article['slug']}.html"
    structured = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["description"],
        "datePublished": article["date"],
        "dateModified": article["date"],
        "author": {"@type": "Person", "name": "Jaiz Anuar", "url": SITE_URL},
        "image": {"@type": "ImageObject", "url": image_abs, "width": image["width"], "height": image["height"]},
        "mainEntityOfPage": page_url,
    }
    structured_json = json.dumps(structured, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Jaiz Anuar</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{page_url}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{image_abs}" />
  <meta property="og:image:width" content="{image['width']}" />
  <meta property="og:image:height" content="{image['height']}" />
  <meta property="og:image:alt" content="{escape(image['alt'], quote=True)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{image_abs}" />
  <script type="application/ld+json">{structured_json}</script>
  <link rel="stylesheet" href="../assets/style.css" />
</head>
<body class="light-page">
  <header class="page-header">
    <div class="logo">Jaiz Anuar</div>
    <nav>
      <a href="../index.html">Home</a>
      <a href="index.html">Articles</a>
      <a href="../about/">About</a>
      <a href="../dashboard/">Dashboard</a>
    </nav>
  </header>

  <main class="reader">
    <a href="index.html" class="back-link">← Back to Articles</a>
    <div class="article-meta">{escape(meta_line(article))}</div>
    <a class="download-button article-download" href="../{escape(article['pdf'], quote=True)}" download>Download PDF</a>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    <figure class="article-featured-image">
      <img src="{image_rel}" width="{image['width']}" height="{image['height']}" alt="{escape(image['alt'], quote=True)}" fetchpriority="high" decoding="async" />
    </figure>

{article['body_html']}
  </main>

  <footer>© 2026 Jaiz Anuar. Independent perspectives on cybersecurity and digital trust.</footer>
  <script data-goatcounter="https://jaizanuar.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
'''


INDEX_SCRIPT = r'''<script>
const pageSize = 12;
const list = document.getElementById('articleList');
const cards = [...list.querySelectorAll('.article-card')].sort((a, b) => b.dataset.date.localeCompare(a.dataset.date));
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const yearFilter = document.getElementById('yearFilter');
const pagination = document.getElementById('pagination');
const summary = document.getElementById('resultsSummary');

function populateFilters() {
  const categories = [...new Set(cards.flatMap(card => card.dataset.categories.split(',')))].sort();
  const years = [...new Set(cards.map(card => card.dataset.date.slice(0, 4)))].sort().reverse();
  categories.forEach(category => categoryFilter.add(new Option(category, category)));
  years.forEach(year => yearFilter.add(new Option(year, year)));
}

function pageLink(page, label, current) {
  const link = document.createElement(current ? 'span' : 'a');
  link.textContent = label;
  link.className = current ? 'current-page' : '';
  if (!current) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    link.href = url.pathname + url.search;
    link.addEventListener('click', event => { event.preventDefault(); render(page); });
  }
  return link;
}

function render(requestedPage = 1) {
  const search = searchInput.value.toLowerCase().trim();
  const category = categoryFilter.value;
  const year = yearFilter.value;
  const matching = cards.filter(card => card.textContent.toLowerCase().includes(search) && (!category || card.dataset.categories.split(',').includes(category)) && (!year || card.dataset.date.startsWith(year)));
  const totalPages = Math.max(1, Math.ceil(matching.length / pageSize));
  const page = Math.min(Math.max(1, requestedPage), totalPages);
  const start = (page - 1) * pageSize;
  list.replaceChildren(...matching.slice(start, start + pageSize));
  summary.textContent = matching.length ? `Showing ${start + 1}-${Math.min(start + pageSize, matching.length)} of ${matching.length} articles` : 'No articles match your search.';
  pagination.replaceChildren();
  if (totalPages > 1) {
    if (page > 1) pagination.append(pageLink(page - 1, 'Previous', false));
    for (let number = 1; number <= totalPages; number++) pagination.append(pageLink(number, number, number === page));
    if (page < totalPages) pagination.append(pageLink(page + 1, 'Next', false));
  }
  const url = new URL(window.location);
  if (page === 1) url.searchParams.delete('page'); else url.searchParams.set('page', page);
  window.history.replaceState({}, '', url.pathname + url.search);
}

populateFilters();
searchInput.addEventListener('input', () => render(1));
categoryFilter.addEventListener('change', () => render(1));
yearFilter.addEventListener('change', () => render(1));
render(Number(new URLSearchParams(window.location.search).get('page')) || 1);
</script>'''


def index_page(articles: list[dict]) -> str:
    cards = []
    for article in articles:
        image = article["image"]
        cards.append(f'''    <article class="article-card" data-date="{article['date']}" data-categories="{escape(','.join(article['categories']), quote=True)}">
      <a class="article-card-image" href="{article['slug']}.html" aria-label="Read {escape(article['title'], quote=True)}"><img src="../{image['path']}" width="{image['width']}" height="{image['height']}" alt="{escape(image['alt'], quote=True)}" loading="lazy" decoding="async" /></a>
      <div class="article-meta">{escape(meta_line(article))}</div>
      <h2><a href="{article['slug']}.html">{escape(article['title'])}</a></h2>
      <p>{escape(article['excerpt'])}</p>
      <div class="article-actions"><a class="read-more" href="{article['slug']}.html">Read article →</a><a class="download-button article-download" href="../{escape(article['pdf'], quote=True)}" download>Download PDF</a></div>
    </article>''')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Articles | Jaiz Anuar</title>
  <meta name="description" content="Independent reflections on cybersecurity, digital trust, governance, architecture, and leadership." />
  <link rel="canonical" href="{SITE_URL}/articles/" />
  <link rel="stylesheet" href="../assets/style.css" />
</head>
<body class="light-page">
<header class="page-header"><div class="logo">Jaiz Anuar</div><nav><a href="../index.html">Home</a><a href="index.html">Articles</a><a href="../about/">About</a><a href="../dashboard/">Dashboard</a></nav></header>
<section class="article-hero"><h1>Articles</h1><p>Independent reflections on cybersecurity, digital trust, governance, architecture, and leadership.</p><div class="article-filters" aria-label="Filter articles"><input type="search" id="searchInput" placeholder="Search articles..." aria-label="Search articles" /><select id="categoryFilter" aria-label="Filter by category"><option value="">All topics</option></select><select id="yearFilter" aria-label="Filter by year"><option value="">All years</option></select></div></section>
<main class="article-list"><p class="results-summary" id="resultsSummary" aria-live="polite"></p><section id="articleList">
{chr(10).join(cards)}
  </section><nav class="pagination" id="pagination" aria-label="Article pages"></nav></main>
<footer>© 2026 Jaiz Anuar. Independent perspectives on cybersecurity and digital trust.</footer>
{INDEX_SCRIPT}
<script data-goatcounter="https://jaizanuar.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
'''


def update_dashboard(articles: list[dict]) -> None:
    path = ROOT / "assets" / "dashboard.js"
    source = path.read_text(encoding="utf-8")
    rows = [f"    [{json.dumps(a['title'], ensure_ascii=False)}, {json.dumps(a['date'])}, {json.dumps('/articles/' + a['slug'] + '.html')}]" for a in articles]
    replacement = "var articles = [\n" + ",\n".join(rows) + "\n  ];"
    updated, count = re.subn(r"var articles = \[.*?\n  \];", replacement, source, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not locate dashboard article array")
    path.write_text(updated, encoding="utf-8")


def build(data: dict) -> None:
    articles = sorted(data["articles"], key=lambda item: (item["date"], item["slug"]), reverse=True)
    for article in articles:
        (ROOT / "articles" / f"{article['slug']}.html").write_text(article_page(article), encoding="utf-8")
    (ROOT / "articles" / "index.html").write_text(index_page(articles), encoding="utf-8")
    update_dashboard(articles)
    print(f"Built {len(articles)} article pages, listing and dashboard index")


def validate(data: dict) -> None:
    errors = []
    articles = data.get("articles", [])
    slugs = [article.get("slug") for article in articles]
    if len(slugs) != len(set(slugs)):
        errors.append("article slugs must be unique")
    required = ["slug", "title", "description", "lead", "date", "display_date", "categories", "reading_time", "excerpt", "body_html", "image"]
    for article in articles:
        slug = article.get("slug", "<unknown>")
        missing = [field for field in required if not article.get(field)]
        if missing:
            errors.append(f"{slug}: missing required fields {missing}")
            continue
        image = article["image"]
        if image.get("status") != "approved":
            errors.append(f"{slug}: image status is not approved")
        image_path = ROOT / image.get("path", "")
        if not image_path.is_file():
            errors.append(f"{slug}: image file is missing")
        else:
            try:
                approve_image(article, image_path)
            except Exception as error:
                errors.append(str(error))
        page = ROOT / "articles" / f"{slug}.html"
        if not page.is_file():
            errors.append(f"{slug}: generated article page is missing")
        else:
            page_text = page.read_text(encoding="utf-8")
            for marker in [f'../{image["path"]}', 'property="og:image"', 'name="twitter:image"', 'application/ld+json']:
                if marker not in page_text:
                    errors.append(f"{slug}: generated page is missing {marker}")
    index = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
    if index.count('class="article-card"') != len(articles):
        errors.append("article listing card count does not match structured content")
    if errors:
        print("Publication validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Publication validation passed: {len(articles)} articles, each with an approved 1600x900 image")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["normalise-images", "generate-missing", "build", "validate", "publish"])
    args = parser.parse_args()
    data = load_content()
    if args.command == "normalise-images":
        normalise_existing(data)
    elif args.command == "generate-missing":
        generate_missing(data)
    elif args.command == "build":
        build(data)
    elif args.command == "validate":
        validate(data)
    elif args.command == "publish":
        generate_missing(data)
        build(data)
        validate(data)


if __name__ == "__main__":
    main()
