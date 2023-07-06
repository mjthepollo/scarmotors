import {setSettlementAmountInfoFactory} from "./modal/came_out.js";
import {setChargeInfoFactory} from "./modal/charge.js";
import {setRateInfoFactory} from "./modal/deposit.js";
import {getIdOfField} from "./modal/modal.js";

const totalNumberOfEditOrderForms = document.querySelectorAll(".edit_order_form").length;
const totlaNumberOfEditOrderSet = totalNumberOfEditOrderForms / 4;

function callEveryArgumentsFactory() {
  const functions = arguments;
  return function () {
    for (let i = 0; i < functions.length; i++) {
      functions[i]();
    }
  };
}
function setPaymentDataFactory(paymentData, faultRatioInput, indemnityAmountInput, refundAmountInput) {
  return function () {
    const faultRatio = parseInt(faultRatioInput.value);
    const indemnityAmount = parseInt(indemnityAmountInput.value);
    const refundAmount = parseInt(refundAmountInput.value);
    paymentData.dataset.fault_ratio = isNaN(faultRatio) ? 100 : faultRatio;
    paymentData.dataset.indemnity_amount = isNaN(indemnityAmount) ? 0 : indemnityAmount;
    paymentData.dataset.refund_amount = isNaN(refundAmount) ? 0 : refundAmount;
  };
}

function setChargeAmountDataFactory(chargeAmountData, wageAmountInput, componentAmountInput, paymentData) {
  return function () {
    const wageAmount = parseInt(wageAmountInput.value);
    const componentAmount = parseInt(componentAmountInput.value);
    const repairAmount = wageAmount + componentAmount;
    const faultRatio = parseInt(paymentData.dataset.fault_ratio);
    const chargableAmount = (repairAmount * faultRatio * 1.1) / 100;
    const indemnityAmount = parseInt(paymentData.dataset.indemnity_amount);
    const refundAmount = parseInt(paymentData.dataset.refund_amount);
    let chargeAmount = chargableAmount - indemnityAmount + refundAmount;
    if (isNaN(chargableAmount)) {
      chargeAmountData.dataset.charge_amount = "";
    } else {
      chargeAmount = chargeAmount > 0 ? chargeAmount : 0;
      chargeAmountData.dataset.charge_amount = chargeAmount;
    }
  };
}

for (let i = 0; i < totlaNumberOfEditOrderSet; i++) {
  const faultRatioInput = document.querySelector(`#${getIdOfField("order", "fault_ratio", i)}`);
  const indemnityAmountInput = document.querySelector(`#${getIdOfField("payment", "indemnity_amount", i)}`);
  const discountAmountInput = document.querySelector(`#${getIdOfField("payment", "discount_amount", i)}`);
  const refundAmountInput = document.querySelector(`#${getIdOfField("payment", "refund_amount", i)}`);
  const settlementAmountInfo = document.querySelectorAll(".settlement_amount_info")[i];
  const wageAmountInput = document.querySelector(`#${getIdOfField("charge", "wage_amount", i)}`);
  const componentAmountInput = document.querySelector(`#${getIdOfField("charge", "component_amount", i)}`);
  const paymentData = document.querySelectorAll(".payment_data")[i];
  const repairAmountInfo = document.querySelectorAll(".repair_amount_info")[i];
  const vatInfo = document.querySelectorAll(".vat_info")[i];
  const chargableAmountInfo = document.querySelectorAll(".chargable_amount_info")[i];
  const chargeAmountInfo = document.querySelectorAll(".charge_amount_info")[i];
  const chargeAmountData = document.querySelectorAll(".charge_amount_data")[i];
  const depositAmountInput = document.querySelector(`#${getIdOfField("deposit", "deposit_amount", i)}`);
  const paymentRateInfo = document.querySelectorAll(".payment_rate_info")[i];
  const curRateInfo = document.querySelectorAll(".cut_rate_info")[i];

  const setSettlementAmount = setSettlementAmountInfoFactory(settlementAmountInfo, indemnityAmountInput, discountAmountInput);
  const setPaymentData = setPaymentDataFactory(paymentData, faultRatioInput, indemnityAmountInput, refundAmountInput);
  const setChargeAmountData = setChargeAmountDataFactory(chargeAmountData, wageAmountInput, componentAmountInput, paymentData);
  const setChargeInfo = setChargeInfoFactory(
    wageAmountInput,
    componentAmountInput,
    paymentData,
    repairAmountInfo,
    vatInfo,
    chargableAmountInfo,
    chargeAmountInfo
  );
  const setRateInfo = setRateInfoFactory(chargeAmountData, depositAmountInput, paymentRateInfo, curRateInfo);

  const handleAll = callEveryArgumentsFactory(setPaymentData, setChargeAmountData, setChargeInfo, setRateInfo, setSettlementAmount);
  faultRatioInput.addEventListener("input", handleAll);
  indemnityAmountInput.addEventListener("input", handleAll);
  discountAmountInput.addEventListener("input", handleAll);
  refundAmountInput.addEventListener("input", handleAll);
  wageAmountInput.addEventListener("input", handleAll);
  componentAmountInput.addEventListener("input", handleAll);
  depositAmountInput.addEventListener("input", handleAll);
  handleAll();
}
