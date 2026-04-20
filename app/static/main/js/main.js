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


 