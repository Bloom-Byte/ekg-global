const tabToggles = document.querySelectorAll('.tab-toggle');


tabToggles.forEach((toggle, index) => {

    toggle.addEventListener('click', () => {
        const tabDataUrl = toggle.dataset.tabDataUrl;

        // Get the tab corresponding to the toggle's index
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

        fetch(tabDataUrl, options).then((response) => {
            if (!response.ok) {
                response.json().then((data) => {
                    pushNotification("error", data.detail ?? data.message ?? 'An error occurred!');
                });
    
            }else{
                response.json().then((data) => {    
                    const tabData = data.data ?? null;
                    console.log(tabData);
                    
                    var table = new Tabulator(tabTable, {
                        data:tabData,
                        autoColumns:true,
                    });
                });
            }
        });
    });
});
