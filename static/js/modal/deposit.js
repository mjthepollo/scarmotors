import {modalFuctionFactory} from "./modal.js";

const depositButtons = document.querySelectorAll(".deposit_button");

function depositModalPreprocess(e) {}
function depositModalPostprocess(e) {}

const depositButtonHandler = modalFuctionFactory(depositModalPreprocess, depositModalPostprocess);

for (let i = 0; i < depositButtons.length; i++) {
  depositButtons[i].addEventListener("click", depositButtonHandler);
}
