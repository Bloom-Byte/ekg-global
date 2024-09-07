const profileTabToggles = document.querySelectorAll('.tab-toggle');
const profileTabDataReloaders = document.querySelectorAll('.tab-data-reloader');


function truthyFormatter(cell, formatterParams, onRendered){
    let value = cell.getValue();
    if(value) {
        cell.getElement().classList.add("text-success");
    } else {
        cell.getElement().classList.add("text-danger");
    }
    return value;
}


function heatMapFormatter(cell, formatterParams, onRendered){
    let value = cell.getValue();
    let intensity = (parseInt(value, 10) / 100) * 255; // assuming the value is out of 100
    let color = `rgb(${255 - intensity}, ${intensity}, 0)`; // transitions from red to green

    cell.getElement().style.backgroundColor = `${color} !important`;
    cell.getElement().style.color = "#fff"; // set text color to white for readability
    return `${value} %`;
}


function columnDefinitionsHandler(definitions) {
    definitions.forEach((column, index) => {
        // Freeze the first two columns
        if (index in [0, 1]) {
            column.frozen = true;
        }
        // For cell 3 to the second to the last cell, add a class to the cell based on the value
        // If the value of the cell is truthy, add a class of text-success, else add a class of text-danger
        else if (index < definitions.length - 1) {
            column.formatter = truthyFormatter;
        }
        // For the last cell, set the background color of the cell based on the value
        else if (index === definitions.length - 1) {
            column.formatter = heatMapFormatter;
        }
        column.title = column.title.toUpperCase();
    });
    return definitions;
}


function buildTable(tableData, tableElement) {
    var table = new Tabulator(tableElement, {
        data:tableData,
        autoColumns:true,
        autoColumnsDefinitions: columnDefinitionsHandler,
        autoResize: true,
        resizableColumnFit: true,
        pagination: "local",
        paginationSize: 20,
        paginationSizeSelector: [10, 20, 30, 40, 50],
        movableColumns: true,
        paginationCounter: "rows",
        // layout: "fitColumns",
        layoutColumnsOnNewData: true,
    });

    // Sort the table by descending order of the last column
    // PS: The last column is the ranking of each stock
    table.on("tableBuilt", function(){
        // Get the column definitions
        let columns = table.getColumns();
        
        // Get the field name of the last column
        let lastColumnField = columns[columns.length - 1].getField();
        
        // Apply sorting to the last column
        table.setSort(lastColumnField, "desc");
    });
    return table;
};


profileTabDataReloaders.forEach((reloader, index) => {

    reloader.addEventListener('click', () => {
        const tabDataUrl = reloader.dataset.tabDataUrl;

        // Get the tab corresponding to the reloader's index
        const tab = document.querySelectorAll('.tabs-section .tab')[index];
        const tabTable = tab.querySelector('.risk-profile-table');
        
        if (!tabDataUrl) return;

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            mode: 'same-origin',
            body: JSON.stringify({}),
        }

        // Add the spin class to the reloader and disable it
        reloader.classList.add("spin", "disabled");
        fetch(tabDataUrl, options).then((response) => {
            // On response, remove the spin class and enable the reloader
            reloader.classList.remove("spin", "disabled");
            
            if (!response.ok) {
                response.json().then((data) => {
                    pushNotification("error", data.detail ?? data.message ?? 'An error occurred!');
                });
    
            }else{
                response.json().then((data) => {    
                    const tabData = data.data ?? null;
                    if (!tabData) return;
                    buildTable(tabData, tabTable);
                });       
            }
        });
    });
});


profileTabToggles.forEach((toggle, index) => {
    toggle.addEventListener('click', () => {
        const tab = document.querySelectorAll('.tabs-section .tab')[index];
        const profileTable = tab.querySelector('.risk-profile-table');
        const profileTabDataReloader = tab.querySelector('.tab-data-reloader');

        // If the table element contains a tabulator js table element, it means the table has been rendered
        const tableHasBeenRendered = profileTable.querySelector(".tabulator-table") !== null;
        // If it does not, click on the tab data reloader to fetch and render table data
        if (!tableHasBeenRendered) {
            profileTabDataReloader.click();
        }
    });
});
