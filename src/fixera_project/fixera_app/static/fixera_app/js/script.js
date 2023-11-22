function handleBugCreation(event) {
    event.preventDefault();

    const form = event.target;
    const data = new FormData(this);
    const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;

    fetch('/api/bugs/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: data,
    })
    .then(response => response.json())
    .then(bug => {
        updateBugList(bug);
        form.reset();
    })
    .catch(error => console.error('Error creating bug: ', error));
}

function updateBugList(new_bug) {
    const listItem = document.createElement('li');

    const heading = document.createElement('h2');
    heading.textContent = new_bug.title;
    listItem.appendChild(heading);
    
    const paragraph1 = document.createElement('p');
    paragraph1.textContent = new_bug.description;
    listItem.appendChild(paragraph1);
    
    const paragraph2 = document.createElement('p');
    paragraph2.textContent = new_bug.created_at;
    listItem.appendChild(paragraph2);

    const bugList = document.getElementById('bug-list');
    bugList.append(listItem);


}

function initApp() {
    document.getElementById('bug-form').addEventListener('submit', handleBugCreation)
}

document.addEventListener('DOMContentLoaded', initApp);