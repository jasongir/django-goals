//! add a modal if the user tries to like without being logged in
const notLoggedInButtons = document.querySelectorAll(".btn-no-login");
const cancelLoginButtons = document.querySelectorAll(".cancel-no-login");

const modal = document.querySelector(".login-modal-container");
console.log(modal);
// console.log(notLoggedInButtons);

notLoggedInButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        modal.classList.remove("hidden-modal");
    });
});

cancelLoginButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        modal.classList.add("hidden-modal");
    });
});

