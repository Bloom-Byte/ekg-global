const profileCreateModal = document.querySelector('#profileCreateModal');
const profileCreateForm = profileCreateModal.querySelector('#profile-create-form');
const criteriaCreationSectionToggle = profileCreateForm.querySelector('#criteria-creation-section-toggle');
const criteriaCreationSection = profileCreateForm.querySelector("#criteria-creation-section");
const criteriaCreationFieldContainer = criteriaCreationSection.querySelector("#criteria-creation-fields");
const criteriaCreationFormFields = criteriaCreationFieldContainer.querySelector(".form-fields");
const functionInputs = criteriaCreationFormFields.querySelectorAll("input.function-input");
const criteriaAddButton = criteriaCreationFieldContainer.querySelector(".add-btn");


function resetFormFields(formFieldsContainer) {
    const formInputs = formFieldsContainer.querySelectorAll(".form-input");

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
                "options": JSON.parse(options),
            }
        }
        else {
            data[input.name] = input.value
        }
    });

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


criteriaAddButton.addEventListener("click", () => {
    const formInputs = criteriaCreationSection.querySelectorAll("#criteria-creation-fields > .form-fields > .form-field > .form-input");
    const criteriaData = getCriteriaCreationFormInputsData(formInputs);
    
    criteriaCreationSection.classList.remove("show-block");
    resetFormFields(criteriaCreationFormFields);
});
