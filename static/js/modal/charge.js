import {numberWithCommas} from "../utility.js";
import {modalFuctionFactory} from "./modal.js";

const chargeButtons = document.querySelectorAll(".charge_button");

function setAdditionalInfoFactory(e, modal) {
  return function (e) {
    const wageAmountInput = modal.querySelector("#id_wage_amount");
    const componentAmountInput = modal.querySelector("#id_component_amount");
    const chargeData = modal.querySelector(".charge_data");
    const wageAmount = isNaN(parseInt(wageAmountInput.value)) ? 0 : parseInt(wageAmountInput.value);
    const componentAmount = isNaN(parseInt(componentAmountInput.value)) ? 0 : parseInt(componentAmountInput.value);
    const repairAmount = wageAmount + componentAmount;
    const vatAmount = repairAmount * 0.1;
    const faultRatio = (chargeData.dataset.fault_ratio ? parseFloat(chargeData.dataset.fault_ratio) : 100) / 100;
    const chargableAmount = faultRatio * (repairAmount + vatAmount);
    const indemnityAmount = parseFloat(chargeData.dataset.indemnity_amount);
    const refundAmount = parseFloat(chargeData.dataset.refund_amount);
    const chargeAmount = chargableAmount - indemnityAmount + refundAmount;

    const repairAmountInfo = modal.querySelector(".repair_amount_info");
    const vatInfo = modal.querySelector(".vat_info");
    const chargableAmountInfo = modal.querySelector(".chargable_amount_info");
    const chargeAmountInfo = modal.querySelector(".charge_amount_info");
    repairAmountInfo.innerHTML = isNaN(repairAmount) ? "-" : numberWithCommas(parseInt(repairAmount));
    vatInfo.innerHTML = isNaN(vatAmount) ? "-" : numberWithCommas(parseInt(vatAmount));
    chargableAmountInfo.innerHTML = isNaN(chargableAmount) ? "-" : numberWithCommas(parseInt(chargableAmount));
    chargeAmountInfo.innerHTML = isNaN(chargeAmount) ? "-" : numberWithCommas(parseInt(chargeAmount));
  };
}

function chargeModalPreprocess(e) {}
function chargeModalPostprocess(e, modal) {
  const wageAmountInput = modal.querySelector("#id_wage_amount");
  const componentAmountInput = modal.querySelector("#id_component_amount");
  const setAdditionalInfo = setAdditionalInfoFactory(e, modal);
  wageAmountInput.addEventListener("input", setAdditionalInfo);
  componentAmountInput.addEventListener("input", setAdditionalInfo);
  setAdditionalInfo();
}

const chargeButtonHandler = modalFuctionFactory(chargeModalPreprocess, chargeModalPostprocess);

for (let i = 0; i < chargeButtons.length; i++) {
  chargeButtons[i].addEventListener("click", chargeButtonHandler);
}
