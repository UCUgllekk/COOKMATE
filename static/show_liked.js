if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}
if (liked_recipes != "[]") {
    liked_recipes = liked_recipes.slice(2, -2).split("], [");
    var new_liked_recipes = [];
    // liked_recipes.push(["asd", "asdf"]);
    for (var i = 0; i < liked_recipes.length; i++) {
        if (liked_recipes[i].slice(1, -1).split('", "')) {
        new_liked_recipes.push(liked_recipes[i].slice(1, -1).split('", "'));
        }
    };
    liked_recipes = new_liked_recipes
    for (var i = 0; i < liked_recipes.length; i ++) {
        ingredients_section = document.createElement("div");
        ingredients_section.classList.add("ingredients-section")
        var titleDiv = document.createElement('div')
        titleDiv.classList.add("recipe-title")
        titleDiv.innerText = liked_recipes[i][1]

        // ingredients_section.append(titleDiv)
        var column_div = document.createElement('div');
        column_div.classList.add("ingredients-column");

        var img = document.createElement('img');
        img.src = "static/Food Images/"+ liked_recipes[i][0] + ".jpg";
        img.loading = "lazy";
        img.classList.add("img-3");
        column_div.append(img);

        var textdiv = document.createElement("div");
        textdiv.classList.add("ingredient-text");
        ingredients = liked_recipes[i][2].split("; ");
        var ul_ingr = document.createElement("ul");
        for (var ingredient of ingredients) {
            ul_ingr.innerHTML += "<li>" + ingredient + "</li>";
        }
        textdiv.append(ul_ingr)

        var show_recipe = document.createElement("a")
        // show_recipe.id = 
        show_recipe.innerText = "jump to recipe"
        show_recipe.href = "javascript:void(0);"
        show_recipe.classList.add("find-meal")
        show_recipe.classList.add("visible")

        var find_meal_div = document.createElement("div")
        find_meal_div.classList.add("find-meal-container")
        find_meal_div.append(show_recipe)
        // <div class="find-meal-container">
        //   <a href="javascript:void(0);" id="expandButton" class="find-meal visible">find a meal</a>
        // </div>
        
        ingredients_section.append(column_div)
        ingredients_section.append(textdiv)

        document.getElementsByClassName("recipe-details")[0].append(titleDiv)
        document.getElementsByClassName("recipe-details")[0].append(ingredients_section)
        document.getElementsByClassName("recipe-details")[0].append(find_meal_div)
    }
} else {
    var h2 = document.createElement("h1")
    h2.innerText = "No liked recipes"
    h2.style.margin = "10% 10%";
    var main_page = document.createElement("a")
    main_page.innerText = "main page"
    main_page.href = "/"
    main_page.classList.add("find-meal")
    main_page.classList.add("visible")

    var main_page_div = document.createElement("div")
    main_page_div.classList.add("find-meal-container")
    main_page_div.style.position = "absolute";
    main_page_div.style.bottom = 0;
    main_page_div.append(main_page)
    document.getElementsByClassName("main-container")[0].append(h2)
    document.getElementsByClassName("main-container")[0].append(main_page_div)
}
const expandButtons = document.getElementsByClassName('find-meal');
expandButtons_dict = {}
num_of_buttons = expandButtons.length
for (var i = 0; i < expandButtons.length; i ++) {
    expandButtons_dict[i] = expandButtons[i];
    expandButtons[i].value = i;
    expandButtons[i].addEventListener('click', function() {
        const recipeTitle = document.createElement('div');
        recipeTitle.classList.add('recipe-title2');

        recipeTitle.innerText = 'Recipe';
        recipeTitle.style.fontWeight = 'bold';
        recipeTitle.style.border = 'none'; // Remove the borderf
        recipeTitle.style.textAlign = 'left'; // Align text to the left

        const recipeDescription = document.createElement('div');
        recipeDescription.classList.add('recipe-description');
        split_instructions = liked_recipes[this.value][3].trim().split(/\n/);
        var ul = document.createElement("ul");
        for (var part of split_instructions) {
            for (line of part.split(/\. |\.$; /))
                if (/[A-Z]+/i.test(line) && !["F", "tsp", "tbsp", "Tbsp", "Tsp"].some((el) => line.endsWith(el + "."))) {
                    line = line.trim()
                    ul.innerHTML += `<li>${line.charAt(0).toUpperCase() + line.slice(1)}</li>`;
                };
            ul.innerHTML += "<p></p>";
        };
        recipeDescription.append(ul);
        expandButtons_dict[this.value].parentNode.parentNode.insertBefore(recipeTitle, expandButtons_dict[this.value].parentNode.nextSibling);
        expandButtons_dict[this.value].parentNode.parentNode.insertBefore(recipeDescription, recipeTitle.nextSibling);
        expandButtons_dict[this.value].scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Remove the button after clicking
        expandButtons_dict[this.value].parentNode.remove()
        const ingredientText = document.querySelectorAll('.ingredient-text');
        ingredientText.forEach(item => {
        item.style.overflowWrap = 'break-word';
        item.style.listStyleType = 'disc';
        });
    });
}