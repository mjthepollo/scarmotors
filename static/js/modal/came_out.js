import {numberWithCommas} from "../utility.js";
import {getIdOfField, modalFuctionFactory} from "./modal.js";

const cameOutButtons = document.querySelectorAll(".came_out_button");
const prefix = "payment";

function setSettlementAmountInfoFactory(settlementAmountInfo, indemnityAmountInput, discountAmountInput) {
  return function () {
    const indemnityAmount = parseInt(indemnityAmountInput.value);
    const discountAmount = isNaN(parseInt(discountAmountInput.value)) ? 0 : parseInt(discountAmountInput.value);
    const settlementAmount = indemnityAmount - discountAmount;
    settlementAmountInfo.innerHTML = isNaN(settlementAmount) ? "-" : numberWithCommas(settlementAmount);
  };
}

function cameOutModalPreprocess(e) {}
function cameOutModalPostprocess(e, modal) {
  const numberOfForms = document.querySelectorAll(".payment_form").length;
  const settlementAmountInfos = modal.querySelectorAll(".settlement_amount_info");
  for (let i = 0; i < numberOfForms; i++) {
    const settlementAmountInfo = settlementAmountInfos[i];
    const indemnityAmountInput = modal.querySelector(`#${getIdOfField(prefix, "indemnity_amount", i)}`);
    const discountAmountInput = modal.querySelector(`#${getIdOfField(prefix, "discount_amount", i)}`);

    const setSettlementAmount = setSettlementAmountInfoFactory(settlementAmountInfo, indemnityAmountInput, discountAmountInput);
    indemnityAmountInput.addEventListener("input", setSettlementAmount);
    discountAmountInput.addEventListener("input", setSettlementAmount);
    setSettlementAmount();
  }
}

const cameOutButtonHandler = modalFuctionFactory(cameOutModalPreprocess, cameOutModalPostprocess);

for (let i = 0; i < cameOutButtons.length; i++) {
  cameOutButtons[i].addEventListener("click", cameOutButtonHandler);
}

export {setSettlementAmountInfoFactory};
