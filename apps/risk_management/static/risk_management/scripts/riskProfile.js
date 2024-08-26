const riskProfileTableEl = document.querySelector("#risk-profile-table");

if (riskProfileTableEl){
    const riskProfileTable = new DataTable(riskProfileTableEl, {
        dom: "frtip",
        scrollX: false,
        searchable: true,
        sortable: true,
        paging: false,
        info: false,
        columnDefs: [{ targets: 'no-sort', orderable: false }]
    });

}
