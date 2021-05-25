//! give each article functionality for deleting
const goalArticles = document.querySelectorAll(".individual-goal");

goalArticles.forEach(goal => {
    const trashCan = goal.querySelector(".delete-goal-trash");
    const confirmDeleteSection = goal.querySelector(".delete-goal");
    const container = goal.querySelector(".edit-delete-buttons");
    // console.log(trashCan);
    // console.log(confirmDeleteSection);

    trashCan.addEventListener("click", () => {
        // console.log("clicked")
        confirmDeleteSection.classList.toggle("hide-delete");
        container.classList.toggle("show-border");
    });
    const cancelDelete = confirmDeleteSection.querySelector(".no-delete-goal");
    cancelDelete.addEventListener("click", () => {
        confirmDeleteSection.classList.add("hide-delete");
        container.classList.remove("show-border");
    });
});