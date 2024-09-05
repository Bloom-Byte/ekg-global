const tabToggles = document.querySelectorAll('.tab-toggle');


tabToggles.forEach((toggle) => {

    toggle.addEventListener('click', () => {
        const tabDataUrl = toggle.dataset.tabDataUrl;
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
                });
            }
        });
    });
});
