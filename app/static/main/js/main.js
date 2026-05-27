document.addEventListener('DOMContentLoaded', function () {
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
  });
});
