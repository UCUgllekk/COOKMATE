var selected_ingredients = [];
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
            var ingredient_deleter = document.createElement('div');
            ingredient_deleter.className = "ingredient_deleter";
            var ingredientDiv = document.createElement('div');
            ingredientDiv.textContent = shortestSuggestion.textContent;
            ingredientDiv.classList.add("tag");
            selected_ingredients.push(shortestSuggestion.textContent);
            const selected_ingredients_div = document.getElementById('selected-ingredients');
            ingredient_deleter.appendChild(ingredientDiv);
            ingredient_deleter.innerHTML += `<button class="deleter" id='deleter:${shortestSuggestion.textContent}'><i class="fa fa-xmark"></i></button>`;
            selected_ingredients_div.appendChild(ingredient_deleter)
            document.getElementById(`deleter:${shortestSuggestion.textContent}`).addEventListener("click", function() {
                const ind = selected_ingredients.indexOf(this.id.slice(8));
                selected_ingredients.splice(ind, 1);
                selected_ingredients_div.getElementsByClassName("ingredient_deleter")[ind].remove();
            });
        }
        searchBar.value = "";
        searchBar.focus();
        suggestionsDiv.innerHTML = "";
    };
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
                var ingredient_deleter = document.createElement('div');
                ingredient_deleter.className = "ingredient_deleter";
                var ingredientDiv = document.createElement('div');
                ingredientDiv.textContent = suggestion;
                ingredientDiv.classList.add("tag");
                selected_ingredients.push(suggestion);
                const selected_ingredients_div = document.getElementById('selected-ingredients');
                ingredient_deleter.appendChild(ingredientDiv);
                ingredient_deleter.innerHTML += `<button class="deleter" id='deleter:${suggestion}'><i class="fa fa-xmark"></i></button>`;
                selected_ingredients_div.appendChild(ingredient_deleter)
                document.getElementById(`deleter:${suggestion}`).addEventListener("click", function() {
                    const ind = selected_ingredients.indexOf(this.id.slice(8));
                    selected_ingredients.splice(ind, 1);
                    selected_ingredients_div.getElementsByClassName("ingredient_deleter")[ind].remove();
                });
            }
        };
        searchBar.value = "";
        event.target.parentNode.innerHTML = "";
        searchBar.focus();
    }
});

function isAlphaSpace(text){
    return /^[A-Z ]*$/i.test(text) && /[A-Z]{1}/i.test(text);
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
                    if (document.getElementById('search-bar').value.toLowerCase() == inputVal) {
                        suggestions.slice(0, 5).forEach(function(suggestion) {
                            var button = document.createElement('button');

                            button.textContent = suggestion;
                            button.classList.add("option")

                            suggestionsDiv.appendChild(button);
                        });
                    } else {
                        document.getElementById('search-bar').dispatchEvent(new Event("input", {bubbles: true}))
                    }
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
            var p = document.createElement('button');

            p.textContent = "No such ingredient";
            p.classList.add("no-option")

            suggestionsDiv.appendChild(p);
        }
    } else {
        suggestionsDiv.innerHTML = '';
    }
});

// document.getElementById('select_hint').addEventListener('mouseenter', function() {
//     const hint_div = document.createElement("div");
//     hint_div.textContent = "Start typing the ingredient you want to select. Under the search bar there will be suggestions. To pick the first one press Enter. To pick the any of suggested click on the right suggestion with mouse."
//     hint_div.classList = "hint";
//     this.appendChild(hint_div)
// });

// document.getElementById('select_hint').addEventListener('mouseleave', function() {
//     const hint_div = this.querySelector(".hint");
//     this.removeChild(hint_div)
// });

document.getElementById("search-bar-img").addEventListener("click", function() {
    document.getElementById("search-title").scrollIntoView({behavior: "smooth"})
    setTimeout(function() {
        document.getElementById("search-bar").focus()
    }, 500)
});

document.querySelector(".arrow-link").addEventListener("click", function() {
    document.getElementById("search-title").scrollIntoView({behavior: "smooth"})
    setTimeout(function() {
        document.getElementById("search-bar").focus()
    }, 500)
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
