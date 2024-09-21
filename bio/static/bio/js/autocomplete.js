
// Fetch suggestions for celebrity name
function fetchSuggestions(query) {
    if (query.length > 2) {
        fetch(`/bio/autocomplete/?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const suggestionsDiv = document.getElementById('suggestions');
                suggestionsDiv.innerHTML = '';
                data.forEach(celebrity => {
                    const div = document.createElement('div');
                    div.innerHTML = celebrity.name;
                    div.onclick = function() {
                        document.getElementById('celebrity_name').value = celebrity.name;
                        suggestionsDiv.innerHTML = '';
                    };
                    suggestionsDiv.appendChild(div);
                });
            });
    }
}

// Form validation
function validateForm() {
    const nameInput = document.getElementById('celebrity_name');
    if (nameInput.value.trim() === '') {
        alert('Please enter a celebrity name.');
        return false;
    }
    showLoadingSpinner();
    return true;
}

// Show loading spinner
function showLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'block';
}
