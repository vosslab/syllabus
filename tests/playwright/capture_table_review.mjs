// Capture every rendered syllabus table at desktop/mobile widths and in both themes.
// The report is implementation and release evidence, not a permanent pixel test.

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

import { chromium } from "playwright";

import { startStaticServer } from "./helper_server.mjs";
import { REPO_ROOT } from "./repo_root.mjs";

const SITE_ROOT = path.join(REPO_ROOT, "site");
const OUTPUT_PARENT = path.join(REPO_ROOT, "output");
const OUTPUT_ROOT = path.join(OUTPUT_PARENT, "table_review");
const SCREENSHOT_ROOT = path.join(OUTPUT_ROOT, "screenshots");

const STATES = [
	{
		colorScheme: "light",
		materialScheme: "default",
		name: "desktop_light",
		viewport: { width: 1440, height: 1000 },
	},
	{
		colorScheme: "dark",
		materialScheme: "slate",
		name: "desktop_dark",
		viewport: { width: 1440, height: 1000 },
	},
	{
		colorScheme: "light",
		materialScheme: "default",
		name: "mobile_light",
		viewport: { width: 390, height: 844 },
	},
	{
		colorScheme: "dark",
		materialScheme: "slate",
		name: "mobile_dark",
		viewport: { width: 390, height: 844 },
	},
];

//============================================
function collectHtmlPaths(directory) {
	const htmlPaths = [];
	for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
		const entryPath = path.join(directory, entry.name);
		if (entry.isDirectory()) {
			htmlPaths.push(...collectHtmlPaths(entryPath));
			continue;
		}
		if (entry.isFile() && entry.name.endsWith(".html")) {
			htmlPaths.push(entryPath);
		}
	}
	return htmlPaths.sort();
}

//============================================
function routeFromHtmlPath(htmlPath) {
	const relativePath = path.relative(SITE_ROOT, htmlPath);
	// ASVS 5.3.2: discovered pages must remain inside the trusted generated site root.
	assert.ok(relativePath !== "" && !relativePath.startsWith(".."));
	const posixPath = relativePath.split(path.sep).join("/");
	if (posixPath === "index.html") {
		return "/";
	}
	if (posixPath.endsWith("/index.html")) {
		return `/${posixPath.slice(0, -"index.html".length)}`;
	}
	return `/${posixPath}`;
}

//============================================
function routeSlug(route) {
	if (route === "/") {
		return "home";
	}
	const slug = route.replace(/^\/+|\/+$/g, "").replace(/[^a-zA-Z0-9]+/g, "_");
	return slug || "page";
}

//============================================
function escapeHtml(value) {
	// ASVS 1.2.1: encode captured page text at the final HTML report boundary.
	return String(value)
		.replaceAll("&", "&amp;")
		.replaceAll("<", "&lt;")
		.replaceAll(">", "&gt;")
		.replaceAll('"', "&quot;")
		.replaceAll("'", "&#39;");
}

//============================================
function renderDocument(title, body) {
	return `<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>${escapeHtml(title)}</title>
	<style>
		:root { color-scheme: light; font-family: system-ui, sans-serif; }
		body { background: #eef2ef; color: #17221b; margin: 0; padding: 1.25rem; }
		a { color: #005f37; }
		h1 { margin-block-start: 0; }
		.review-grid { display: grid; gap: 1rem; grid-template-columns: repeat(3, minmax(0, 1fr)); }
		.review-card { background: #fff; border: 1px solid #aebbb3; border-radius: 0.5rem; margin: 0; padding: 0.75rem; }
		.review-card img { background: #fff; border: 1px solid #d4ddd7; display: block; height: auto; width: 100%; }
		.review-card code { overflow-wrap: anywhere; }
		.review-card figcaption { font-size: 0.82rem; line-height: 1.4; margin-block-start: 0.6rem; }
		.review-card strong { display: block; font-size: 0.95rem; }
		.review-links { display: flex; flex-wrap: wrap; gap: 0.75rem; padding: 0; }
		.review-links li { list-style: none; }
		@media (max-width: 65rem) { .review-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
		@media (max-width: 42rem) { .review-grid { grid-template-columns: 1fr; } }
	</style>
</head>
<body>
${body}
</body>
</html>
`;
}

//============================================
function renderStateSheet(state, records) {
	const cards = records.map((record) => {
		const calculatedWidths = record.columns.map((column, index) => {
			return `${column.header}: ${record.calculatedWidths[index]}%`;
		}).join(" | ");
		const renderedWidths = record.columns.map((column) => `${column.header}: ${column.widthPx}px`).join(" | ");
		return `<figure class="review-card">
	<img src="${escapeHtml(record.relativeScreenshot)}" alt="Rendered table from ${escapeHtml(record.route)}">
	<figcaption>
		<strong>${escapeHtml(record.profile)} - ${escapeHtml(record.headers.join(" | "))}</strong>
		<code>${escapeHtml(record.route)}</code><br>
		Calculated: ${escapeHtml(calculatedWidths)}<br>
		Rendered: ${escapeHtml(renderedWidths)}<br>
		Series ${escapeHtml(record.seriesSize)}; demand ${escapeHtml(record.minimumWidth)}; table ${escapeHtml(record.tableWidthPx)}px; scroll area ${escapeHtml(record.containerWidthPx)}px
	</figcaption>
</figure>`;
	}).join("\n");
	const body = `<h1>Table review: ${escapeHtml(state.name)}</h1>
<p><a href="index.html">Back to report index</a></p>
<main class="review-grid">${cards}</main>`;
	return renderDocument(`Table review: ${state.name}`, body);
}

//============================================
function renderIndex(records) {
	const links = STATES.map((state) => {
		return `<li><a href="contact_sheet_${state.name}.html">${escapeHtml(state.name)}</a></li>`;
	}).join("\n");
	const uniqueTables = new Set(records.map((record) => `${record.route}#${record.tableIndex}`));
	const profiles = [...new Set(records.map((record) => record.profile))].sort();
	const body = `<h1>Rendered syllabus table review</h1>
<p>${uniqueTables.size} tables captured in ${STATES.length} viewport/theme states.</p>
<p>Profiles: ${escapeHtml(profiles.join(", "))}</p>
<ul class="review-links">${links}</ul>
<p><a href="table_report.json">Machine-readable measurements</a></p>`;
	return renderDocument("Rendered syllabus table review", body);
}

//============================================
async function measureTable(table) {
	const measurement = await table.evaluate((element) => {
		const normalize = (value) => value.replace(/\s+/g, " ").trim();
		const headerCells = [...element.querySelectorAll("thead th")];
		const bodyRows = [...element.querySelectorAll("tbody tr")];
		const columns = headerCells.map((headerCell, columnIndex) => {
			let maxLines = 1;
			let maxTextLength = 0;
			for (const row of bodyRows) {
				const cell = row.children[columnIndex];
				if (!(cell instanceof HTMLElement)) {
					continue;
				}
				const style = getComputedStyle(cell);
				const lineHeight = Number.parseFloat(style.lineHeight);
				const padding = Number.parseFloat(style.paddingTop) + Number.parseFloat(style.paddingBottom);
				const contentHeight = Math.max(0, cell.getBoundingClientRect().height - padding);
				if (Number.isFinite(lineHeight) && lineHeight > 0) {
					maxLines = Math.max(maxLines, Math.round(contentHeight / lineHeight));
				}
				maxTextLength = Math.max(maxTextLength, normalize(cell.textContent ?? "").length);
			}
			const width = headerCell.getBoundingClientRect().width;
			return {
				header: normalize(headerCell.textContent ?? ""),
				maxLines,
				maxTextLength,
				widthPx: Math.round(width),
			};
		});
		const container = element.closest(".md-typeset__scrollwrap")
			?? element.closest(".md-typeset__table")
			?? element;
		const parseIntegerList = (value) => value.split(",").map((item) => Number.parseInt(item, 10));
		return {
			calculatedDemands: parseIntegerList(element.dataset.tableDemands ?? ""),
			calculatedWidths: parseIntegerList(element.dataset.tableWidths ?? ""),
			columns,
			containerScrollWidthPx: Math.round(container.scrollWidth),
			containerWidthPx: Math.round(container.getBoundingClientRect().width),
			headers: headerCells.map((cell) => normalize(cell.textContent ?? "")),
			minimumWidth: element.style.getPropertyValue("--table-minimum-width"),
			profile: element.dataset.tableProfile ?? "unclassified",
			seriesSize: Number.parseInt(element.dataset.tableSeriesSize ?? "1", 10),
			tableWidthPx: Math.round(element.getBoundingClientRect().width),
		};
	});
	return measurement;
}

//============================================
async function captureTables(browser, baseUrl, routes) {
	const records = [];
	for (const state of STATES) {
		console.log(`Capturing ${state.name} table renders`);
		const context = await browser.newContext({
			colorScheme: state.colorScheme,
			reducedMotion: "reduce",
			viewport: state.viewport,
		});
		for (const route of routes) {
			const page = await context.newPage();
			await page.addInitScript(() => window.localStorage.clear());
			const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "domcontentloaded" });
			assert.equal(response?.status(), 200, `${route} did not load`);
			await page.waitForFunction(
				(materialScheme) => document.body.dataset.mdColorScheme === materialScheme,
				state.materialScheme,
			);
			await page.evaluate(() => document.fonts.ready);
			const documentOverflows = await page.evaluate(() => {
				return document.documentElement.scrollWidth > window.innerWidth + 1;
			});
			assert.equal(
				documentOverflows,
				false,
				`${route} overflows the ${state.name} document viewport`,
			);
			const tables = page.locator("main .md-typeset table");
			const tableCount = await tables.count();
			for (let tableIndex = 0; tableIndex < tableCount; tableIndex += 1) {
				const table = tables.nth(tableIndex);
				const captureId = `${state.name}_${routeSlug(route)}_${tableIndex + 1}`;
				await table.evaluate((element, value) => {
					const target = element.closest(".md-typeset__scrollwrap")
						?? element.closest(".md-typeset__table")
						?? element;
					target.dataset.tableReviewCapture = value;
				}, captureId);
				const target = page.locator(`[data-table-review-capture="${captureId}"]`);
				await target.scrollIntoViewIfNeeded();
				const filename = `${captureId}.png`;
				const screenshotPath = path.join(SCREENSHOT_ROOT, filename);
				await target.screenshot({ animations: "disabled", path: screenshotPath });
				const measurement = await measureTable(table);
				records.push({
					...measurement,
					colorScheme: state.colorScheme,
					relativeScreenshot: `screenshots/${filename}`,
					route,
					state: state.name,
					tableIndex: tableIndex + 1,
					viewport: state.viewport,
				});
			}
			await page.close();
		}
		await context.close();
	}
	return records;
}

//============================================
async function captureContactSheets(browser) {
	const reportServer = await startStaticServer(OUTPUT_ROOT);
	try {
		const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
		for (const state of STATES) {
			await page.goto(`${reportServer.baseUrl}/contact_sheet_${state.name}.html`, {
				waitUntil: "networkidle",
			});
			await page.locator("img").evaluateAll(async (images) => {
				await Promise.all(images.map((image) => image.decode()));
			});
			await page.screenshot({
				animations: "disabled",
				fullPage: true,
				path: path.join(OUTPUT_ROOT, `contact_sheet_${state.name}.png`),
			});
		}
		await page.close();
	} finally {
		await reportServer.close();
	}
}

assert.ok(fs.existsSync(SITE_ROOT), "site/ is missing; run the production build first");
// ASVS 5.3.2: the stable generated destination is fixed below repository output/.
assert.equal(path.dirname(OUTPUT_ROOT), OUTPUT_PARENT);
fs.mkdirSync(OUTPUT_PARENT, { recursive: true });
fs.rmSync(OUTPUT_ROOT, { force: true, recursive: true });
fs.mkdirSync(SCREENSHOT_ROOT, { recursive: true });

const routes = collectHtmlPaths(SITE_ROOT)
	.filter((htmlPath) => fs.readFileSync(htmlPath, "utf8").includes("<table"))
	.map(routeFromHtmlPath);
const siteServer = await startStaticServer(SITE_ROOT);
const browser = await chromium.launch();

try {
	const records = await captureTables(browser, siteServer.baseUrl, routes);
	assert.ok(records.length > 0, "No rendered syllabus tables were found");
	assert.ok(
		records.every((record) => record.profile !== "unclassified"),
		"One or more rendered tables has no semantic table profile",
	);
	assert.ok(
		records.every((record) => (
			record.calculatedWidths.length === record.headers.length
			&& record.calculatedDemands.length === record.headers.length
			&& record.calculatedWidths.reduce((total, value) => total + value, 0) === 100
		)),
		"One or more rendered tables has an invalid content-derived layout",
	);
	fs.writeFileSync(
		path.join(OUTPUT_ROOT, "table_report.json"),
		`${JSON.stringify(records, null, "\t")}\n`,
		"utf8",
	);
	fs.writeFileSync(path.join(OUTPUT_ROOT, "index.html"), renderIndex(records), "utf8");
	for (const state of STATES) {
		const stateRecords = records.filter((record) => record.state === state.name);
		const stateHtml = renderStateSheet(state, stateRecords);
		fs.writeFileSync(
			path.join(OUTPUT_ROOT, `contact_sheet_${state.name}.html`),
			stateHtml,
			"utf8",
		);
	}
	await captureContactSheets(browser);
	const tableCount = new Set(records.map((record) => `${record.route}#${record.tableIndex}`)).size;
	console.log(`Captured ${tableCount} tables in ${STATES.length} states under ${OUTPUT_ROOT}`);
} finally {
	await browser.close();
	await siteServer.close();
}
