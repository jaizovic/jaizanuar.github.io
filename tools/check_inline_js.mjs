import fs from "node:fs";
import vm from "node:vm";

const source = fs.readFileSync("articles/index.html", "utf8");
const scripts = [...source.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map((match) => match[1]);

if (scripts.length === 0) {
  throw new Error("No inline article-listing script found");
}

for (const script of scripts) {
  new vm.Script(script, { filename: "articles/index.html" });
}

console.log(`Inline JavaScript syntax passed: ${scripts.length} script block`);
