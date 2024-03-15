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

        ingredients_section.append(titleDiv)
        var column_div = document.createElement('div');
        column_div.classList.add("ingredients-column");
        
        var img = document.createElement('img');
        img.src = "static/Food Images/"+ liked_recipes[i][0] + ".jpg";
        img.loading = "lazy";
        img.classList.add("img-3");
        column_div.append(img);

        var div = document.createElement("div");
        var textdiv = document.createElement("div")
        textdiv.classList.add("ingredient-text")
        ingredients = liked_recipes[i][2].split("; ")
        for (var k of Array(ingredients.length).keys()) {
            ingredients[k] = " • " + ingredients[k] + "<br />"
        }
        textdiv.innerHTML = ingredients.join("")
        
        div.append(textdiv)

        // var show_recipe = document.createElement("a")
        // show_recipe.idli
        // show_recipe.classList.add("find-meal visible")
        // <div class="find-meal-container">
        //   <a href="javascript:void(0);" id="expandButton" class="find-meal visible">find a meal</a>
        // </div>
        
        ingredients_section.append(column_div)
        ingredients_section.append(div)
        
        document.getElementById("recipe-details").append(ingredients_section)
    }
}
console.log(liked_recipes)