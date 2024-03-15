if (liked_recipes) {
    liked_recipes = liked_recipes.slice(2, -2).split("], [");
    for (var i = 0; i < liked_recipes.length; i++) {
        liked_recipes[i] = liked_recipes[i].slice(1, -1).split('", "');
    }
    ingredients_section = document.getElementById("ingredients_section");
    console.log(liked_recipes)
    for (var i = 0; i < liked_recipes.length; i ++) {
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

        ingredients_section.append(column_div)
        ingredients_section.append(div)

    }
}
console.log(liked_recipes)