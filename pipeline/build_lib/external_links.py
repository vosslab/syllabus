"""Add safe, accessible new-tab behavior to off-site website links."""

# Standard Library
import urllib.parse
import xml.etree.ElementTree

# PIP3 modules
import markdown
import markdown.extensions
import markdown.treeprocessors


EXTERNAL_LINK_DESCRIPTION_ID = "external-link-new-tab-description"
EXTERNAL_LINK_DESCRIPTION = "Opens in a new tab."


#============================================
def is_external_web_link(href: str, site_url: str) -> bool:
	"""Return whether an HTTP(S) destination falls outside the configured site."""
	site_parts = urllib.parse.urlsplit(site_url)
	site_scheme = site_parts.scheme.lower()
	if site_scheme not in ("http", "https") or not site_parts.netloc:
		raise ValueError("site_url must be an absolute HTTP or HTTPS URL")
	href_parts = urllib.parse.urlsplit(href)
	href_scheme = href_parts.scheme.lower()
	is_protocol_relative = not href_scheme and bool(href_parts.netloc)
	if href_scheme not in ("http", "https") and not is_protocol_relative:
		return False
	if (
		href_parts.hostname,
		href_parts.port,
	) != (
		site_parts.hostname,
		site_parts.port,
	):
		return True
	site_path = site_parts.path.rstrip("/")
	if not site_path:
		return False
	is_within_site = href_parts.path == site_path or href_parts.path.startswith(
		f"{site_path}/"
	)
	return not is_within_site


#============================================
class ExternalLinksTreeprocessor(markdown.treeprocessors.Treeprocessor):
	"""Write external-link behavior into the generated website HTML tree."""

	def __init__(self, site_url: str) -> None:
		super().__init__()
		self.site_url = site_url

	def run(
		self,
		root: xml.etree.ElementTree.Element,
	) -> xml.etree.ElementTree.Element:
		"""Add new-tab attributes and one shared accessible description."""
		has_external_link = False
		for link in root.iter("a"):
			href = link.get("href")
			if href is None or not is_external_web_link(href, self.site_url):
				continue
			has_external_link = True
			# Set attributes on the parsed link before Markdown serializes the tree.
			link.set("target", "_blank")
			rel_tokens = link.get("rel", "").split()
			if "noopener" not in rel_tokens:
				rel_tokens.append("noopener")
			link.set("rel", " ".join(rel_tokens))
			description_ids = link.get("aria-describedby", "").split()
			if EXTERNAL_LINK_DESCRIPTION_ID not in description_ids:
				description_ids.append(EXTERNAL_LINK_DESCRIPTION_ID)
			link.set("aria-describedby", " ".join(description_ids))
		if not has_external_link:
			return root
		description_exists = any(
			element.get("id") == EXTERNAL_LINK_DESCRIPTION_ID
			for element in root.iter()
		)
		if description_exists:
			return root
		# Reuse one hidden description across every external link in the page content.
		description = xml.etree.ElementTree.SubElement(root, "span")
		description.set("id", EXTERNAL_LINK_DESCRIPTION_ID)
		description.set("class", "md-visually-hidden")
		description.text = EXTERNAL_LINK_DESCRIPTION
		return root


#============================================
class ExternalLinksExtension(markdown.extensions.Extension):
	"""Register the website-only external-link tree processor."""

	def __init__(self, site_url: str) -> None:
		super().__init__()
		self.site_url = site_url

	def extendMarkdown(self, md: markdown.Markdown) -> None:
		"""Run after link creation and attribute-list handling."""
		processor = ExternalLinksTreeprocessor(self.site_url)
		md.treeprocessors.register(processor, "external_links", 4)
