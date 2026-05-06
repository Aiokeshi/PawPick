document.addEventListener('DOMContentLoaded', function () {
    const burgerButton = document.querySelector('[data-burger-button]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    const overlay = document.querySelector('[data-mobile-menu-overlay]');

    if (!burgerButton || !mobileMenu || !overlay) {
        return;
    }

    function closeMenu() {
        burgerButton.classList.remove('is-open');
        mobileMenu.classList.remove('is-open');
        overlay.classList.remove('is-open');
        burgerButton.setAttribute('aria-expanded', 'false');
        burgerButton.setAttribute('aria-label', 'Открыть меню');
        document.body.classList.remove('menu-open');
    }

    function openMenu() {
        burgerButton.classList.add('is-open');
        mobileMenu.classList.add('is-open');
        overlay.classList.add('is-open');
        burgerButton.setAttribute('aria-expanded', 'true');
        burgerButton.setAttribute('aria-label', 'Закрыть меню');
        document.body.classList.add('menu-open');
    }

    burgerButton.addEventListener('click', function () {
        if (mobileMenu.classList.contains('is-open')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    overlay.addEventListener('click', closeMenu);

    mobileMenu.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeMenu();
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 767) {
            closeMenu();
        }
    });
});
