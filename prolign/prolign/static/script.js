// Control height of textarea dynamically
const textArea = document.querySelector("textarea")
textArea.addEventListener("keyup", e => {
    textArea.style.minHeight = '15vh';
    let scHeight = e.target.scrollHeight;
    textArea.style.height = scHeight + "px";
});

// Display window length slider value dynamically
let windowLengthSlider = document.getElementById("window-length-range-slider")
let windowLengthSliderValue = document.getElementById("window-slider-range-default-value")
windowLengthSliderValue.textContent = windowLengthSlider.value // Required to display correct value after submission
windowLengthSlider.oninput = function (){
    windowLengthSliderValue.textContent = this.value
}

// Display edge weight slider value dynamically
let edgeWeightSlider = document.getElementById("edge-weight-range-slider")
let edgeWeightSliderValue = document.getElementById("edge-weight-slider-range-default-value")
edgeWeightSliderValue.textContent = edgeWeightSlider.value
edgeWeightSlider.oninput = function (){
    edgeWeightSliderValue.textContent = this.value
}

// Render error messages
let errorMessage = document.querySelector(".error-message") // Selecting First Error Message
if (errorMessage) {
    errorMessage.scrollIntoView({behavior: "smooth"})
    let inputTextArea = document.querySelector(".input-textarea-area")
    inputTextArea.style.borderColor = "#F8A5AF"
}

// Handle geometric progression edge case
function getSelectedValue() {
    let selectElement = document.querySelector(".model-select-box-element")
    let selectedValue = selectElement.value;
    let edgeWeightMinValue = document.querySelector(".edge-weight-slider-range-min-value")
    let edgeWeightSlider = document.querySelector("#edge-weight-range-slider")
    if (selectedValue === "Geometric Progression") {
        console.log(edgeWeightSlider.ariaValueMin)
        edgeWeightSlider.min = "0.1"
        edgeWeightMinValue.textContent = "0.1"
    }
    else {
        edgeWeightSlider.min = "0"
        edgeWeightMinValue.textContent = "0"
    }
    console.log(selectedValue);
}

// Scroll to plot after submission
window.onload = function() {
    let graphSection = document.getElementById('align-string');
    if (graphSection){
        graphSection.scrollIntoView({behavior: 'smooth'});
    }
};