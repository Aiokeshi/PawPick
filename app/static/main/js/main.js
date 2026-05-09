const slides = document.querySelectorAll('.slider img , .card_slider img');
let i = 0;

function show(n) {
  slides[i].classList.remove('active');
  i = (n + slides.length) % slides.length;
  slides[i].classList.add('active');
}

document.getElementById('next').onclick = () => show(i + 1);
document.getElementById('prev').onclick = () => show(i - 1);

setInterval(() => show(i + 1), 3000);

document.addEventListener('DOMContentLoaded', function () {
    initSliders();
    initFilmReelCarousel();
    initProfileEdit();
});


function initSliders() {
    const sliderBlocks = document.querySelectorAll('.slider, .card_slider');

    sliderBlocks.forEach(function (slider) {
        const slides = slider.querySelectorAll('img');
        const nextButton = slider.querySelector('#next, .next');
        const prevButton = slider.querySelector('#prev, .prev');

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
            slides[currentIndex].classList.remove('active');
            currentIndex = (index + slides.length) % slides.length;
            slides[currentIndex].classList.add('active');
        }

        if (nextButton) {
            nextButton.addEventListener('click', function () {
                showSlide(currentIndex + 1);
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', function () {
                showSlide(currentIndex - 1);
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
