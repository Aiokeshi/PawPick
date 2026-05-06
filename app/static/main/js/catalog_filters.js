document.addEventListener('DOMContentLoaded', function () {
    const filterButton = document.querySelector('[data-filter-button]');
    const filterPanel = document.querySelector('[data-filter-panel]');
    const filterOverlay = document.querySelector('[data-filter-overlay]');

    function closeFilters() {
        if (!filterButton || !filterPanel || !filterOverlay) {
            return;
        }

        filterButton.classList.remove('is-open');
        filterPanel.classList.remove('is-open');
        filterOverlay.classList.remove('is-open');
        filterButton.setAttribute('aria-expanded', 'false');
        filterButton.setAttribute('aria-label', 'Открыть фильтры');
        document.body.classList.remove('filters-open');
    }

    function openFilters() {
        if (!filterButton || !filterPanel || !filterOverlay) {
            return;
        }

        filterButton.classList.add('is-open');
        filterPanel.classList.add('is-open');
        filterOverlay.classList.add('is-open');
        filterButton.setAttribute('aria-expanded', 'true');
        filterButton.setAttribute('aria-label', 'Закрыть фильтры');
        document.body.classList.add('filters-open');
    }

    if (filterButton && filterPanel && filterOverlay) {
        filterButton.addEventListener('click', function () {
            if (filterPanel.classList.contains('is-open')) {
                closeFilters();
            } else {
                openFilters();
            }
        });

        filterOverlay.addEventListener('click', closeFilters);

        const filterForm = filterPanel.querySelector('form');
        if (filterForm) {
            filterForm.addEventListener('submit', closeFilters);
        }
    }

    document.querySelectorAll('[data-filter-group]').forEach(function (group) {
        const toggle = group.querySelector('[data-filter-toggle]');
        const options = group.querySelector('[data-filter-options]');

        if (!toggle || !options) {
            return;
        }

        const hasCheckedInput = Boolean(group.querySelector('input[type="checkbox"]:checked'));

        if (hasCheckedInput) {
            group.classList.add('is-open');
            toggle.setAttribute('aria-expanded', 'true');
        }

        toggle.addEventListener('click', function () {
            const isOpen = group.classList.toggle('is-open');
            toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeFilters();
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 767) {
            closeFilters();
        }
    });
});
