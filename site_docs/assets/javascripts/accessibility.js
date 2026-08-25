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

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", updateScrollableTables);
} else {
	updateScrollableTables();
}

window.addEventListener("resize", updateScrollableTables);
