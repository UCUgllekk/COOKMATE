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
recipes = new_recipes
if (!recipes.length) {
  // var h1 = document.createElement("h1")
  // h1.classList.add("search-title")
  // h1.innerText = "Choose your meal"
  // var emptydiv = document.createElement("div")
  // emptydiv.style("width: 250px;")
  // innerText = "&nbsp;"
  // document.getElementsByClassName("icon-container")[0].classList.add("removed")
  // document.getElementsByClassName("find-meal-container")[0].classList.add("removed")
  var textdiv = document.createElement("h1")
  textdiv.classList.add("no-elements")
  textdiv.innerText = "No recipes."
  // document.getElementsByClassName("main-container")[0].append(textdiv)
  swiper.innerHTML = ""
  swiper.classList.add("no-recipe-div")
  swiper.append(textdiv)
  document.getElementById("ingredients_button").innerText = "main page"
  document.getElementById("ingredients_button").id = "main_page"
  document.getElementById('main_page').addEventListener('click', function() {
    window.location.href = "/"
  });
  // document.getElementById("swiper").innerText = "No recipes."
  console.log("removed")
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
console.log(recipes)

let cardCount = -4;


function appendNewCard() {
  cardCount += 4;
  if (recipes.length <= cardCount) {
    console.log("no recipes left")
    const elements = document.getElementsByClassName("meal-title");
    if (elements.length > 0){
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

  const elements = document.getElementsByClassName("meal-title");
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }

  // Create title for the card
  const title = document.createElement('div');
  title.innerText = recipes[cardCount + 1];
  title.classList.add("meal-title");

  // Append title after the card element
  document.getElementsByClassName("main-container")[0].insertBefore(title, document.getElementsByClassName("find-meal-container")[0]);
  }
}

appendNewCard();


