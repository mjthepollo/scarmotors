const goLeftButtons = document.querySelectorAll("button.go_left");
const goRightButtons = document.querySelectorAll("button.go_right");

const questionContainer = document.querySelector("#question_container");

let counter = 0;

for (let i = 0; i < goLeftButtons.length; i++) {
  goLeftButtons[i].addEventListener("click", goLeft);
}
for (let i = 0; i < goRightButtons.length; i++) {
  goRightButtons[i].addEventListener("click", goRight);
}

function goLeft(e) {
  counter--;
  questionContainer.style.transform = `translateX(-${counter}00vw)`;
}

function goRight(e) {
  counter++;
  questionContainer.style.transform = `translateX(-${counter}00vw)`;
}
