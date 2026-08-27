// Selector contract:
// - Material theme markup comes from mkdocs.yml:12; navigation labels and routes come from
//   mkdocs.yml:77.
// - Current-course links and Blackboard context come from site_docs/index.md:1; term download
//   access comes from site_docs/fall_2026/index.md:7.
// - The important-dates wrapper comes from site_docs/fall_2026/shared/IMPORTANT_DATES.md:1;
//   its generated month tables come from pipeline/sync_important_dates.py:386.
// - Main headings, prose, tables, course-page links, and download links come from
//   site_docs/fall_2026/genetics/index.md:1.
// - Typography and focus-visible behavior come from site_docs/assets/stylesheets/site.css:109 and
//   site_docs/assets/stylesheets/site.css:321.
// - System-aware palette toggles come from mkdocs.yml:18; dark color roles come from
//   site_docs/assets/stylesheets/site.css:55.
// - Course-header metadata comes from each course .meta.yml, overrides/main.html:5, and
//   site_docs/assets/stylesheets/site.css:78.
// - The shared protein favicon and header logo come from mkdocs.yml:15,
//   mkdocs.yml:16, and site_docs/assets/images/favicon.svg:1.
// - Footer social-link names and destinations come from mkdocs.yml:58.

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

import { REPO_ROOT } from "./repo_root.mjs";
import { startStaticServer } from "./helper_server.mjs";

const COURSE_ROUTES = [
	"/fall_2026/biostats/",
	"/fall_2026/genetics/",
	"/fall_2026/biotech/",
];

const ROUTES = [
	"/",
	"/fall_2026/",
	"/fall_2026/shared/IMPORTANT_DATES/",
	...COURSE_ROUTES,
	"/fall_2026/shared/policies/",
	"/fall_2026/shared/INSTRUCTOR_INFORMATION/",
	"/fall_2026/shared/policies/COURSE_DELIVERY/",
	"/fall_2026/shared/policies/ASSESSMENT/",
	"/fall_2026/shared/policies/ATTENDANCE_AND_ACCOMMODATIONS/",
	"/fall_2026/shared/policies/ACADEMIC_INTEGRITY/",
	"/fall_2026/shared/policies/COURSE_EXPECTATIONS/",
	"/fall_2026/shared/policies/INCLUSION_AND_SAFETY/",
	"/fall_2026/shared/policies/COURSE_ENROLLMENT/",
	"/fall_2026/shared/STUDENT_RESOURCES/",
];

const VIEWPORTS = [
	{ name: "desktop", width: 1280, height: 900 },
	{ name: "mobile", width: 390, height: 844 },
];

const COLOR_SCHEMES = [
	{
		name: "light",
		materialScheme: "default",
		toggleName: "Switch to dark mode",
	},
	{
		name: "dark",
		materialScheme: "slate",
		toggleName: "Switch to light mode",
	},
];

const DARK_GREEN_SURFACE = "rgb(30, 41, 35)";
const ROOSEVELT_GREEN = "rgb(115, 193, 103)";
const ROOSEVELT_LINK_GREEN = "rgb(0, 120, 73)";
const WHITE = "rgb(255, 255, 255)";

const SOCIAL_LINKS = [
	{ name: "GitHub", href: "https://github.com/vosslab" },
	{ name: "YouTube", href: "https://www.youtube.com/neilvosslab" },
	{ name: "Bluesky", href: "https://bsky.app/profile/neilvosslab.bsky.social" },
	{ name: "LinkedIn", href: "https://www.linkedin.com/in/vosslab" },
	{ name: "Facebook", href: "https://www.facebook.com/neilvosslab" },
];

async function getCourseTypography(page) {
	return page.evaluate(async () => {
		const fontSize = (selector) => {
			const element = document.querySelector(selector);
			if (!element) {
				throw new Error(`Missing typography test element: ${selector}`);
			}
			return Number.parseFloat(window.getComputedStyle(element).fontSize);
		};
		const body = document.querySelector("main p");
		if (!body) {
			throw new Error("Missing course body text for typography test");
		}
		const normalFaces = await document.fonts.load(
			'400 1em "Atkinson Hyperlegible Next"',
			"Il1O0",
		);
		const boldFaces = await document.fonts.load(
			'700 1em "Atkinson Hyperlegible Next"',
			"Il1O0",
		);
		const italicFaces = await document.fonts.load(
			'italic 400 1em "Atkinson Hyperlegible Next"',
			"Il1O0",
		);
		return {
			boldFaces: boldFaces.length,
			body: fontSize("main p"),
			bodyFamily: window.getComputedStyle(body).fontFamily,
			italicFaces: italicFaces.length,
			normalFaces: normalFaces.length,
			table: fontSize("main table td"),
		};
	});
}

function checkCourseTypography(typography, viewportName) {
	assert.ok(typography.bodyFamily.includes("Atkinson Hyperlegible Next"));
	assert.ok(typography.normalFaces > 0, `${viewportName} regular font did not load`);
	assert.ok(typography.boldFaces > 0, `${viewportName} bold font did not load`);
	assert.ok(typography.italicFaces > 0, `${viewportName} italic font did not load`);
	assert.ok(
		typography.table >= typography.body,
		`${viewportName} table text ${typography.table}px is smaller than course text ${typography.body}px`,
	);
}

async function getResponsiveReadingMetrics(page, baseUrl, width) {
	await page.setViewportSize({ width, height: 900 });
	const response = await page.goto(
		`${baseUrl}/fall_2026/shared/policies/ACADEMIC_INTEGRITY/`,
		{ waitUntil: "domcontentloaded" },
	);
	assert.equal(response?.status(), 200, `Responsive typography route failed at ${width}px`);
	await page.locator("main h1").waitFor({ state: "visible" });
	return page.evaluate(() => {
		const body = document.querySelector("main p");
		const header = document.querySelector(".md-header__topic");
		const navigation = document.querySelector(".md-sidebar--primary .md-nav");
		const readingColumn = document.querySelector("main h1");
		if (!body || !header || !navigation || !readingColumn) {
			throw new Error("Responsive typography elements are missing");
		}
		const bodyFontSize = Number.parseFloat(window.getComputedStyle(body).fontSize);
		return {
			bodyFontSize,
			headerFontSize: Number.parseFloat(window.getComputedStyle(header).fontSize),
			navigationFontSize: Number.parseFloat(
				window.getComputedStyle(navigation).fontSize,
			),
			readingMeasure: readingColumn.getBoundingClientRect().width / bodyFontSize,
		};
	});
}

async function getHeaderColor(page, baseUrl, route) {
	const response = await page.goto(`${baseUrl}${route}`, {
		waitUntil: "domcontentloaded",
	});
	assert.equal(response?.status(), 200, `${route} did not load for header-color review`);
	const header = page.locator(".md-header");
	await header.waitFor({ state: "visible" });
	return header.evaluate((element) => window.getComputedStyle(element).backgroundColor);
}

const siteRoot = path.join(REPO_ROOT, "site");
assert.ok(fs.existsSync(siteRoot), "site/ is missing; run python3 pipeline/build_site.py first");

const staticServer = await startStaticServer(siteRoot);
const siteOrigin = new URL(staticServer.baseUrl).origin;
const browser = await chromium.launch();

try {
	for (const colorScheme of COLOR_SCHEMES) {
		for (const viewport of VIEWPORTS) {
			const context = await browser.newContext({
				colorScheme: colorScheme.name,
				viewport: { width: viewport.width, height: viewport.height },
			});
			for (const route of ROUTES) {
				const page = await context.newPage();
				const externalFontRequests = [];
				const pageErrors = [];
				page.on("pageerror", (error) => pageErrors.push(error.message));
				page.on("request", (request) => {
					if (request.resourceType() !== "font") {
						return;
					}
					if (new URL(request.url()).origin !== siteOrigin) {
						externalFontRequests.push(request.url());
					}
				});
				const response = await page.goto(`${staticServer.baseUrl}${route}`, {
					waitUntil: "domcontentloaded",
				});
				assert.equal(
					response?.status(),
					200,
					`${route} did not load in ${viewport.name} ${colorScheme.name} mode`,
				);
				assert.equal(
					pageErrors.length,
					0,
					`${route} raised browser errors: ${pageErrors.join("; ")}`,
				);
				await page.locator("main h1").waitFor({ state: "visible" });
				assert.equal(
					await page.locator("body").getAttribute("data-md-color-scheme"),
					colorScheme.materialScheme,
				);
				if (route === "/") {
					await page
						.getByTitle(colorScheme.toggleName, { exact: true })
						.waitFor({ state: "visible" });
				}
				const results = await new AxeBuilder({ page })
					.withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
					.analyze();
				assert.deepEqual(
					results.violations,
					[],
					`${route} ${viewport.name} ${colorScheme.name} accessibility violations:\n${JSON.stringify(results.violations, null, 2)}`,
				);
				const horizontalOverflow = await page.evaluate(() => {
					return document.documentElement.scrollWidth > window.innerWidth + 1;
				});
				assert.equal(
					horizontalOverflow,
					false,
					`${route} overflows the ${viewport.name} ${colorScheme.name} viewport`,
				);
				if (COURSE_ROUTES.includes(route)) {
					checkCourseTypography(
						await getCourseTypography(page),
						`${viewport.name} ${colorScheme.name}`,
					);
				}
				assert.deepEqual(
					externalFontRequests,
					[],
					`${route} ${viewport.name} ${colorScheme.name} requested external fonts`,
				);
				await page.close();
			}
			await context.close();
		}
	}

	const themeContext = await browser.newContext({ colorScheme: "light" });
	const homePage = await themeContext.newPage();
	await homePage.goto(`${staticServer.baseUrl}/`);
	const faviconLink = homePage.locator('link[rel="icon"]');
	const faviconUrl = new URL(await faviconLink.getAttribute("href"), homePage.url());
	assert.equal(faviconUrl.pathname, "/assets/images/favicon.svg");
	const faviconResponse = await homePage.request.get(faviconUrl.href);
	assert.equal(faviconResponse.status(), 200, "Protein favicon did not load");
	assert.match(faviconResponse.headers()["content-type"], /^image\/svg\+xml/);
	const homeMain = homePage.getByRole("article");
	const currentCourses = [
		{
			name: "BIOL 318 and BIOL 418 - Biostatistics",
			pathname: "/fall_2026/biostats/",
		},
		{
			name: "BIOL 351 and BIOL 451 - General Genetics",
			pathname: "/fall_2026/genetics/",
		},
		{
			name: "BIOL 480 - Applications of Biotechnology",
			pathname: "/fall_2026/biotech/",
		},
	];
	for (const course of currentCourses) {
		const courseLink = homeMain.getByRole("link", { name: course.name, exact: true });
		await courseLink.waitFor();
		const courseUrl = new URL(await courseLink.getAttribute("href"), homePage.url());
		assert.equal(courseUrl.pathname, course.pathname);
		assert.equal(
			await courseLink.evaluate((element) => getComputedStyle(element).color),
			ROOSEVELT_LINK_GREEN,
		);
	}
	await homeMain
		.getByRole("heading", { name: "Blackboard and private course materials" })
		.waitFor();
	assert.equal(await homeMain.getByRole("heading", { name: "Archived terms" }).count(), 0);
	assert.equal(await homeMain.getByRole("heading", { name: "Secure course access" }).count(), 0);
	const socialFooter = homePage.locator(".md-social");
	await socialFooter.waitFor({ state: "visible" });
	for (const social of SOCIAL_LINKS) {
		const socialLink = socialFooter.getByRole("link", { name: social.name, exact: true });
		await socialLink.waitFor({ state: "visible" });
		assert.equal(await socialLink.getAttribute("href"), social.href);
		assert.equal(await socialLink.getAttribute("target"), "_blank");
		assert.match(await socialLink.getAttribute("rel"), /\bnoopener\b/);
	}
	await homePage.getByTitle("Switch to dark mode", { exact: true }).click();
	await homePage.waitForFunction(() => document.body.dataset.mdColorScheme === "slate");
	const darkPageBackground = await homePage
		.locator("body")
		.evaluate((element) => getComputedStyle(element).backgroundColor);
	assert.equal(
		darkPageBackground,
		DARK_GREEN_SURFACE,
	);
	for (const course of currentCourses) {
		const courseLink = homeMain.getByRole("link", { name: course.name, exact: true });
		assert.equal(
			await courseLink.evaluate((element) => getComputedStyle(element).color),
			ROOSEVELT_GREEN,
		);
	}
	await homePage.goto(`${staticServer.baseUrl}/fall_2026/genetics/`);
	assert.equal(await homePage.locator("body").getAttribute("data-md-color-scheme"), "slate");
	assert.equal(
		await homePage
			.locator(".md-header")
			.evaluate((element) => getComputedStyle(element).color),
		WHITE,
	);
	await homePage.getByTitle("Switch to light mode", { exact: true }).click();
	await homePage.waitForFunction(() => document.body.dataset.mdColorScheme === "default");
	await homePage.close();
	await themeContext.close();

	const accommodationPage = await browser.newPage();
	await accommodationPage.goto(
		`${staticServer.baseUrl}/fall_2026/shared/policies/ATTENDANCE_AND_ACCOMMODATIONS/`,
	);
	const absenceTable = accommodationPage.getByRole("table").filter({
		hasText: "First communicated",
	});
	await absenceTable.waitFor();
	assert.deepEqual(await absenceTable.getByRole("columnheader").allTextContents(), [
		"Absence type",
		"Score",
		"Included in total points",
	]);
	await accommodationPage.close();

	const gradingPage = await browser.newPage();
	await gradingPage.goto(`${staticServer.baseUrl}/fall_2026/shared/policies/ASSESSMENT/`);
	const gradeTable = gradingPage.getByRole("table").first();
	await gradeTable.waitFor();
	assert.deepEqual(await gradeTable.getByRole("columnheader").allTextContents(), [
		"Percentage",
		"Grade",
	]);
	await gradingPage.close();

	const termPage = await browser.newPage();
	await termPage.goto(`${staticServer.baseUrl}/fall_2026/`);
	const termDownloadLinks = await termPage
		.getByRole("link", {
			name: /^BIOL .+ complete syllabus \((?:PDF|DOCX)\)$/,
		})
		.all();
	const actualDownloadPaths = [];
	for (const downloadLink of termDownloadLinks) {
		const accessibleName = await downloadLink.getAttribute("aria-label");
		const downloadUrl = new URL(
			await downloadLink.getAttribute("href"),
			termPage.url(),
		);
		actualDownloadPaths.push(downloadUrl.pathname);
		assert.equal(downloadUrl.origin, siteOrigin);
		assert.match(
			accessibleName,
			/^BIOL .+ complete syllabus \((?:PDF|DOCX)\)$/,
		);
		const downloadResponse = await termPage.request.get(downloadUrl.href);
		assert.equal(
			downloadResponse.status(),
			200,
			`${accessibleName} did not load`,
		);
	}
	const expectedDownloadPaths = fs
		.readdirSync(path.join(siteRoot, "downloads"))
		.filter((fileName) => [".docx", ".pdf"].includes(path.extname(fileName)))
		.map((fileName) => `/downloads/${fileName}`)
		.sort();
	assert.deepEqual(actualDownloadPaths.sort(), expectedDownloadPaths);
	await termPage.close();

	const coursePage = await browser.newPage();
	await coursePage.goto(`${staticServer.baseUrl}/fall_2026/genetics/`);
	const courseMain = coursePage.getByRole("article");
	await courseMain.getByRole("link", { name: "Meetings and instructor" }).waitFor();
	await courseMain
		.getByRole("link", { name: "Learning Objectives, Outcomes, and Goals" })
		.waitFor();
	await courseMain.getByRole("link", { name: "Dr. Voss course policies" }).waitFor();
	await courseMain.getByRole("link", { name: "Help and student services" }).waitFor();
	const layoutOrder = await coursePage.evaluate(() => {
		const pageLinks = document.querySelector(".course-page-links");
		const courseTable = document.querySelector("main table");
		const downloads = document.querySelector(".syllabus-downloads");
		if (!pageLinks || !courseTable || !downloads) {
			throw new Error("Course landing page is missing required content groups");
		}
		return {
			linksBeforeTable: Boolean(
				pageLinks.compareDocumentPosition(courseTable) & Node.DOCUMENT_POSITION_FOLLOWING,
			),
			tableBeforeDownloads: Boolean(
				courseTable.compareDocumentPosition(downloads) & Node.DOCUMENT_POSITION_FOLLOWING,
			),
		};
	});
	assert.equal(layoutOrder.linksBeforeTable, true, "Course-page links must precede the summary");
	assert.equal(
		layoutOrder.tableBeforeDownloads,
		true,
		"Complete-syllabus downloads must follow the summary",
	);
	const pdfLink = courseMain.getByRole("link", {
		name: "Download the complete course syllabus (PDF)",
	});
	const docxLink = courseMain.getByRole("link", {
		name: "Download the complete course syllabus (DOCX)",
	});
	const pdfUrl = new URL(await pdfLink.getAttribute("href"), coursePage.url());
	const docxUrl = new URL(await docxLink.getAttribute("href"), coursePage.url());
	assert.equal(pdfUrl.origin, siteOrigin);
	assert.equal(docxUrl.origin, siteOrigin);
	assert.match(pdfUrl.pathname, /\.pdf$/);
	assert.match(docxUrl.pathname, /\.docx$/);
	const pdfResponse = await coursePage.request.get(pdfUrl.href);
	const docxResponse = await coursePage.request.get(docxUrl.href);
	assert.equal(pdfResponse.status(), 200, "PDF download did not load");
	assert.equal(docxResponse.status(), 200, "DOCX download did not load");
	await pdfLink.focus();
	assert.equal(await pdfLink.evaluate((element) => element.matches(":focus-visible")), true);
	await docxLink.focus();
	assert.equal(await docxLink.evaluate((element) => element.matches(":focus-visible")), true);
	await coursePage.close();

	const headerPage = await browser.newPage();
	const homeColor = await getHeaderColor(headerPage, staticServer.baseUrl, "/");
	const biostatisticsColor = await getHeaderColor(
		headerPage,
		staticServer.baseUrl,
		"/fall_2026/biostats/",
	);
	const biostatisticsDetailsColor = await getHeaderColor(
		headerPage,
		staticServer.baseUrl,
		"/fall_2026/biostats/COURSE_DETAILS/",
	);
	const geneticsColor = await getHeaderColor(
		headerPage,
		staticServer.baseUrl,
		"/fall_2026/genetics/",
	);
	const biotechnologyColor = await getHeaderColor(
		headerPage,
		staticServer.baseUrl,
		"/fall_2026/biotech/",
	);
	const sharedPageColor = await getHeaderColor(
		headerPage,
		staticServer.baseUrl,
		"/fall_2026/shared/policies/",
	);
	assert.equal(homeColor, ROOSEVELT_GREEN);
	assert.equal(sharedPageColor, ROOSEVELT_GREEN);
	assert.equal(
		biostatisticsDetailsColor,
		biostatisticsColor,
		"Course subpages must inherit their course header color",
	);
	assert.notEqual(biostatisticsColor, geneticsColor);
	assert.notEqual(biostatisticsColor, biotechnologyColor);
	assert.notEqual(geneticsColor, biotechnologyColor);
	assert.notEqual(sharedPageColor, biostatisticsColor);
	assert.notEqual(sharedPageColor, geneticsColor);
	assert.notEqual(sharedPageColor, biotechnologyColor);
	await headerPage.close();

	const responsivePage = await browser.newPage();
	const desktopReading = await getResponsiveReadingMetrics(
		responsivePage,
		staticServer.baseUrl,
		1280,
	);
	const wideReading = await getResponsiveReadingMetrics(
		responsivePage,
		staticServer.baseUrl,
		2004,
	);
	assert.equal(
		wideReading.bodyFontSize,
		desktopReading.bodyFontSize,
		"Widening the browser must not enlarge body text",
	);
	assert.equal(
		wideReading.navigationFontSize,
		desktopReading.navigationFontSize,
		"Widening the browser must not enlarge navigation text",
	);
	assert.equal(
		wideReading.headerFontSize,
		desktopReading.headerFontSize,
		"Widening the browser must not enlarge header text",
	);
	assert.ok(
		wideReading.readingMeasure > desktopReading.readingMeasure,
		"Widening the browser must increase the reading measure",
	);
	await responsivePage.close();
} finally {
	await browser.close();
	await staticServer.close();
}

console.log("PASS: syllabus browser accessibility audit");
