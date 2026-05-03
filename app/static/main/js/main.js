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


 document.getElementById('editBtn').onclick = function() {

    document.getElementById('nameText').style.display = 'none';
    document.getElementById('nameInput').style.display = 'block';

    document.getElementById('saveBtn').style.display = 'inline-block';
    this.style.display = 'none';

    // клик по аватару = загрузка
    document.getElementById('avatarPreview').onclick = function() {
        document.getElementById('avatarInput').click();
    }
}

// превью аватара
document.getElementById('avatarInput').onchange = function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('avatarPreview').src = URL.createObjectURL(file);
    }
}