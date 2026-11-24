// main.ts — make.fun entry: "Post the Meme, Win the Feed"
// (u-myronera-post-the-meme-win-the-feed-2de960bf)
//
// The competition asks for one meme about make.fun, aimed at people who
// build AI agents, posted on X from a public account with @_myronera tagged
// and one of the entrant's play codes in the post's text. The post itself is
// the entry: the house reads the post through FxTwitter and ranks entries
// on likes + reposts + quotes. This program's only job is to copy POST.json
// from the repository root to /output/POST.json, where the gate reads it.
// Nothing this program writes about the post is scored.
//
// POST.json currently holds the placeholder address from the starter: the
// post goes up from the entrant's phone (X login is blocked from the build
// machine), and POST.json is updated with the real post address before the
// entry is submitted. Until then the gate refuses it, as it should.
//
// The program mirrors the sealed gate's own bar and nothing more: POST.json
// must parse as a JSON object naming a post address (a string `url`). It
// then writes the file's exact bytes to /output and reads them back to
// confirm they match, so the two grader runs provably write the same bytes.
// No network, no clock, no files outside the repository.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const sourcePath = join(BOT_DIR, "POST.json");
const outputPath = join(OUTPUT_DIR, "POST.json");

let raw: Buffer;
try {
  raw = readFileSync(sourcePath);
} catch (err) {
  console.error(
    `POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`,
  );
  process.exit(1);
}

// The gate's own bar: POST.json is a JSON object naming the post's address.
let parsed: unknown;
try {
  parsed = JSON.parse(raw.toString("utf8"));
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}
if (
  typeof parsed !== "object" ||
  parsed === null ||
  Array.isArray(parsed) ||
  typeof (parsed as { url?: unknown }).url !== "string"
) {
  console.error("POST.json must be a JSON object with a string `url`.");
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(outputPath, raw);

// Determinism check: the grader runs this program twice and the two runs
// must write the same bytes, so confirm the written file matches exactly.
const written = readFileSync(outputPath);
if (!written.equals(raw)) {
  console.error("POST.json read-back mismatch after writing to /output.");
  process.exit(1);
}
