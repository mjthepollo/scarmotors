import {modalFuctionFactory} from "./modal.js";

const cameOutButtons = document.querySelectorAll(".came_out_button");

function cameOutModalPreprocess(e) {}
function cameOutModalPostprocess(e) {}

const cameOutButtonHandler = modalFuctionFactory(cameOutModalPreprocess, cameOutModalPostprocess);

for (let i = 0; i < cameOutButtons.length; i++) {
  cameOutButtons[i].addEventListener("click", cameOutButtonHandler);
}
