// Frontend precompile — docs/HARDENING.md Phase 5 (prod deploy path).
//
// Compiles every design/*.jsx and design/screens/*.jsx (plus the inline
// <script type="text/babel"> app shell inside design/Brain University.html)
// to plain .js under design/.compiled/, preserving the window-global
// architecture (classic scripts, no modules). Emits
// design/.compiled/manifest.json mapping each compiled file to a content
// hash, which the HTML's inline loader uses both as the prod/dev switch and
// as a cache-busting ?v= token.
//
// This is ADDITIVE: the zero-build dev mode (in-browser Babel over the raw
// .jsx files) keeps working unchanged whenever design/.compiled/ is absent.
// design/.compiled/ is a deploy artifact — never commit it (see .gitignore).
//
// Usage:  npm ci && node scripts/build_frontend.mjs
// Deploy: netlify.toml [build] command runs this after gen-config.mjs.

import { createHash } from "node:crypto";
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";
import babel from "@babel/core";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");
const designDir = join(root, "design");
const outDir = join(designDir, ".compiled");
const htmlPath = join(designDir, "Brain University.html");

// Babel options mirroring in-browser @babel/standalone's text/babel handling:
// the react preset only (classic runtime -> React.createElement globals),
// classic-script semantics, no module transform, modern JS left untouched.
const BABEL_OPTS = {
  presets: [["@babel/preset-react", {}]],
  // Every compiled file runs as a classic <script> sharing one global scope,
  // and many screens open with `const { useState, ... } = React;`. Top-level
  // const/let collide across scripts ("Can't create duplicate variable"), so
  // lower them to var, matching what in-browser Babel (preset-env) does in dev.
  plugins: ["@babel/plugin-transform-block-scoping"],
  sourceType: "script",
  babelrc: false,
  configFile: false,
  compact: false,
  sourceMaps: false,
};

function hashOf(code) {
  return createHash("sha256").update(code).digest("hex").slice(0, 16);
}

function syntaxCheck(code, name) {
  // Same check as `node --check`: throws on any syntax error.
  new vm.Script(code, { filename: name });
}

async function compileOne(source, sourceName, outRelPath, manifest) {
  const result = await babel.transformAsync(source, {
    ...BABEL_OPTS,
    filename: sourceName,
  });
  const code = result.code + "\n";
  syntaxCheck(code, outRelPath);
  const outPath = join(outDir, outRelPath);
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, code);
  manifest[outRelPath] = hashOf(code);
  console.log(`[build_frontend] ${sourceName} -> .compiled/${outRelPath}`);
}

function jsxFiles(dir, prefix) {
  return readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isFile() && e.name.endsWith(".jsx"))
    .map((e) => ({ abs: join(dir, e.name), rel: prefix + e.name }))
    .sort((a, b) => (a.rel < b.rel ? -1 : 1));
}

// Extract <script type="text/babel"> tags from the HTML: inline bodies get
// compiled to _inline_{n}.js (document order); src= refs are collected so we
// can fail loudly if the HTML references a .jsx the glob didn't cover.
function scanHtml(html) {
  const inline = [];
  const externalSrcs = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const attrs = m[1];
    if (!/type\s*=\s*["']text\/babel["']/i.test(attrs)) continue;
    const src = attrs.match(/\bsrc\s*=\s*["']([^"']+)["']/i);
    if (src) externalSrcs.push(src[1].split("?")[0]);
    else inline.push(m[2]);
  }
  return { inline, externalSrcs };
}

async function main() {
  rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });

  const manifest = {};
  const files = [
    ...jsxFiles(designDir, ""),
    ...jsxFiles(join(designDir, "screens"), "screens/"),
  ];
  if (files.length === 0) throw new Error("no .jsx files found under design/");

  for (const f of files) {
    const source = readFileSync(f.abs, "utf8");
    await compileOne(source, f.rel, f.rel.replace(/\.jsx$/, ".js"), manifest);
  }

  const html = readFileSync(htmlPath, "utf8");
  const { inline, externalSrcs } = scanHtml(html);
  if (inline.length === 0) {
    throw new Error("no inline <script type=\"text/babel\"> app shell found in the HTML");
  }
  for (let i = 0; i < inline.length; i++) {
    await compileOne(inline[i], `Brain University.html <inline #${i}>`, `_inline_${i}.js`, manifest);
  }

  // Referential integrity: every text/babel src in the HTML must have been
  // compiled, or the prod page would 404 on it.
  const missing = externalSrcs
    .map((s) => s.replace(/\.jsx$/, ".js"))
    .filter((k) => !(k in manifest));
  if (missing.length > 0) {
    throw new Error(`HTML references uncompiled jsx: ${missing.join(", ")}`);
  }

  // Format stamp: the HTML loader only trusts bundles built by this version of
  // the build, so a stale design/.compiled left over from an older build falls
  // back to dev mode instead of loading broken or missing bundles.
  manifest.__format = 2;
  writeFileSync(join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  console.log(`[build_frontend] wrote manifest.json (${Object.keys(manifest).length} entries)`);
}

main().catch((err) => {
  console.error("[build_frontend] FAILED:", err.message);
  process.exit(1);
});
