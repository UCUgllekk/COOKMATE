// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');
recipes = recipes.slice(2, -2).split('", "')
if (recipes && recipes[0] == "") {
  recipes = []
}
var liked_recipes = []
console.log(recipes)
// constants
// const urls = [
//   'https://source.unsplash.com/random/1000x1000/?sky',
//   'https://source.unsplash.com/random/1000x1000/?landscape',
//   'https://source.unsplash.com/random/1000x1000/?ocean',
//   'https://source.unsplash.com/random/1000x1000/?moutain',
//   'https://source.unsplash.com/random/1000x1000/?forest'
// ];

// variables
let cardCount = -4;

// script.js

// script.js

function appendNewCard() {
  cardCount += 4;
  if (recipes.length <= cardCount) {
    console.log("no recipes left")
    const elements = document.getElementsByClassName("title");
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
  } else {
  const card = new Card({
    imageUrl: recipes[cardCount],
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

  const elements = document.getElementsByClassName("title");
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }

  // Create title for the card
  const title = document.createElement('div');
  title.innerText = recipes[cardCount + 1];
  title.classList.add("title");

  // Append title after the card element
  swiper.append(title);
  }
}

appendNewCard();

document.getElementById('ingredients_button').addEventListener('click', function() {
  fetch('/store_liked_recipes', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(liked_recipes),
  })
  .then(response => {
      if (response.ok) {
          window.location.href = '/ingredients';
      }
  })
  .catch((error) => {
      console.error('Error:', error);
  });
});
