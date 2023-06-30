import {modalFuctionFactory} from "./modal.js";

const cameOutButtons = document.querySelectorAll(".came_out_button");
const prefix = "payment";

function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function getIdOfField(prefix, field, index) {
  return `id_${prefix}-${index}-${field}`;
}

function getNumberOfForms(prefix, modal) {
  const totalForm = modal.querySelector(`input[name=${prefix}-TOTAL_FORMS]`);
  return parseInt(totalForm.value);
}

function setSettlementAmountInfoFactory(e, settlementAmountInfo, indemnityAmountInfo, discontAmountInput) {
  return function (e) {
    const indemnityAmount = parseInt(indemnityAmountInfo.value);
    const discontAmount = isNaN(parseInt(discontAmountInput.value)) ? 0 : parseInt(discontAmountInput.value);
    const settlementAmount = indemnityAmount - discontAmount;
    settlementAmountInfo.innerHTML = isNaN(settlementAmount) ? (settlementAmountInfo.innerHTML = "-") : numberWithCommas(settlementAmount);
  };
}

function cameOutModalPreprocess(e) {}
function cameOutModalPostprocess(e, modal) {
  const numberOfForms = getNumberOfForms(prefix, modal);
  console.log(numberOfForms);
  const settlementAmountInfos = modal.querySelectorAll(".settlement_amount_info");
  console.log(settlementAmountInfos);
  for (let i = 0; i < numberOfForms; i++) {
    const settlementAmountInfo = settlementAmountInfos[i];
    console.log(getIdOfField(prefix, "indemnity_amount", i));
    console.log(getIdOfField(prefix, "discount_amount", i));
    const indemnityAmountInput = modal.querySelector(`#${getIdOfField(prefix, "indemnity_amount", i)}`);
    const discontAmountInput = modal.querySelector(`#${getIdOfField(prefix, "discount_amount", i)}`);
    indemnityAmountInput.addEventListener("input", setSettlementAmountInfoFactory(e, settlementAmountInfo, indemnityAmountInput, discontAmountInput));
    discontAmountInput.addEventListener("input", setSettlementAmountInfoFactory(e, settlementAmountInfo, indemnityAmountInput, discontAmountInput));
    setSettlementAmountInfoFactory(e, settlementAmountInfo, indemnityAmountInput, discontAmountInput)();
  }
}

const cameOutButtonHandler = modalFuctionFactory(cameOutModalPreprocess, cameOutModalPostprocess);

for (let i = 0; i < cameOutButtons.length; i++) {
  cameOutButtons[i].addEventListener("click", cameOutButtonHandler);
}
