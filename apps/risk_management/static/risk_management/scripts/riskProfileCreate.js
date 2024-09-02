const profileCreateModal = document.querySelector('#profileCreateModal');
const profileCreateForm = profileCreateModal.querySelector('#profile-create-form');
const criteriaFormToggle = profileCreateForm.querySelector('#criteria-form-toggle');

addOnPostAndOnResponseFuncAttr(criteriaFormToggle, 'Please wait...');


/**
 * Creates a modal containing the given form element and title.
 * @param {HTMLFormElement} formElement - The form element to include in the modal.
 * @param {string} modalTitle - The title of the modal.
 * @returns {HTMLDivElement} The modal element.
 */
function createModalWithForm(formElement, modalTitle) {
    if (!(formElement instanceof HTMLFormElement)) {
        throw new Error('The provided element is not a valid HTMLFormElement');
    }

    // Clone the form element to avoid modifying the original
    const clonedFormElement = formElement.cloneNode(true);

    // Create the modal HTML structure
    const modalHTML = `
        <div class="modal fade" style="display: none;" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content" style="border-radius: 0;">
                    <div class="modal-header">
                        <h5 class="modal-title">${modalTitle}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    
                    <div class="modal-body">
                        ${clonedFormElement.outerHTML}
                    </div>
                    
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger light btn-sm" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Create a container div for the modal
    const container = document.createElement('div');
    container.innerHTML = modalHTML;
    
    // Return the modal element
    return container.firstElementChild; // Return the first child, which is the modal div
}


/**
 * Generates a <select> element from an object with key-value pairs.
 * @param {Object} data - The object with key-value pairs to convert into options.
 * @param {string} selectId - The ID to assign to the <select> element.
 * @returns {HTMLSelectElement} The HTML select element.
 */
function generateSelectFromObject(data) {
    const select = document.createElement('select');

    Object.keys(data).forEach(key => {
        const option = document.createElement('option');
        option.value = data[key];
        option.text = key;
        select.appendChild(option);
    });

    return select;
}


// Helper function to generate an optgroup for a given group of functions
function generateOptgroupElementFromFunctionGroupSchema(groupName, functionGroupSchema) {
    const optgroup = document.createElement('optgroup');
    optgroup.label = groupName;

    Object.keys(functionGroupSchema).forEach(functionName => {
        const functionSchema = functionGroupSchema[functionName];
        const option = document.createElement('option');

        option.value = functionName;
        option.text = functionSchema.name;

        if (functionSchema.description) {
            option.title = functionSchema.description;
        }

        // // Optional: Add a `required` attribute if there are required arguments (though not typical for <option>)
        // if (functionSchema.kwargs && functionSchema.kwargs.required_arguments.length > 0) {
        //     option.required = true;
        // }

        optgroup.appendChild(option);
    });

    return optgroup;
}


function generateSelectElementFromFunctionGroupsSchema(functionGroupsSchema) {
    const select = document.createElement('select');
    select.id = 'function-selector';

    Object.keys(functionGroupsSchema).forEach(groupName => {
        const functionGroupSchema = functionGroupsSchema[groupName];
        const optgroup = generateOptgroupElementFromFunctionGroupSchema(groupName, functionGroupSchema);
        select.appendChild(optgroup);
    });

    return select;
}


function wrapSelectElementinFormFieldElement(selectEl, fieldLabel) {
    const fieldLabelEl = document.createElement("label");
    fieldLabelEl.textContent = fieldLabel ?? "";
    fieldLabelEl.setAttribute("for", selectEl.id);

    const formFieldEl = document.createElement("div");
    formFieldEl.classList.add("form-field");

    formFieldEl.appendChild(fieldLabelEl);
    formFieldEl.appendChild(selectEl);

    return formFieldEl;
}


function generateCriteriaFormElementFromCriteriaFormSchema(criteriaFormSchema) {
    const operatorsSchema = criteriaFormSchema["operators"];
    const functionGroupsSchema = criteriaFormSchema["functions"];
    // Convert the operators and functions schema into <select> elements
    const operatorsSelectEl = generateSelectFromObject(operatorsSchema);
    const functionOneSelectEl = generateSelectElementFromFunctionGroupsSchema(functionGroupsSchema);
    const functionTwoSelectEl = generateSelectElementFromFunctionGroupsSchema(functionGroupsSchema);

    // Name and ID the select elements for form submission
    operatorsSelectEl.name = "op";
    operatorsSelectEl.id = "op";
    functionOneSelectEl.name = "func1";
    functionOneSelectEl.id = "func1";
    functionTwoSelectEl.name = "func2";
    functionTwoSelectEl.id = "func2";

    // Wrap the select elements in form fields
    const operatorsFormFieldEl = wrapSelectElementinFormFieldElement(operatorsSelectEl);
    const functionOneFormFieldEl = wrapSelectElementinFormFieldElement(functionOneSelectEl);
    const functionTwoFormFieldEl = wrapSelectElementinFormFieldElement(functionTwoSelectEl);

    // Create a wrapper div for the form fields
    const formFieldsWrapper = document.createElement("div");
    formFieldsWrapper.classList.add("form-fields");
    // Append the form fields to the wrapper div
    formFieldsWrapper.appendChild(functionOneFormFieldEl);
    formFieldsWrapper.appendChild(operatorsFormFieldEl);
    formFieldsWrapper.appendChild(functionTwoFormFieldEl);

    // Create a form element and append the form fields to it
    const form = document.createElement("form");
    form.id = "criteria-form";
    form.appendChild(formFieldsWrapper);

    return form;
}


function renderCriteriaForm(criteriaFormEl) {
    const modalBody = profileCreateModal.querySelector(".modal-body")
    modalBody.appendChild(criteriaFormEl);
}


criteriaFormToggle.addEventListener('click', (e) => {

    const criteriaCreationSchemaURL = criteriaFormToggle.dataset.criteriaCreationSchemaUrl ?? null;
    if (!criteriaCreationSchemaURL) return;

    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    }

    criteriaFormToggle.onPost();
    fetch(`${criteriaCreationSchemaURL}?grouped=true`, options).then((response) => {
        if (!response.ok) {
            criteriaFormToggle.onResponse();

            response.json().then((data) => {
                pushNotification("error", data.detail ?? data.message ?? 'An error occurred!');
            });

        } else {
            response.json().then((data) => {
                const criteriaCreationSchema = data.data;
                const criteriaFormEl = generateCriteriaFormElementFromCriteriaFormSchema(criteriaCreationSchema);
                renderCriteriaForm(criteriaFormEl);
            });
        }
    });

});
