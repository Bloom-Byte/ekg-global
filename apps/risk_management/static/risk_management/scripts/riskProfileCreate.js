const profileCreateModal = document.querySelector('#profileCreateModal');
const profileCreateForm = profileCreateModal.querySelector('#profile-create-form');
const profileCreateButton = profileCreateForm.querySelector('.submit-btn');
const selectedCriteriaContainer = profileCreateModal.querySelector('#criteria-selected');

// Criteria Creation Section
const criteriaCreationSectionToggle = profileCreateForm.querySelector('#criteria-creation-section-toggle');
const criteriaCreationSection = profileCreateForm.querySelector("#criteria-creation-section");
const criteriaCreationFieldContainer = criteriaCreationSection.querySelector("#criteria-creation-fields");
const criteriaCreationFormFields = criteriaCreationFieldContainer.querySelector(".form-fields");
const criteriaCreationFormInputs = criteriaCreationSection.querySelectorAll("#criteria-creation-fields > .form-fields > .form-field > .form-input");
const functionInputs = criteriaCreationFormFields.querySelectorAll("input.function-input");
const criteriaAddButton = criteriaCreationFieldContainer.querySelector(".add-btn");


/**
 * Resets the values of the given form inputs
 * @param {HTMLElement} formInputs 
 */
function resetFormInputs(formInputs) {
    formInputs.forEach(formInput => {
        formInput.value = null;
    });
}


function getCriteriaCreationFormInputsData(formInputs) {
    const data = {}

    formInputs.forEach(input => {
        const options = input.dataset.options ?? null;
        if (options) {
            data[input.name] = {
                "name": input.value,
                "kwargs": JSON.parse(options),
            }
        }
        else {
            data[input.name] = input.value
        }
    });

    return data;
}


/**
 * Makes an HTMLElement holding the criteria data
 * @param {Object} criteriaData
 * @returns {HTMLButtonElement}
 */
function makeCriteriaElement(criteriaData) {
    const criteriaEl = document.createElement("button");
    criteriaEl.type = "button";
    criteriaEl.dataset.data = JSON.stringify(criteriaData);
    criteriaEl.classList.add("btn", "btn-outline-primary", "btn-xs", "criteria");

    const criteriaName = `${criteriaData.func1.name} ${criteriaData.op} ${criteriaData.func2.name}`;
    criteriaEl.innerHTML = `
        ${criteriaName}
        <i class="fas fa-times fa-xs"></i>
    `

    criteriaEl.addEventListener("click", () => {
        criteriaEl.remove();
    });

    return criteriaEl;
}


function getSelectedCriteriaData() {
    const selectedCriteria = selectedCriteriaContainer.querySelectorAll(".criteria");
    console.log(selectedCriteria)
    const data = []

    selectedCriteria.forEach(criteria => {
        const criteriaData = criteria.dataset.data ?? null;
        if (!criteriaData) return;

        data.push(JSON.parse(criteriaData));
    });

    return data;
}


function getPortfolioCreationFormData() {
    const data = {}
    const topLevelFormInputs = document.querySelectorAll("#profile-create-form > .form-fields > .form-field > .form-input");

    topLevelFormInputs.forEach(input => {
        data[input.name] = input.value
    });
    data["criteria"] = getSelectedCriteriaData();

    return data;
}


function captureFunctionSelection(functionsModal, inputField) {
    const options = functionsModal.querySelectorAll(".option");

    options.forEach(option => {
        const optionSubOptions = option.querySelector(".sub-options");

        if (!optionSubOptions) {
            option.addEventListener("click", () => {
                const functionName = option.dataset.function ?? null;
                if (!functionName) return;

                inputField.value = functionName;
                inputField.dataset.options = null;

                functionsModal.close();
            });
            return;
        };

        const doneBtns = functionsModal.querySelectorAll(".done-btn");
        doneBtns.forEach(doneBtn => {
            doneBtn.addEventListener("click", () => {
                const parentFormFieldContainer = doneBtn.closest(".form-fields");
                const formFieldsData = getSubOptionFormFieldsData(parentFormFieldContainer);

                inputField.value = formFieldsData.name;
                inputField.dataset.options = JSON.stringify(formFieldsData.options);

                functionsModal.close();
            });
        });
    });
};


selectedCriteriaContainer.addCriteria = (criteriaData) => {
    const criteriaEl = makeCriteriaElement(criteriaData);
    selectedCriteriaContainer.appendChild(criteriaEl);
}

criteriaCreationSectionToggle.addEventListener("click", () => {
    criteriaCreationSection.classList.toggle("show-block");
});


functionInputs.forEach((input) => {
    input.addEventListener("click", () => {
        const functionsModal = input.parentElement.querySelector(".functions-modal");
        if (!functionsModal) return;

        functionsModal.open();
        captureFunctionSelection(functionsModal, input);
    });
});


criteriaCreationFieldContainer.addEventListener("pointerover", () => {
    const allFieldsHaveValues = Array.from(criteriaCreationFormInputs).every((input) => {
        if (!input.value){
            return false
        }
        return true
    })

    if (allFieldsHaveValues){
        criteriaAddButton.disabled = false;
    }else {
        criteriaAddButton.disabled = true;
    }
});


criteriaAddButton.addEventListener("click", () => {
    const criteriaData = getCriteriaCreationFormInputsData(criteriaCreationFormInputs);
    selectedCriteriaContainer.addCriteria(criteriaData);
    
    criteriaCreationSection.classList.remove("show-block");
    resetFormInputs(criteriaCreationFormInputs);
});


addOnPostAndOnResponseFuncAttr(profileCreateButton, 'Processing...');

profileCreateForm.onsubmit = function(e) {
    e.stopImmediatePropagation();
    e.preventDefault();

    const data = getPortfolioCreationFormData();
    const criteria = data.criteria;
    if (!criteria.length) {
        pushNotification("error", "At least one criteria is required!");
        return;
    }

    profileCreateButton.onPost();
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        mode: 'same-origin',
        body: JSON.stringify(data),
    }

    fetch(this.action, options).then((response) => {
        if (!response.ok) {
            profileCreateButton.onResponse();
            response.json().then((data) => {
                const errors = data.errors ?? null;
                if (errors){
                    console.log(errors)
                    if(!typeof errors === Object) throw new TypeError("Invalid data type for 'errors'")

                    for (const [fieldName, msg] of Object.entries(errors)){
                        if (fieldName == "__all__"){
                            if (typeof msg === Array){
                                msg.forEach((m) => {
                                    pushNotification("error", m);
                                });
                            }else{
                                pushNotification("error", msg);
                            };
                        };
                        
                        let field = this.querySelector(`*[name=${fieldName}]`);
                        if (!field) return;
                        field.scrollIntoView({"block": "center"});
                        formFieldHasError(field.parentElement, msg);
                    };

                }else{
                    pushNotification("error", data.detail ?? data.message ?? 'An error occurred!');
                };
            });

        }else{
            profileCreateButton.onResponse();
            profileCreateButton.disabled = true;

            response.json().then((data) => {
                pushNotification("success", data.detail ?? data.message ?? 'Request successful!');

                const redirectURL  = data.redirect_url ?? null
                if(!redirectURL) return;

                setTimeout(() => {
                    window.location.href = redirectURL;
                }, 2000);
            });
        }
    });
};

