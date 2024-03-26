var selected_ingredients = []
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var suggestionsDiv = document.getElementById('suggestions');
    var suggestions = Array.from(suggestionsDiv.getElementsByTagName('button'));
    if (suggestions.length > 0 && suggestions[0].classList.contains("option")) {
        var shortestSuggestion = suggestions[0];
        var searchBar = document.getElementById('search-bar');
        var alreadySelected = selected_ingredients.some(function(ingredient) {
            return ingredient === shortestSuggestion.textContent;
        });
        if (!alreadySelected) {
            var ingredientDiv = document.createElement('div');
            ingredientDiv.textContent = shortestSuggestion.textContent;
            ingredientDiv.classList.add("tag");
            selected_ingredients.push(shortestSuggestion.textContent);
            console.log(selected_ingredients);
            document.getElementById('selected-ingredients').appendChild(ingredientDiv);
        }
    };
    searchBar.value = "";
    searchBar.focus()
    suggestionsDiv.innerHTML = "";
});

document.addEventListener('click', function(event) {
    if (event.target.id == "search-form" || event.target.classList.contains("search-icon")) {
        document.getElementById('search-bar').focus()
    }
    if (event.target.classList.contains('option')) {

        var suggestion = event.target.innerText;
        var searchBar = document.getElementById('search-bar');

        if (suggestion.length > 0) {
            var alreadySelected = selected_ingredients.some(function(ingredient) {
                return ingredient === suggestion;
            });

            if (!alreadySelected) {
                var ingredientDiv = document.createElement('div');
                ingredientDiv.textContent = suggestion;
                ingredientDiv.classList.add("tag");
                selected_ingredients.push(suggestion);
                document.getElementById('selected-ingredients').appendChild(ingredientDiv);
            }
        };
        searchBar.value = "";
        event.target.parentNode.innerHTML = "";
        searchBar.focus();
    }
});

function isAlphaSpace(text){
    return /^[A-Z ]*$/i.test(text);
}

document.getElementById('search-bar').addEventListener('input', function() {
    var inputVal = this.value.toLowerCase();
    var suggestionsDiv = document.getElementById('suggestions');
    if (inputVal) {
        if (isAlphaSpace(inputVal)) {
            var xhr = new XMLHttpRequest();

            xhr.open('GET', '/search?query=' + inputVal, true);

            xhr.onload = function() {
                var suggestions = JSON.parse(this.responseText);

                suggestionsDiv.innerHTML = '';
                if (suggestions.length) {
                suggestions.slice(0, 5).forEach(function(suggestion) {
                    var button = document.createElement('button');

                    button.textContent = suggestion;
                    button.classList.add("option")

                    suggestionsDiv.appendChild(button);
                });
                } else {
                    var button = document.createElement('button');

                    button.textContent = "No such ingredient";
                    button.classList.add("no-option")

                    suggestionsDiv.appendChild(button);
                }
            };

            xhr.send();
        } else {
            suggestionsDiv.innerHTML = '';
            console.log("no ingredients")
            var p = document.createElement('button');

            p.textContent = "No such ingredient";
            p.classList.add("no-option")

            suggestionsDiv.appendChild(p);
        }
    } else {
        suggestionsDiv.innerHTML = '';
    }
});

document.getElementById('find_meal_button').addEventListener('click', function() {
    if (selected_ingredients.length) {
        this.innerHTML = "finding a meal<p>.</p><p>.</p>"
    };
    fetch('/store_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(selected_ingredients),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/tinder';
            this.innerHTML = "find a meal"
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
