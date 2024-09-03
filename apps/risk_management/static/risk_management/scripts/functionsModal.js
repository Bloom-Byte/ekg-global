const functionsModal = document.querySelector("#functions-modal");
const functionsModalCloseBtn = functionsModal.querySelector("");
const optionsSearchInput = document.querySelector("#options-search-input");
const MainOptionSet = functionsModal.querySelector("#function-options.options");
const subOptionSets = functionsModal.querySelectorAll(".sub-options");
const allOptions = functionsModal.querySelectorAll(".option");

/**
 * Returns the visible element with the highest z-index from a given list of elements.
 *
 * @param {HTMLElement[]} elements - An array or NodeList of HTML elements to check.
 * @returns {HTMLElement|null} - The visible element with the highest z-index. Returns null if no visible element has a valid z-index.
 *
 * @example
 * const elements = document.querySelectorAll('.some-class');
 * const highestVisibleElement = getElementWithHighestZIndex(elements);
 * if (highestVisibleElement) {
 *     console.log('Visible element with highest z-index:', highestVisibleElement, 'with z-index:', window.getComputedStyle(highestVisibleElement).zIndex);
 * } else {
 *     console.log('No visible element with a valid z-index found.');
 * }
 */
function getVisibleElementWithHighestZIndex(elements) {
    let highestVisibleElement = null;
    let highestZIndex = -Infinity;
    const elementArray = Array.isArray(elements) ? elements : Array.from(elements);

    // Filter elements array down to those that are visible
    const visibleElements = elementArray.filter((element) => {
        if (!element) return false;

        const style = window.getComputedStyle(element);
        const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        return isVisible
    })

    visibleElements.forEach(element => {
        const style = window.getComputedStyle(element);
        let zIndex = parseInt(style.zIndex, 10);
        if (isNaN(zIndex)) {
            zIndex = 0;
        }

        // Check if zIndex is greater than the highest z-index
        if (zIndex >= highestZIndex) {
            highestZIndex = zIndex;
            highestVisibleElement = element;
        }
    });

    return highestVisibleElement;
}


// Function to handle search functionality
optionsSearchInput.addEventListener('input', function () {
    const filter = this.value.toLowerCase();
    const OptionSets = [MainOptionSet, ...subOptionSets]
    const targetOptionSet = getVisibleElementWithHighestZIndex(OptionSets);

    targetOptionSet.querySelectorAll('.option').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? '' : 'none';
    });
});


allOptions.forEach(option => {
    const optionLabel = option.querySelector(".option-label");
    const subOptionSet = option.querySelector(".sub-options");
    if (!subOptionSet) return;

    optionLabel.addEventListener("click", () => {
        subOptionSet.style.display = "flex";
        const subOptionBackArrow = subOptionSet.querySelector(".sub-options-head > .arrow");

        subOptionBackArrow.addEventListener("click", () => {
            subOptionSet.style.display = "none";
        });
    });
});

