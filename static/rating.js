document.addEventListener('DOMContentLoaded', function() {
    var stars = document.getElementsByClassName('star');

    for (var i = 0; i < stars.length; i++) {
        stars[i].addEventListener('click', function() {
            var recipeId = this.getAttribute('data-recipe-id');
            var rating = this.getAttribute('data-value');

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/rate', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function() {
                if (xhr.status === 200) {
                    alert('You rated this ' + rating + ' stars.');
                }
            };
            xhr.send('recipe_id=' + recipeId + '&rating=' + rating);
        });
    }
});
