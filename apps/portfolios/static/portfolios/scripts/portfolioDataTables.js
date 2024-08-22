const portfolioDataTabsSection = document.querySelector("#portfolio-data-tabs-section");

if (portfolioDataTabsSection) {
    const portfolioDataTableEl = portfolioDataTabsSection.querySelector("#portfolio-data-table");
    const stockProfilesDataTableEl = portfolioDataTabsSection.querySelector("#stock-profiles-data-table");
    const stockProfilesFilterURLParamName = "filter_sp_by";
    const stockProfilesFiltersWrapper = portfolioDataTabsSection.querySelector("#stock-profiles-filters-wp");


    if (stockProfilesFiltersWrapper) {
        const stockProfilesFilters = stockProfilesFiltersWrapper.querySelectorAll('.stock-profiles-filter');
        const activeFilterValue = stockProfilesFiltersWrapper.dataset.activefilter ?? "";

        stockProfilesFilters.forEach((filter) => {
            filter.onclick = function () {
                const filterValue = this.children[0].dataset.value;
                updateURLParams(stockProfilesFilterURLParamName, filterValue);
                window.location.reload();
            }

            if (activeFilterValue) {
                const filterValue = filter.children[0].dataset.value ?? "";
                if (filterValue.toLowerCase() == activeFilterValue.toLowerCase()) {
                    filter.classList.add("active")
                }
                else {
                    filter.classList.remove("active")
                }
            }
        });
    }

    if (portfolioDataTableEl) {
        // Portfolio datatable configuration
        const portfolioDataTable = new DataTable(portfolioDataTableEl, {
            dom: "Bfrtip",
            scrollX: false,
            paging: false,
            info: false,
            columnDefs: [{ targets: 'no-sort', orderable: false }]
        });
    }

    if (stockProfilesDataTableEl) {
        // Stock profiles datatable configuration
        const stockProfilesDataTable = new DataTable(stockProfilesDataTableEl, {
            dom: "Bfrtip",
            scrollX: false,
            paging: false,
            info: false,
            columnDefs: [
                { targets: 'no-sort', orderable: false }, 
            ]
        });
    }
}
