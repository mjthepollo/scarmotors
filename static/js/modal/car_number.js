import {modalFuctionFactory} from "./modal.js";

const carNumberInput = document.querySelector("input[name=car_number]");
const carNumberButton = document.querySelector("#car_number_button");

function carNumberModalPreprocess(e) {
  const carNumber = carNumberInput.value;
  const defaultUrl = e.currentTarget.dataset.modal_default_url;
  const modalUrl = defaultUrl + carNumber;
  console.log(modalUrl);
  e.currentTarget.dataset.modal_url = modalUrl;
}
function carNumberModalPostprocess(e, modal) {}

const carNumberButtonHandler = modalFuctionFactory(carNumberModalPreprocess, carNumberModalPostprocess);

carNumberButton.addEventListener("click", carNumberButtonHandler);
