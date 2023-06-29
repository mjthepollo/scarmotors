import {modalFuctionFactory} from "./modal.js";

const chargeButtons = document.querySelectorAll(".charge_button");

function chargeModalPreprocess(e) {}
function chargeModalPostprocess(e) {}

const chargeButtonHandler = modalFuctionFactory(chargeModalPreprocess, chargeModalPostprocess);

for (let i = 0; i < chargeButtons.length; i++) {
  chargeButtons[i].addEventListener("click", chargeButtonHandler);
}
