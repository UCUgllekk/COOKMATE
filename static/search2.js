document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('search_bar');

    searchInput.addEventListener('input', function() {
        var query = searchInput.value;

        if(query.length > 0){
            fetch('/search?query=' + query)
                .then(response => response.json())
                .then(data => {
                    var resultsDiv = document.getElementById('results');
                    resultsDiv.innerHTML = '';

                    data.forEach(function(ingredient) {
                        var p = document.createElement('p');
                        p.textContent = ingredient;
                        resultsDiv.appendChild(p);
                    });
                });
        } else {
            document.getElementById('results').innerHTML = '';
        }
    });
});
