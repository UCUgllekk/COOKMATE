// Make an AJAX request to get the image names
fetch('/store_data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(yourData),  // replace yourData with the actual data you want to send
})
.then(response => response.json())
.then(data => {
    // data is the list of found recipes
    console.log(data)
    const urls = data.map(recipe => '/static/FoodImages/$' + recipe.image_name);  // Replace urls with the image names

    // Now you can use urls in your appendNewCard function
    function appendNewCard(imageUrl) {
        const card = new Card({
            imageUrl: imageUrl,
            onDismiss: appendNewCard,
            onLike: () => {
                like.style.animationPlayState = 'running';
                like.classList.toggle('trigger');
            },
            onDislike: () => {
                dislike.style.animationPlayState = 'running';
                dislike.classList.toggle('trigger');
            }
        });

        swiper.append(card.element);

        // Create title for the card
        const title = document.createElement('div');

        // Append title after the card element
        swiper.append(title);
    }

    // Call the function to create a card for each image
    urls.forEach(url => {
        appendNewCard(url);
    });
});
