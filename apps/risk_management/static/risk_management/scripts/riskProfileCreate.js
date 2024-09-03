const profileCreateModal = document.querySelector('#profileCreateModal');
const profileCreateForm = profileCreateModal.querySelector('#profile-create-form');
const criteriaCreationSectionToggle = profileCreateForm.querySelector('#criteria-creation-section-toggle');
const criteriaCreationSection = profileCreateForm.querySelector("#criteria-creation-section");
const criteriaCreationFields = criteriaCreationSection.querySelector("#criteria-creation-fields");
const functionInputs = criteriaCreationFields.querySelectorAll("input.function-input");


criteriaCreationSectionToggle.addEventListener("click", () => {    
    criteriaCreationSection.classList.toggle("show-block");
});


functionInputs.forEach((input) => {
    input.addEventListener("click", () => {
        functionsModal.classList.toggle("show-flex");
    });
});
