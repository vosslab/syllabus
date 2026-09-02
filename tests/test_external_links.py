"""Tests for generated website external-link behavior."""

# Standard Library
import xml.etree.ElementTree

# PIP3 modules
import markdown

# local repo modules
import build_lib.external_links


SITE_URL = "https://vosslab.github.io/syllabus/"


#============================================
def render_markdown(markdown_text: str) -> xml.etree.ElementTree.Element:
	"""Render Markdown with the website-only external-link extension."""
	extension = build_lib.external_links.ExternalLinksExtension(SITE_URL)
	rendered = markdown.markdown(markdown_text, extensions=[extension, "attr_list"])
	root = xml.etree.ElementTree.fromstring(f"<div>{rendered}</div>")
	return root


#============================================
def test_external_link_receives_static_new_tab_attributes() -> None:
	"""Generated HTML owns safe new-tab behavior without browser JavaScript."""
	root = render_markdown("[Reference](https://example.org/resource)")
	link = root.find(".//a")
	description = root.find(
		f".//span[@id='{build_lib.external_links.EXTERNAL_LINK_DESCRIPTION_ID}']"
	)
	observed = (
		link.get("target"),
		link.get("rel"),
		link.get("aria-describedby"),
		description.get("class"),
		description.text,
	)
	assert observed == (
		"_blank",
		"noopener",
		build_lib.external_links.EXTERNAL_LINK_DESCRIPTION_ID,
		"md-visually-hidden",
		build_lib.external_links.EXTERNAL_LINK_DESCRIPTION,
	)


#============================================
def test_internal_and_non_web_links_keep_normal_navigation() -> None:
	"""Syllabus routes, anchors, downloads, and email remain in the current tab."""
	markdown_text = (
		"[Relative](COURSE_DETAILS.md)\n\n"
		"[Anchor](#topic)\n\n"
		"[Download](../../downloads/syllabus.pdf)\n\n"
		"[Email](mailto:teacher@example.org)\n\n"
		"[Absolute internal](https://vosslab.github.io/syllabus/EXTRA_CREDIT_MOVIES/)"
	)
	root = render_markdown(markdown_text)
	observed = [
		(link.get("target"), link.get("rel"), link.get("aria-describedby"))
		for link in root.iter("a")
	]
	assert observed == [(None, None, None)] * 5


#============================================
def test_site_boundary_classification() -> None:
	"""Only same-host destinations inside the configured site path stay internal."""
	assert not build_lib.external_links.is_external_web_link(
		"http://vosslab.github.io/syllabus/fall_2026/",
		SITE_URL,
	)
	assert build_lib.external_links.is_external_web_link(
		"https://vosslab.github.io/other-project/",
		SITE_URL,
	)
	assert build_lib.external_links.is_external_web_link(
		"//example.org/resource",
		SITE_URL,
	)


#============================================
def test_external_link_preserves_existing_relationships_and_description() -> None:
	"""Generation adds required tokens without discarding authored attributes."""
	markdown_text = (
		"[Reference](https://example.org/resource)"
		'{ rel="author" aria-describedby="citation-note" }'
	)
	root = render_markdown(markdown_text)
	link = root.find(".//a")
	observed = (link.get("rel"), link.get("aria-describedby"))
	assert observed == (
		"author noopener",
		"citation-note external-link-new-tab-description",
	)
