// Selector contract:
// - The homepage heading comes from site_docs/index.md:1.
// - The General Genetics heading comes from site_docs/fall_2026/genetics/index.md:1.
// - System-aware palette state comes from mkdocs.yml:18.
// - The production-shaped static root is generated at site/ by mkdocs.yml:5.

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

import { chromium } from "playwright";

import { startStaticServer } from "./helper_server.mjs";
import { REPO_ROOT } from "./repo_root.mjs";

const OUTPUT_ROOT = "/tmp/syllabus_readme_screenshots";
const SITE_ROOT = path.join(REPO_ROOT, "site");
const VIEWPORT = { width: 1440, height: 900 };

const CAPTURES = [
	{
		colorScheme: "light",
		heading: "Fall 2026 course syllabi",
		materialScheme: "default",
		name: "fall_2026_home_light.png",
		route: "/",
	},
	{
		colorScheme: "dark",
		heading: "BIOL 351/451 - General Genetics",
		materialScheme: "slate",
		name: "general_genetics_dark.png",
		route: "/fall_2026/genetics/",
	},
	{
		colorScheme: "light",
		heading: "Biotechnology company projects",
		materialScheme: "default",
		name: "biotech_project_expectations.png",
		route: "/fall_2026/biotech/PROJECTS/",
	},
];

assert.ok(fs.existsSync(SITE_ROOT), "site/ is missing; run the strict MkDocs build first");
fs.mkdirSync(OUTPUT_ROOT, { recursive: true });

const staticServer = await startStaticServer(SITE_ROOT);
const browser = await chromium.launch();

try {
	for (const capture of CAPTURES) {
		const context = await browser.newContext({
			colorScheme: capture.colorScheme,
			reducedMotion: "reduce",
			viewport: VIEWPORT,
		});
		const page = await context.newPage();
		await page.addInitScript(() => window.localStorage.clear());
		const response = await page.goto(`${staticServer.baseUrl}${capture.route}`, {
			waitUntil: "domcontentloaded",
		});
		assert.equal(response?.status(), 200, `${capture.route} did not load`);
		await page.getByRole("heading", { name: capture.heading }).waitFor({
			state: "visible",
		});
		await page.waitForFunction(
			(materialScheme) => document.body.dataset.mdColorScheme === materialScheme,
			capture.materialScheme,
		);
		await page.evaluate(() => document.fonts.ready);
		await page.screenshot({
			animations: "disabled",
			path: path.join(OUTPUT_ROOT, capture.name),
		});
		await page.close();
		await context.close();
	}
} finally {
	await browser.close();
	await staticServer.close();
}

console.log(`README screenshots written to ${OUTPUT_ROOT}`);
