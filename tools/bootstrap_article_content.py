#!/usr/bin/env python3
"""One-time migration of the hand-authored article HTML into structured JSON."""

from __future__ import annotations

import json
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "articles"
OUTPUT = ROOT / "content" / "articles.json"


VISUALS = {
    "attackers-are-becoming-ai-native-deception-must-become-ai-native-too": (
        "An AI-native attacker being diverted into adaptive decoy identities and synthetic systems while defenders observe trust-violation signals.",
        ["AI-native attackers", "adaptive deception", "decoy identities", "trust violation"],
    ),
    "behind-every-line-of-code-human-element-cybersecurity": (
        "A diverse engineering team collectively shaping security controls, code and architecture, emphasising the people behind cyber resilience.",
        ["human element", "engineering team", "security controls", "cyber resilience"],
    ),
    "convenience-is-an-attack-surface": (
        "Nearby personal devices sharing data seamlessly while an untrusted path exposes the risk created by verification happening too late.",
        ["device sharing", "convenience", "late verification", "untrusted receiver"],
    ),
    "cybersecurity-best-practice-baseline-not-blueprint": (
        "A shared security baseline supporting several contextual architectural paths that reach the same protected outcome through different controls.",
        ["security baseline", "contextual architecture", "different controls", "protected outcome"],
    ),
    "cybersecurity-doesnt-fail-because-we-dont-know-enough": (
        "A confident decision-maker following one bright path while important cyber risks remain hidden in adjacent blind spots.",
        ["cybersecurity confidence", "blind spots", "hidden risk", "curiosity"],
    ),
    "cybersecurity-industry-profits": (
        "An independent security leader evaluating outcomes as a marketplace of security products grows around a continuing stream of threats.",
        ["security industry", "incentives", "vendor dependency", "independent judgement"],
    ),
    "enable-business-safely-not-block-business-safely": (
        "A business team advancing across a carefully engineered secure bridge while security architects strengthen the route instead of blocking it.",
        ["business enablement", "secure bridge", "security architects", "guardrails"],
    ),
    "employees-are-adopting-ai-faster-than-organisations-can-govern-it": (
        "Employees adopting AI across fast-moving workflows while identity, data and policy guardrails form a visible governance path around them.",
        ["employee AI adoption", "governance visibility", "data protection", "identity governance"],
    ),
    "most-architecture-diagrams-show-connectivity-few-show-trust-and-controls": (
        "A layered system architecture where every connection crosses visible trust boundaries and passes through explicit controls.",
        ["security architecture", "connectivity", "trust boundaries", "controls"],
    ),
    "not-all-personal-data-can-be-anonymised": (
        "Personal data moving through governed stages where identity is selectively minimised and retained only inside controlled boundaries.",
        ["personal data", "anonymisation", "data governance", "controlled identity"],
    ),
    "real-data-breach-vs-honeypot-data-breach": (
        "An intruder extracting a convincing decoy dataset that leads into a monitored honeypot while defenders learn from the false prize.",
        ["data breach", "honeypot", "decoy data", "threat intelligence"],
    ),
    "the-biggest-ai-deployment-in-your-organisation-may-already-be-happening-without-you": (
        "Employees using AI throughout everyday workflows beyond a central governance boundary, forming an expanding shadow-AI constellation.",
        ["shadow AI", "employees", "AI adoption", "governance visibility"],
    ),
    "the-most-dangerous-incidents-start-as-normal-days": (
        "A calm operations team doing routine work while small ignored deviations align into a hidden cascading failure.",
        ["normal operations", "ignored deviations", "cascading failure", "operational resilience"],
    ),
    "the-new-security-perimeter-is-no-longer-the-network-it-is-identity": (
        "Human, machine, service and workload identities crossing cloud systems through continuously evaluated permission paths as fixed walls fade away.",
        ["identity perimeter", "machine identities", "permissions", "continuous trust"],
    ),
    "the-real-risk-of-ai-coding-agents-is-permission": (
        "An AI coding agent operating across source code, credentials, terminal actions and cloud resources, with its permission scope made visible.",
        ["AI coding agent", "permissions", "developer workspace", "access scope"],
    ),
    "three-reasons-you-havent-been-hacked": (
        "Three quiet security environments that look identical: one defended, one untargeted and one already compromised but undetected.",
        ["security silence", "well defended", "not targeted", "undetected compromise"],
    ),
    "three-types-of-cybersecurity-confidence": (
        "Three connected security structures built respectively on assumptions, borrowed assurance and repeated evidence and testing.",
        ["imagined confidence", "borrowed confidence", "earned confidence", "security evidence"],
    ),
    "when-active-directory-works-but-is-not-resilient": (
        "A functioning identity environment with normal authentication above hidden single points of failure and fragile recovery paths.",
        ["Active Directory", "authentication", "single points of failure", "recovery resilience"],
    ),
    "when-security-tools-become-the-noise": (
        "A security operations team surrounded by repetitive low-value signals while one high-confidence threat risks being lost in the noise.",
        ["security operations", "alert noise", "high-confidence signal", "attention"],
    ),
    "zero-trust-reducing-cost-of-being-wrong": (
        "An uncertain identity receiving narrowly scoped access through segmented compartments so a wrong trust decision remains contained.",
        ["Zero Trust", "scoped access", "segmentation", "contained impact"],
    ),
}


def text_content(node) -> str:
    return " ".join("".join(node.itertext()).split())


def index_metadata() -> dict[str, dict]:
    tree = html.fromstring((ARTICLE_DIR / "index.html").read_text(encoding="utf-8"))
    result = {}
    for card in tree.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), ' article-card ')]"):
        link = card.xpath(".//h2/a")[0]
        slug = Path(link.get("href")).stem
        parts = text_content(card.xpath(".//*[contains(@class, 'article-meta')]")[0]).split(" · ")
        excerpt = text_content(card.xpath("./p")[0])
        result[slug] = {
            "date": card.get("data-date"),
            "display_date": parts[0],
            "categories": [value.strip() for value in card.get("data-categories", "").split(",") if value.strip()],
            "reading_time": parts[-1],
            "excerpt": excerpt,
        }
    return result


def migrate() -> None:
    listing = index_metadata()
    records = []
    for path in sorted(ARTICLE_DIR.glob("*.html")):
        if path.name == "index.html":
            continue
        slug = path.stem
        tree = html.fromstring(path.read_text(encoding="utf-8"))
        main = tree.xpath("//main[contains(concat(' ', normalize-space(@class), ' '), ' reader ')]")[0]
        title_node = main.xpath("./h1")[0]
        lead_node = main.xpath("./p[contains(concat(' ', normalize-space(@class), ' '), ' lead ')]")[0]
        children = list(main)
        body_nodes = children[children.index(lead_node) + 1 :]
        description = tree.xpath("//meta[@name='description']/@content")
        visual_alt, relevance = VISUALS[slug]
        record = {
            "slug": slug,
            "title": text_content(title_node),
            "description": description[0] if description else text_content(lead_node),
            "lead": text_content(lead_node),
            **listing[slug],
            "pdf": f"papers/pdf/{slug}.pdf",
            "body_html": "\n".join(
                html.tostring(node, encoding="unicode", method="html").strip() for node in body_nodes
            ),
            "image": {
                "path": f"assets/images/articles/{slug}.webp",
                "alt": visual_alt,
                "visual_concept": visual_alt,
                "relevance_terms": relevance,
                "status": "approved",
                "width": 1600,
                "height": 900,
            },
        }
        records.append(record)

    records.sort(key=lambda item: (item["date"], item["slug"]), reverse=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({"schema_version": 1, "articles": records}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} articles to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    migrate()
