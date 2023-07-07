import {numberWithCommas} from "../utility.js";
import {modalFuctionFactory} from "./modal.js";

const chargeButtons = document.querySelectorAll(".charge_button");

function setChargeInfoFactory(wageAmountInput, componentAmountInput, repairAmountInfo, vatInfo, chargableAmountInfo) {
  return function (e) {
    const wageAmount = isNaN(parseInt(wageAmountInput.value)) ? 0 : parseInt(wageAmountInput.value);
    const componentAmount = isNaN(parseInt(componentAmountInput.value)) ? 0 : parseInt(componentAmountInput.value);
    const repairAmount = wageAmount + componentAmount;
    const vatAmount = repairAmount * 0.1;
    const chargableAmount = repairAmount + vatAmount;
    repairAmountInfo.innerHTML = isNaN(repairAmount) ? "-" : numberWithCommas(parseInt(repairAmount));
    vatInfo.innerHTML = isNaN(vatAmount) ? "-" : numberWithCommas(parseInt(vatAmount));
    chargableAmountInfo.innerHTML = isNaN(chargableAmount) ? "-" : numberWithCommas(parseInt(chargableAmount));
  };
}

function chargeModalPreprocess(e) {}
function chargeModalPostprocess(e, modal) {
  const wageAmountInput = modal.querySelector("#id_wage_amount");
  const componentAmountInput = modal.querySelector("#id_component_amount");
  const repairAmountInfo = modal.querySelector(".repair_amount_info");
  const vatInfo = modal.querySelector(".vat_info");
  const chargableAmountInfo = modal.querySelector(".chargable_amount_info");
  const setChargeInfo = setChargeInfoFactory(wageAmountInput, componentAmountInput, repairAmountInfo, vatInfo, chargableAmountInfo);
  wageAmountInput.addEventListener("input", setChargeInfo);
  componentAmountInput.addEventListener("input", setChargeInfo);
  setChargeInfo();
}

const chargeButtonHandler = modalFuctionFactory(chargeModalPreprocess, chargeModalPostprocess);

for (let i = 0; i < chargeButtons.length; i++) {
  chargeButtons[i].addEventListener("click", chargeButtonHandler);
}

export {setChargeInfoFactory};
