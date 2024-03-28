// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');
recipes = recipes.slice(2, -2).split('", "')
var new_recipes = []
for (var i = 0; i < recipes.length; i++){
  if (recipes[i].length) {
    new_recipes.push(recipes[i])
  }
}



recipes = new_recipes;
if (!recipes.length) {
  var textdiv = document.createElement("div");
  var h1 = document.createElement("h1");
  h1.innerText = "No recipes.";
  textdiv.append(h1);
  swiper.innerHTML = "";
  swiper.style = "display: flex; justify-content: center; align-items: center;";
  swiper.append(textdiv);
  document.getElementById("ingredients_button").innerText = "main page";
  document.getElementById("ingredients_button").id = "main_page";
  document.getElementById('main_page').addEventListener('click', function() {
    window.location.href = "/";
  });
  console.log("removed");
  like.remove();
  dislike.remove();
} else{
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
}
var liked_recipes = []
let cardCount = -4;
var card = ""

function appendNewCard() {
  cardCount += 4;
  if (recipes.length <= cardCount) {
    document.querySelector(".meal-title").remove()
    document.querySelector(".counter").remove();
  } else {
  card = new Card({
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
  if (cardCount != 0) {
    document.querySelector(".meal-title").remove();
    document.querySelector(".counter").remove();
  }
  const counter = document.createElement("div");
  counter.classList.add("counter");
  counter.innerText = `Recipes left: ${(recipes.length - cardCount) / 4}`;


  // Create title for the card
  const title = document.createElement('div');
  title.innerText = recipes[cardCount + 1];
  title.classList.add("meal-title");


  // Append title after the card element
  document.querySelector(".main-container").insertBefore(counter, document.querySelector(".icon-container"));
  document.querySelector(".main-container").insertBefore(title, document.querySelector(".find-meal-container"));
  }
}

appendNewCard();

function onLike() {
  card.dismiss(1)
}

function onDislike() {
  card.dismiss(-1)
}
