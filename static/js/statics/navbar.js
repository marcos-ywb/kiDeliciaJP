document.addEventListener('DOMContentLoaded', () => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {

            const target = el.dataset.target;
            const $target = document.getElementById(target);

            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');

        });
    });

});


document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.getElementById('dropdownMenu');
    const dropdownLink = dropdown.querySelector('.navbar-link');
    const dropdownContent = dropdown.querySelector('.navbar-dropdown');

    function setDropdownBehavior() {
        if (window.innerWidth > 1023) {
            dropdown.classList.add('is-hoverable');
            dropdown.classList.remove('is-active');
            dropdownContent.style.display = '';
            dropdownLink.removeEventListener('click', toggleDropdown);

        } else {
            dropdown.classList.remove('is-hoverable');
            dropdownContent.style.display = 'none';
            dropdown.classList.remove('is-active');
            dropdownLink.addEventListener('click', toggleDropdown);
        }
    }

    function toggleDropdown(event) {
        event.preventDefault();
        if (dropdownContent.style.display === 'none') {
            dropdownContent.style.display = 'block';

        } else {
            dropdownContent.style.display = 'none';
        }

        dropdown.classList.toggle('is-active');
    }

    setDropdownBehavior();
    window.addEventListener('resize', setDropdownBehavior);
});
