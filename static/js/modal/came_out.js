import {getIdOfField, getNumberOfForms, modalFuctionFactory, numberWithCommas} from "./modal.js";

const cameOutButtons = document.querySelectorAll(".came_out_button");
const prefix = "payment";

function setSettlementAmountInfoFactory(e, settlementAmountInfo, indemnityAmountInput, discountAmountInput) {
  return function (e) {
    const indemnityAmount = parseInt(indemnityAmountInput.value);
    const discountAmount = isNaN(parseInt(discountAmountInput.value)) ? 0 : parseInt(discountAmountInput.value);
    const settlementAmount = indemnityAmount - discountAmount;
    settlementAmountInfo.innerHTML = isNaN(settlementAmount) ? "-" : numberWithCommas(settlementAmount);
  };
}

function cameOutModalPreprocess(e) {}
function cameOutModalPostprocess(e, modal) {
  const numberOfForms = getNumberOfForms(prefix, modal);
  const settlementAmountInfos = modal.querySelectorAll(".settlement_amount_info");
  for (let i = 0; i < numberOfForms; i++) {
    const settlementAmountInfo = settlementAmountInfos[i];
    const indemnityAmountInput = modal.querySelector(`#${getIdOfField(prefix, "indemnity_amount", i)}`);
    const discountAmountInput = modal.querySelector(`#${getIdOfField(prefix, "discount_amount", i)}`);

    const setSettlementAmount = setSettlementAmountInfoFactory(e, settlementAmountInfo, indemnityAmountInput, discountAmountInput);
    indemnityAmountInput.addEventListener("input", setSettlementAmount);
    discountAmountInput.addEventListener("input", setSettlementAmount);
    setSettlementAmount();
  }
}

const cameOutButtonHandler = modalFuctionFactory(cameOutModalPreprocess, cameOutModalPostprocess);

for (let i = 0; i < cameOutButtons.length; i++) {
  cameOutButtons[i].addEventListener("click", cameOutButtonHandler);
}
