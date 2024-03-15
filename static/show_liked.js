if (liked_recipes) {
    liked_recipes = liked_recipes.slice(2, -2).split("], [");
    for (var i = 0; i < liked_recipes.length; i++) {
        liked_recipes[i] = liked_recipes[i].slice(1, -1).split('", "');
    }
    console.log(liked_recipes)
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

        var textdiv = document.createElement("div")
        textdiv.classList.add("ingredient-text")
        ingredients = liked_recipes[i][2].split("; ")
        for (var k of Array(ingredients.length).keys()) {
            ingredients[k] = " • " + ingredients[k] + "<br />"
        }
        textdiv.innerHTML = ingredients.join("")

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
}
console.log(liked_recipes)
console.log(document.getElementById("expandButton"))
const expandButtons = document.getElementsByClassName('find-meal');
expandButtons_dict = {}
num_of_buttons = expandButtons.length
console.log(expandButtons)
for (var i = 0; i < expandButtons.length; i ++) {
    expandButtons_dict[i] = expandButtons[i]
    expandButtons[i].value = i
    expandButtons[i].addEventListener('click', function() {
        const recipeTitle = document.createElement('div');
        recipeTitle.classList.add('recipe-title2');
        
        // console.log(liked_recipes[i][3])
        console.log(this.value)
        recipeTitle.innerText = 'Recipe';
        recipeTitle.style.fontWeight = 'bold';
        recipeTitle.style.border = 'none'; // Remove the borderf
        recipeTitle.style.textAlign = 'left'; // Align text to the left

        const recipeDescription = document.createElement('div');
        recipeDescription.classList.add('recipe-description');
        recipeDescription.innerHTML = liked_recipes[this.value][3].split(". ").join(".<br \>");
        const findMealContainers = document.getElementsByClassName('find-meal-container');
        findMealContainers[this.value].parentNode.insertBefore(recipeTitle, findMealContainers[this.value].nextSibling);
        findMealContainers[this.value].parentNode.insertBefore(recipeDescription, recipeTitle.nextSibling);
        if (this.value == num_of_buttons - 1) {
        recipeTitle.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        // Remove the button after clicking
        expandButtons_dict[this.value].parentNode.removeChild(expandButtons_dict[this.value]);


        // Add CSS styles to ingredient-text class
        const ingredientText = document.querySelectorAll('.ingredient-text');
        ingredientText.forEach(item => {
        item.style.overflowWrap = 'break-word';
        item.style.listStyleType = 'disc';
        });
    });
}