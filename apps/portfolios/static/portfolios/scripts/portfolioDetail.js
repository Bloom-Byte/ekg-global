const netBalanceCard = document.querySelector("#net-balance-card");
const netBalanceCardToggle = document.querySelector("#net-balance-card-toggle");
const portfolioDataTableEl = document.querySelector("#portfolio-data-table");
const stockProfilesDataTableEl = document.querySelector("#stock-profiles-data-table");


netBalanceCardToggle.onclick = function(e) {
    const toggleText = this.dataset.toggletext;
    const newToggleText = this.innerHTML;

    netBalanceCard.classList.toggle("show-block");
    netBalanceCardToggle.innerHTML = toggleText;
    netBalanceCardToggle.dataset.toggletext = newToggleText;
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
        columnDefs: [{ targets: 'no-sort', orderable: false }]
    });
}

