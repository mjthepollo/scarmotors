import {modalFuctionFactory} from "./modal.js";

const depositButtons = document.querySelectorAll(".deposit_button");

function setRateInfoFactory(e, chargeAmount, depositAmountInput, paymentRateInfo, curRateInfo) {
  return function (e) {
    const depositAmout = isNaN(depositAmountInput.value) ? 0 : parseInt(depositAmountInput.value);
    const paymentRate = parseInt((depositAmout / chargeAmount) * 100);
    paymentRateInfo.innerHTML = isNaN(paymentRate) ? "-" : paymentRate.toString() + "%";
    curRateInfo.innerHTML = isNaN(paymentRate) ? "-" : (100 - paymentRate).toString() + "%";
  };
}

function depositModalPreprocess(e) {}
function depositModalPostprocess(e, modal) {
  let chargeAmount = parseInt(modal.querySelector("#charge_amount").value);
  chargeAmount = isNaN(chargeAmount) ? 0 : chargeAmount;
  const depositAmountInput = modal.querySelector("#id_deposit_amount");
  const paymentRateInfo = modal.querySelector(".payment_rate_info");
  const curRateInfo = modal.querySelector(".cut_rate_info");
  const setRateInfo = setRateInfoFactory(e, chargeAmount, depositAmountInput, paymentRateInfo, curRateInfo);
  depositAmountInput.addEventListener("input", setRateInfo);
  setRateInfo();
}

const depositButtonHandler = modalFuctionFactory(depositModalPreprocess, depositModalPostprocess);

for (let i = 0; i < depositButtons.length; i++) {
  depositButtons[i].addEventListener("click", depositButtonHandler);
}
