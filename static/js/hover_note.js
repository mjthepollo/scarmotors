const hoverNotes = document.querySelectorAll(".hover_note");

function showHoverNotes(e) {
  const hoverNote = e.currentTarget.querySelector(".hover_note");
  hoverNote.classList.remove("hidden");
}

function hideHoverNotes(e) {
  const hoverNote = e.currentTarget.querySelector(".hover_note");
  hoverNote.classList.add("hidden");
}

for (let i = 0; i < hoverNotes.length; i++) {
  hoverNotes[i].parentElement.addEventListener("mouseover", showHoverNotes);
  hoverNotes[i].parentElement.addEventListener("mouseout", hideHoverNotes);
}
