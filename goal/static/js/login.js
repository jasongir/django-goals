const form = document.querySelector(".login-form");
const submitBtn = document.querySelector(".submit-btn");

const tableContainer = document.querySelector(".table");
const divContainer = document.querySelector(".mobile-form");

const changeForm = (e) => {
    if (window.innerWidth < 450) {
        submitBtn.insertAdjacentElement('beforebegin', divContainer);
        form.insertAdjacentElement('afterend', tableContainer);

        tableContainer.style.display = 'none';
        divContainer.style.display = 'block';
    } else {
        submitBtn.insertAdjacentElement('beforebegin', tableContainer);
        form.insertAdjacentElement('afterend', divContainer);

        tableContainer.style.display = 'block';
        divContainer.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', changeForm);
window.addEventListener('resize', changeForm);