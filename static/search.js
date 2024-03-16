var selected_ingredients = []
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var suggestionsDiv = document.getElementById('suggestions');
    var suggestions = Array.from(suggestionsDiv.getElementsByTagName('button'));
    console.log()
    if (suggestions.length > 0 && suggestions[0].textContent != "No such ingredient") {
        var shortestSuggestion = suggestions[0]

        var searchBar = document.getElementById('search-bar');
        searchBar.value = shortestSuggestion.textContent;

        var selectedIngredients = Array.from(document.getElementById('selected-ingredients').getElementsByTagName('div'));
        console.log(shortestSuggestion.textContent)
        var alreadySelected = selectedIngredients.some(function(ingredientDiv) {
            return ingredientDiv.textContent === shortestSuggestion.textContent;
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
    document.getElementById('search-bar').value = "";
    document.getElementById('suggestions').innerHTML = "";
});

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('option')) {
            console.log("option")
            console.log(event.target)

            var suggestion = event.target.innerText;
            console.log(suggestion)
            if (suggestion.length > 0) {

                var searchBar = document.getElementById('search-bar');
                searchBar.value = suggestion;

                var selectedIngredients = Array.from(document.getElementById('selected-ingredients').getElementsByTagName('div'));
                console.log(suggestion)
                var alreadySelected = selectedIngredients.some(function(ingredientDiv) {
                    return ingredientDiv.textContent === suggestion;
                });

                if (!alreadySelected) {
                    var ingredientDiv = document.createElement('div');
                    ingredientDiv.textContent = suggestion;
                    ingredientDiv.classList.add("tag");
                    selected_ingredients.push(suggestion);
                    console.log(selected_ingredients);
                    document.getElementById('selected-ingredients').appendChild(ingredientDiv);
                }
            };
            document.getElementById('search-bar').value = "";
            document.getElementById('suggestions').innerHTML = "";
        }
    });
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
                console.log(suggestions.length)
                if (suggestions.length) {
                suggestions.slice(0, 5).forEach(function(suggestion) {
                    var p = document.createElement('button');

                    p.textContent = suggestion;
                    p.classList.add("option")

                    suggestionsDiv.appendChild(p);
                });
                } else {
                    console.log("no ingredients")
                    var p = document.createElement('button');

                    p.textContent = "No such ingredient";
                    p.classList.add("no-option")

                    suggestionsDiv.appendChild(p);
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
    this.innerHTML = "finding a meal<p>.</p><p>.</p>"
    fetch('/store_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(selected_ingredients),
    })
    .then(response => {
        if (response.ok) {
            this.innerHTML = "find a meal"
            window.location.href = '/tinder';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

