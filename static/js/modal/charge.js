import {modalFuctionFactory, numberWithCommas} from "./modal.js";

const chargeButtons = document.querySelectorAll(".charge_button");

function setRepairAmountInfoFactory(e, repairAmountInfo, wageAmountInput, componentAmountInput) {
  return function (e) {
    const wageAmount = isNaN(parseInt(wageAmountInput.value)) ? 0 : parseInt(wageAmountInput.value);
    const componentAmount = isNaN(parseInt(componentAmountInput.value)) ? 0 : parseInt(componentAmountInput.value);
    console.log(componentAmount);
    const repairAmount = wageAmount + componentAmount;
    repairAmountInfo.innerHTML = isNaN(repairAmount) ? "-" : numberWithCommas(repairAmount);
  };
}

function chargeModalPreprocess(e) {}
function chargeModalPostprocess(e, modal) {
  const wageAmountInput = modal.querySelector("#id_wage_amount");
  const componentAmountInput = modal.querySelector("#id_component_amount");
  const repairAmountInfo = modal.querySelector(".repair_amount_info");
  const setRepairAmount = setRepairAmountInfoFactory(e, repairAmountInfo, wageAmountInput, componentAmountInput);
  wageAmountInput.addEventListener("input", setRepairAmount);
  componentAmountInput.addEventListener("input", setRepairAmount);
  setRepairAmount();
}

const chargeButtonHandler = modalFuctionFactory(chargeModalPreprocess, chargeModalPostprocess);

for (let i = 0; i < chargeButtons.length; i++) {
  chargeButtons[i].addEventListener("click", chargeButtonHandler);
}
