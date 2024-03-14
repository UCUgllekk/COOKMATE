var selected_ingredients = []
// Add an event listener for the 'submit' event to the form
document.getElementById('search-form').addEventListener('submit', function(event) {
    // Prevent the form from being submitted and the page from reloading
    event.preventDefault();

    // Get all the suggestions
    var suggestionsDiv = document.getElementById('suggestions');
    var suggestions = Array.from(suggestionsDiv.getElementsByTagName('div'));

    // If there are any suggestions
    if (suggestions.length > 0) {
        // Find the shortest suggestion
        var shortestSuggestion = suggestions.reduce(function(prev, curr) {
            return prev.textContent.length < curr.textContent.length ? prev : curr;
        });

        // Set the value of the search bar to the shortest suggestion
        var searchBar = document.getElementById('search-bar');
        searchBar.value = shortestSuggestion.textContent;

        // Get all the currently selected ingredients
        var selectedIngredients = Array.from(document.getElementById('selected-ingredients').getElementsByTagName('div'));
        console.log(shortestSuggestion.textContent)
        // Check if the selected ingredient is already in the list of selected ingredients
        var alreadySelected = selectedIngredients.some(function(ingredientDiv) {
            return ingredientDiv.textContent === shortestSuggestion.textContent;
        });

        // If the ingredient is not already selected
        if (!alreadySelected) {
            // Create a new div for the selected ingredient
            var ingredientDiv = document.createElement('div');
            ingredientDiv.textContent = shortestSuggestion.textContent;
            ingredientDiv.classList.add("tag");
            selected_ingredients.push(shortestSuggestion.textContent);
            console.log(selected_ingredients);
            // Add the new div to the list of selected ingredients
            document.getElementById('selected-ingredients').appendChild(ingredientDiv);
        }
    };
    document.getElementById('search-bar').value = "";
    document.getElementById('suggestions').innerHTML = "";
});

// Add an event listener for the 'input' event to the search bar
document.getElementById('search-bar').addEventListener('input', function() {
    // Get the current value of the search bar
    var inputVal = this.value.toLowerCase();
    var suggestionsDiv = document.getElementById('suggestions');

    // If the search bar is not empty
    if (inputVal) {
        // Create a new XMLHttpRequest
        var xhr = new XMLHttpRequest();

        // Open a GET request to the '/search' route with the current value of the search bar as a query parameter
        xhr.open('GET', '/search?query=' + inputVal, true);

        // Set the onload function of the XMLHttpRequest
        xhr.onload = function() {
            // Parse the response text as JSON
            var suggestions = JSON.parse(this.responseText);

            // Clear the suggestions div
            suggestionsDiv.innerHTML = '';
            // For each suggestion
            suggestions.slice(0, 5).forEach(function(suggestion) {
                // Create a new p element
                var p = document.createElement('div');

                // Set the text content of the p element to the suggestion
                p.textContent = suggestion;
                p.classList.add("option")

                // Add the p element to the suggestions div
                suggestionsDiv.appendChild(p);
            });
        };

        // Send the XMLHttpRequest
        xhr.send();
    } else {
        // If the search bar is empty, clear the suggestions div
        suggestionsDiv.innerHTML = '';
    }
});

document.getElementById('find_meal_button').addEventListener('click', function() {
    fetch('/store_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(selected_ingredients),
    })
    console.log(selected_ingredients)
    .then(response => {
        if (response.ok) {
            window.location.href = '/tinder';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

