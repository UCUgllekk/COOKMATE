var stars = document.querySelectorAll('.rating > .fa');
var recipeElement = document.getElementById('recipe-title');
var recipe = recipeElement.textContent;
var stars_div = document.querySelector(".rating");
var rating = stars_div.getAttribute("rating")
if (rating == undefined) {
  rating = 0;
}
for (var i = 0; i < stars.length; i++) {
    stars[i].value = i;
    stars[i].addEventListener('click', function() {
      if (this.value + 1 == rating) {
        for (var k = 0; k < 5; k++) {
          stars[k].classList.remove("checked");
          stars[k].style.color = "";
        }
        rating = 0;
      } else {
        for (var k = 0; k < this.value%5 + 1; k++) {
          stars[this.value - k].classList.add("checked");
        }
        for (var k = 1; k < 5 - this.value; k++) {
          stars[this.value + k].classList.remove("checked");
        }
        rating = this.value + 1;
      }
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
      for (var k = 0; k < this.value%5 + 1; k++) {
        if (!stars[this.value - k].classList.contains("checked")) {
          stars[this.value - k].style.color = "gold";
        }
      }
    });
    stars[i].addEventListener('mouseout', function(event) {
      for (var k = 0; k < this.value%5 + 1; k++) {
        stars[this.value - k].style.color = "";
      }
    })
}
