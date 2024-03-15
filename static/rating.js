var stars = document.querySelectorAll('.rating > .fa');
for (var i = 0; i < stars.length; i++) {
    stars[i].value = i
    stars[i].addEventListener('click', function() {
        // Remove the 'checked' class from all stars
        // Add the 'checked' class to the clicked star and all previous stars
        for (var k = 0; k < this.value%5 + 1; k++) {
          console.log("checked", this.value - k)
          stars[this.value - k].classList.add("checked");
        }
        for (var k = 1; k < 5 - this.value; k++) {
          console.log("unchecked", this.value + k)
          stars[this.value + k].classList.remove("checked");
        }
        console.log("")
        // Store the rating in the user's data
        // This will depend on how you're storing user data
        // For example, you might use localStorage:
        localStorage.setItem('rating', i + 1);
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