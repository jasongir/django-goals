//? Add the necessary event listeners to the goal
const goal = document.querySelector(".goal-info");  // this is the article which has the goal inside

const container = goal.querySelector(".edit-delete-buttons"); // this is the container for this whole section with buttons
const trashCan = goal.querySelector(".delete-goal-trash"); // this is the button to press to delete the goal
const confirmDeleteSection = goal.querySelector(".delete-goal"); // this is the hidden section that has the confirmation text

trashCan.addEventListener("click", () => {
    // console.log("clicked")
    confirmDeleteSection.classList.toggle("hide-delete"); // show or hide the confirmation text
    container.classList.toggle("show-border"); // show or hide the border for the larger container
});

const cancelDelete = confirmDeleteSection.querySelector(".no-delete-goal"); // button for saying canceling deletion and closing the popup

cancelDelete.addEventListener("click", () => {
    confirmDeleteSection.classList.add("hide-delete"); // hide the confirmation section
    container.classList.remove("show-border"); // stop showing the border
});

//? Add the necessary event listeners to the comments
const commentButtonSections = document.querySelectorAll(".comment .delete-comment-buttons");

commentButtonSections.forEach(section => {
    const trashCan = section.querySelector(".delete-comment-trash");
    const hiddenDiv = section.querySelector(".delete-comment");
    // console.log(section);
    // console.log(trashCan);
    // console.log(hiddenDiv);

    trashCan.addEventListener("click", () => {
        hiddenDiv.classList.toggle("hide-delete");
        section.classList.toggle("show-border");
    });

    const cancel = section.querySelector(".no-delete-comment");
    cancel.addEventListener("click", () => {
        hiddenDiv.classList.add("hide-delete");
        section.classList.add("show-border");
    });
});
