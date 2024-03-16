var stars = document.querySelectorAll('.rating > .fa');
var recipeElement = document.getElementById('recipe-title');
var recipe = recipeElement.textContent;

for (var i = 0; i < stars.length; i++) {
    stars[i].value = i
    stars[i].addEventListener('click', function() {
        for (var k = 0; k < this.value%5 + 1; k++) {
          stars[this.value - k].classList.add("checked");
        }
        for (var k = 1; k < 5 - this.value; k++) {
          stars[this.value + k].classList.remove("checked");
        }
        var rating = 6-k
        console.log(rating, recipe)

        fetch('/rate', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            rating: rating,
            recipe: recipe}),
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    });
    stars[i].addEventListener('mouseover', function(event) {
      for (var k = 1; k < this.value%5 + 1; k++) {
        if (!stars[this.value - k].classList.contains("checked")) {
          stars[this.value - k].style.color = "gold";
        }
      }
    });
    stars[i].addEventListener('mouseout', function(event) {
      for (var k = 1; k < this.value%5 + 1; k++) {
        stars[this.value - k].style.color = "";
      }
    })
}
