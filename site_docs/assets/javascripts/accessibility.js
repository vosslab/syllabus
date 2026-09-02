function updateScrollableTables() {
	const tableContainers = document.querySelectorAll(".md-typeset__table");
	tableContainers.forEach((container) => {
		if (container.scrollWidth <= container.clientWidth) {
			container.removeAttribute("aria-label");
			container.removeAttribute("role");
			container.removeAttribute("tabindex");
			return;
		}
		const firstHeader = container.querySelector("th");
		const headerText = firstHeader?.textContent?.trim();
		const label = headerText ? `Scrollable table: ${headerText}` : "Scrollable course table";
		container.setAttribute("aria-label", label);
		container.setAttribute("role", "region");
		container.setAttribute("tabindex", "0");
	});
}

function getExternalLinkDescriptionId() {
	const descriptionId = "external-link-new-tab-description";
	if (document.getElementById(descriptionId)) {
		return descriptionId;
	}
	// ASVS 3.7.3: announce off-site navigation before the link is activated.
	const description = document.createElement("span");
	description.id = descriptionId;
	description.classList.add("md-visually-hidden");
	description.textContent = "Opens in a new tab.";
	document.body.append(description);
	return descriptionId;
}

function updateExternalLinks() {
	const links = document.querySelectorAll("a[href]");
	let descriptionId = "";
	links.forEach((link) => {
		const isWebLink = link.protocol === "http:" || link.protocol === "https:";
		if (!isWebLink || link.origin === window.location.origin) {
			return;
		}
		link.target = "_blank";
		link.relList.add("noopener");
		if (!descriptionId) {
			descriptionId = getExternalLinkDescriptionId();
		}
		const describedBy = new Set(
			(link.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean),
		);
		describedBy.add(descriptionId);
		link.setAttribute("aria-describedby", [...describedBy].join(" "));
	});
}

function initializeAccessibilityEnhancements() {
	updateScrollableTables();
	updateExternalLinks();
}

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", initializeAccessibilityEnhancements);
} else {
	initializeAccessibilityEnhancements();
}

window.addEventListener("resize", updateScrollableTables);
