var BACKEND_URL = 'https://aitarot.azurewebsites.net/';
// const backendUrl = BACKEND_URL || 'http://127.0.0.1:5000';
// const backendUrl = 'http://127.0.0.1:5000';
const backendUrl = BACKEND_URL;

console.log(BACKEND_URL);

const formConfig = [
    {
        question: "Select a aspect",
        options: ["Romanticships", "Studying", "Business", "Fortune", "Health", "Family"]
    }
];

const answers = {};
puzzles={};
draft_story="";
final_story="";
retry=0;
function generateForm() {
    const formContainer = document.getElementById('form');
    formConfig.forEach((section, index) => {
        sectionDiv = document.createElement('div');
        sectionDiv.id = `section${index + 1}`;
        sectionDiv.className = 'form-container';
        
        if (index !== 0) {
            sectionDiv.style.display = 'none';
        }
        
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row align-items-center';

        const buttonGroupCol = document.createElement('div');
        buttonGroupCol.className = 'col-8';

        questionDiv = document.createElement('div');
        questionDiv.className = 'question fs-4';
        questionDiv.textContent = section.question;
        sectionDiv.appendChild(questionDiv);
        
        buttonGroup = document.createElement('div');
        buttonGroup.className = 'button-group';
        section.options.forEach(option => {
            const button = document.createElement('button');
            button.textContent = option;
            button.className = 'button';
            button.onclick = () => selectAnswer(index + 1, option);
            buttonGroup.appendChild(button);
        });

        buttonGroupCol.appendChild(buttonGroup);
        
        const regenerateButtonCol = document.createElement('div');
        regenerateButtonCol.className = 'col-4 text-end';

        const regenerateButton = document.createElement('button');
        regenerateButton.textContent = 'Regenerate';
        regenerateButton.className = 'btn btn-outline-primary me-md-2';
        regenerateButton.onclick = () => regenerateOptions(index + 1);
        regenerateButtonCol.appendChild(regenerateButton);

        rowDiv.appendChild(buttonGroupCol);
        rowDiv.appendChild(regenerateButtonCol);

        sectionDiv.appendChild(rowDiv);

        formContainer.appendChild(sectionDiv);
    });
    const generateButtonDiv = document.getElementById("generate-button")
    const submitButton = document.createElement('button');
    submitButton.className = 'submit-button';
    submitButton.id="submit-button";
    submitButton.textContent = 'Generate';
    submitButton.style.display = 'none';
    submitButton.onclick = submitForm;
    generateButtonDiv.appendChild(submitButton);
}


function selectAnswer(section, answer) {
    answers['section' + section] = answer;
    const currentSection = document.getElementById('section' + section);
    currentSection.classList.add('active');
    updateButtonSelection(section, answer);
    
    const nextSection = document.getElementById('section' + (section + 1));
    if (nextSection) {
        nextSection.style.removeProperty('display');
    } else {
        document.getElementById("submit-button").style.display = 'block';
    }
}

function validateInput(section, input) {
    if (input.trim() !== '') {
        selectAnswer(section, input);
        return true;
    }
    return false;
}

function updateButtonSelection(section, answer) {
    const buttons = document.querySelectorAll(`#section${section} .button-group button`);
    buttons.forEach(button => {
        if (button.textContent === answer) {
            button.classList.add('selected');
        } else {
            button.classList.remove('selected');
        }
    });
}

function regenerateOptions(section) {
    const typeMapping = {
        1: 'aspect',
    };
    const type = typeMapping[section];

    fetch(`${backendUrl}/get_options?type=${type}`)
        .then(response => response.json())
        .then(data => {
            let options = data[`options`];
            console.log(options);
            // Check if options is a string and try to parse it
            if (typeof options === 'string') {
                try {
                    options = JSON.parse(options);
                } catch (e) {
                    console.error('Error parsing options:', e);
                    return;
                }
            }

            if (Array.isArray(options)) {
                const buttonGroup = document.querySelector(`#section${section} .button-group`);
                buttonGroup.innerHTML = ''; // Clear existing options

                options.forEach(option => {
                    const button = document.createElement('button');
                    button.textContent = option;
                    button.onclick = () => selectAnswer(section, option);
                    buttonGroup.appendChild(button);
                });
            } else {
                console.error('Error: options is not an array');
            }
        })
        .catch(error => console.error('Error:', error));
}

async function submitForm() {
    console.log(JSON.stringify(answers));
    
    const responseDiv = document.getElementById('response');
    responseDiv.style.removeProperty('display');
    responseDiv.innerHTML = 'Loading...';

    try {
        const response = await fetch(`${backendUrl}/generate_draft_story`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(answers)
        });
        const data = await response.json();
        responseDiv.innerHTML = "";
        storyTitleDiv = document.createElement('div');
        storyTitleDiv.className = 'question fs-4';
        storyTitleDiv.textContent = "Tarot shows...";
        responseDiv.appendChild(storyTitleDiv);

        storyDiv = document.createElement('div');
        storyDiv.className = 'text-start';
        storyDiv.textContent = data.answer;
        responseDiv.appendChild(storyDiv);

        draft_story=data.answer;
    } catch (error) {
        responseDiv.innerHTML = 'Error: ' + error.message;
    }
}

document.addEventListener('DOMContentLoaded', generateForm);