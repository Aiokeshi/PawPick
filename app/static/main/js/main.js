document.addEventListener('DOMContentLoaded', function () {
  initSliders();
  initFilmReelCarousel();
  initFavoriteButtons();
});

function initSliders() {
  const sliders = document.querySelectorAll('.slider, .card_slider');

  sliders.forEach(function (slider) {
    const slides = slider.querySelectorAll('img');

    if (!slides.length) {
      return;
    }

    let currentIndex = 0;

    const activeIndex = Array.from(slides).findIndex(function (slide) {
      return slide.classList.contains('active');
    });

    if (activeIndex >= 0) {
      currentIndex = activeIndex;
    } else {
      slides[0].classList.add('active');
    }

    function showSlide(index) {
      slides.forEach(function (slide) {
        slide.classList.remove('active');
      });

      currentIndex = (index + slides.length) % slides.length;
      slides[currentIndex].classList.add('active');
    }

    showSlide(currentIndex);

    const prevButton = slider.querySelector('#prev, .prev');
    const nextButton = slider.querySelector('#next, .next');

    if (prevButton) {
      prevButton.addEventListener('click', function (event) {
        event.preventDefault();
        showSlide(currentIndex - 1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener('click', function (event) {
        event.preventDefault();
        showSlide(currentIndex + 1);
      });
    }

    if (
      slides.length > 1 &&
      (
        slider.classList.contains('slider') ||
        slider.classList.contains('card_slider')
      )
    ) {
      setInterval(function () {
        showSlide(currentIndex + 1);
      }, 3000);
    }
  });
}

function initFilmReelCarousel() {
  const reelTrack = document.querySelector('.sec3slider');

  if (!reelTrack) {
    return;
  }

  if (reelTrack.classList.contains('is-running')) {
    return;
  }

  const images = Array.from(reelTrack.querySelectorAll('img'));

  if (images.length < 2) {
    return;
  }

  images.forEach(function (image) {
    const clone = image.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    reelTrack.appendChild(clone);
  });

  reelTrack.classList.add('is-running');
}

function initFavoriteButtons() {
  const favoriteForms = document.querySelectorAll('.favorite-form');

  favoriteForms.forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();

      const button = form.querySelector('.favorite-button');

      if (!button || button.disabled) {
        return;
      }

      button.disabled = true;

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
      })
        .then(function (response) {
          if (response.redirected) {
            window.location.href = response.url;
            return null;
          }

          if (!response.ok) {
            throw new Error('Favorite request failed');
          }

          return response.json();
        })
        .then(function (data) {
          if (!data) {
            return;
          }

          if (data.is_favorite) {
            button.classList.add('is-favorite');
            button.setAttribute('aria-label', 'Убрать из избранного');
            button.setAttribute('title', 'Убрать из избранного');
          } else {
            button.classList.remove('is-favorite');
            button.setAttribute('aria-label', 'Добавить в избранное');
            button.setAttribute('title', 'Добавить в избранное');

            removeCardFromFavoritesPage(form);
          }
        })
        .catch(function () {
          form.submit();
        })
        .finally(function () {
          button.disabled = false;
        });
    });
  });
}

function removeCardFromFavoritesPage(form) {
  const favoritesCatalog = form.closest('.favorites-catalog');

  if (!favoritesCatalog) {
    return;
  }

  const card = form.closest('.card');

  if (card) {
    card.remove();
  }

  const remainingCards = favoritesCatalog.querySelectorAll('.card');

  if (remainingCards.length === 0) {
    window.location.reload();
  }
}
