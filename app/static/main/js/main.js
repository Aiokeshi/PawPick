document.addEventListener('DOMContentLoaded', function () {
  initSliders();
  initFilmReelCarousel();
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

    if (slider.classList.contains('slider')) {
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
