// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

// constants
const urls = [
  'https://source.unsplash.com/random/1000x1000/?sky',
  'https://source.unsplash.com/random/1000x1000/?landscape',
  'https://source.unsplash.com/random/1000x1000/?ocean',
  'https://source.unsplash.com/random/1000x1000/?moutain',
  'https://source.unsplash.com/random/1000x1000/?forest'
];

// variables
let cardCount = 0;

// script.js

// script.js

function appendNewCard() {
  const card = new Card({
    imageUrl: urls[cardCount % 5],
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

  // Створення елементу для назви фото
  const title = document.createElement('div');
  title.textContent = `Фото ${cardCount + 1}`;
  title.classList.add('card-title');

  // Створення елементу для тексту під фото
  const description = document.createElement('div');
  description.textContent = `Опис фото ${cardCount + 1}`;
  description.classList.add('card-description');
  
  // Створення контейнера для карти та її назви та опису
  const cardContainer = document.createElement('div');
  cardContainer.classList.add('card-container');
  cardContainer.appendChild(card.element);
  cardContainer.appendChild(title);
  cardContainer.appendChild(description);

  swiper.append(cardContainer);
  cardCount++;
}

// Виклик функції для створення перших 5 карт
for (let i = 0; i < 5; i++) {
  appendNewCard();
}

