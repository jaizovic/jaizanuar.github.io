# Structured article publishing

`articles.json` is the canonical source for article content, metadata and its featured-image contract. Generated HTML under `articles/` and the article array in `assets/dashboard.js` must not be edited by hand.

Each article image contract contains:

- `visual_concept`: the article-specific scene the image must communicate.
- `relevance_terms`: concepts that ground the image contract in the article.
- `alt`: the accessible description used on the article and listing pages.
- `status`: publication is allowed only when this is `approved`.
- `width` and `height`: fixed at 1600 × 900.

## Local commands

Install the publishing dependency:

```sh
python3 -m pip install -r requirements-publishing.txt
```

Build and validate without generating images:

```sh
python3 tools/article_pipeline.py build
python3 tools/article_pipeline.py validate
```

Generate images that are missing, then build and validate everything:

```sh
OPENAI_API_KEY=... python3 tools/article_pipeline.py publish
```

Generation uses the article title, lead, main headings, visual concept and relevance terms. Approval fails closed unless the image is a valid WebP, exactly 1600 × 900, under the file-size limit, mapped to a grounded content contract and referenced by every generated publication surface.

## GitHub automation

Add `OPENAI_API_KEY` as a GitHub Actions repository secret. A change to `content/articles.json` on `main` then generates any missing image, marks it approved, rebuilds the pages and commits the publication artifacts. Pull requests run the same build and mandatory validation without spending image-generation credits.
