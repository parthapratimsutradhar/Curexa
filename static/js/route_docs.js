(function () {
    "use strict";

    const searchInput = document.getElementById("routeSearch");
    const searchClear = document.getElementById("searchClear");
    const resultsCount = document.getElementById("resultsCount");
    const noResults = document.getElementById("noResults");
    const resetFilters = document.getElementById("resetFilters");
    const filterChips = document.querySelectorAll(".filter-chip");
    const routeCards = document.querySelectorAll(".route-card");
    const categories = document.querySelectorAll(".route-category");
    const sidebarLinks = document.querySelectorAll(".sidebar-link");

    let activeFilter = "all";

    function updateResultsCount(visible) {
        const total = routeCards.length;
        if (visible === total) {
            resultsCount.textContent = `Showing all ${total} routes`;
        } else {
            resultsCount.textContent = `Showing ${visible} of ${total} routes`;
        }
    }

    function applyFilters() {
        const query = (searchInput?.value || "").trim().toLowerCase();
        let visibleCount = 0;

        categories.forEach((section) => {
            let sectionVisible = 0;
            const cards = section.querySelectorAll(".route-card");

            cards.forEach((card) => {
                const path = card.dataset.path || "";
                const name = card.dataset.name || "";
                const desc = card.dataset.desc || "";
                const type = card.dataset.type || "";

                const matchesSearch =
                    !query ||
                    path.includes(query) ||
                    name.includes(query) ||
                    desc.includes(query);

                const matchesFilter =
                    activeFilter === "all" ||
                    (activeFilter === "web" && type === "web") ||
                    (activeFilter === "api" && type === "api") ||
                    (activeFilter === "admin" && type === "admin") ||
                    (activeFilter === "doctor" && type === "doctor");

                const visible = matchesSearch && matchesFilter;
                card.classList.toggle("hidden", !visible);
                if (visible) {
                    visibleCount++;
                    sectionVisible++;
                }
            });

            section.classList.toggle("hidden", sectionVisible === 0);
        });

        if (noResults) {
            noResults.classList.toggle("d-none", visibleCount > 0);
        }
        updateResultsCount(visibleCount);

        if (searchClear) {
            searchClear.classList.toggle("visible", query.length > 0);
        }
    }

    function setActiveFilter(filter) {
        activeFilter = filter;
        filterChips.forEach((chip) => {
            chip.classList.toggle("active", chip.dataset.filter === filter);
        });
        applyFilters();
    }

    function copyToClipboard(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const original = button.innerHTML;
            button.classList.add("copied");
            button.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                button.classList.remove("copied");
                button.innerHTML = original;
            }, 1800);
        });
    }

    function highlightSidebarLink() {
        const scrollPos = window.scrollY + 200;
        let current = null;

        categories.forEach((section) => {
            if (section.offsetTop <= scrollPos && !section.classList.contains("hidden")) {
                current = section.id;
            }
        });

        sidebarLinks.forEach((link) => {
            const href = link.getAttribute("href");
            link.classList.toggle("active", href === "#" + current);
        });
    }

    searchInput?.addEventListener("input", applyFilters);

    searchClear?.addEventListener("click", () => {
        searchInput.value = "";
        applyFilters();
        searchInput.focus();
    });

    filterChips.forEach((chip) => {
        chip.addEventListener("click", () => setActiveFilter(chip.dataset.filter));
    });

    resetFilters?.addEventListener("click", () => {
        searchInput.value = "";
        setActiveFilter("all");
    });

    document.querySelectorAll(".copy-path").forEach((btn) => {
        btn.addEventListener("click", () => copyToClipboard(btn.dataset.path, btn));
    });

    sidebarLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute("href"));
            if (target) {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });

    window.addEventListener("scroll", highlightSidebarLink, { passive: true });

    applyFilters();
    highlightSidebarLink();
})();
