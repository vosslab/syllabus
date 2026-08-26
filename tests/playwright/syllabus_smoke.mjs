// Selector contract:
// - Material route and navigation markup come from mkdocs.yml:7 and mkdocs.yml:36.
// - Current-course links and Blackboard context come from site_docs/index.md:1.
// - The important-dates wrapper comes from site_docs/fall_2026/shared/IMPORTANT_DATES.md:1;
//   its generated month tables come from pipeline/sync_important_dates.py:386.
// - Main headings, prose, tables, course-page links, and download links come from
//   site_docs/fall_2026/genetics/index.md:1.
// - Typography and focus-visible behavior come from site_docs/assets/stylesheets/site.css:17.
// - Course-header metadata comes from each course .meta.yml, overrides/main.html:5, and
//   site_docs/assets/stylesheets/site.css:23.

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
	for (const viewport of VIEWPORTS) {
		const context = await browser.newContext({
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
			assert.equal(response?.status(), 200, `${route} did not load in ${viewport.name}`);
			assert.equal(pageErrors.length, 0, `${route} raised browser errors: ${pageErrors.join("; ")}`);
			await page.locator("main h1").waitFor({ state: "visible" });
			const results = await new AxeBuilder({ page })
				.withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
				.analyze();
			assert.deepEqual(
				results.violations,
				[],
				`${route} ${viewport.name} accessibility violations:\n${JSON.stringify(results.violations, null, 2)}`,
			);
			const horizontalOverflow = await page.evaluate(() => {
				return document.documentElement.scrollWidth > window.innerWidth + 1;
			});
			assert.equal(horizontalOverflow, false, `${route} overflows the ${viewport.name} viewport`);
			if (COURSE_ROUTES.includes(route)) {
				checkCourseTypography(await getCourseTypography(page), viewport.name);
			}
			assert.deepEqual(
				externalFontRequests,
				[],
				`${route} ${viewport.name} requested external fonts`,
			);
			await page.close();
		}
		await context.close();
	}

	const homePage = await browser.newPage();
	await homePage.goto(`${staticServer.baseUrl}/`);
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
	}
	await homeMain
		.getByRole("heading", { name: "Blackboard and private course materials" })
		.waitFor();
	assert.equal(await homeMain.getByRole("heading", { name: "Archived terms" }).count(), 0);
	assert.equal(await homeMain.getByRole("heading", { name: "Secure course access" }).count(), 0);
	await homePage.close();

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
} finally {
	await browser.close();
	await staticServer.close();
}

console.log("PASS: syllabus browser accessibility audit");
