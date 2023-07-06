import {setSettlementAmountInfoFactory} from "./modal/came_out.js";
import {setChargeInfoFactory} from "./modal/charge.js";
import {setRateInfoFactory} from "./modal/deposit.js";
import {getIdOfField} from "./modal/modal.js";

const totalNumberOfEditOrderForms = document.querySelectorAll(".edit_order_form").length;
const totlaNumberOfEditOrderSet = totalNumberOfEditOrderForms / 4;

setRateInfoFactory;

for (let i = 0; i < totlaNumberOfEditOrderSet; i++) {
  const faultRatioInput = document.querySelector(`#${getIdOfField("order", "fault_ratio", i)}`);
  const indemnityAmountInput = document.querySelector(`#${getIdOfField("payment", "indemnity_amount", i)}`);
  const discountAmountInput = document.querySelector(`#${getIdOfField("payment", "discount_amount", i)}`);
  const settlementAmountInfo = document.querySelectorAll(".settlement_amount_info")[i];
  const wageAmountInput = document.querySelector(`#${getIdOfField("charge", "wage_amount", i)}`);
  const componentAmountInput = document.querySelector(`#${getIdOfField("charge", "component_amount", i)}`);
  const chargeData = document.querySelectorAll(".charge_data")[i];
  const repairAmountInfo = document.querySelectorAll(".repair_amount_info")[i];
  const vatInfo = document.querySelectorAll(".vat_info")[i];
  const chargableAmountInfo = document.querySelectorAll(".chargable_amount_info")[i];
  const chargeAmountInfo = document.querySelectorAll(".charge_amount_info")[i];
  const depositAmountInput = document.querySelector(`#${getIdOfField("deposit", "deposit_amount", i)}`);
  const paymentRateInfo = document.querySelectorAll(".payment_rate_info")[i];
  const curRateInfo = document.querySelectorAll(".cut_rate_info")[i];

  const setSettlementAmount = setSettlementAmountInfoFactory({}, settlementAmountInfo, indemnityAmountInput, discountAmountInput);
  indemnityAmountInput.addEventListener("input", setSettlementAmount);
  discountAmountInput.addEventListener("input", setSettlementAmount);
  setSettlementAmount();

  const setChargeInfo = setChargeInfoFactory(
    wageAmountInput,
    componentAmountInput,
    chargeData,
    repairAmountInfo,
    vatInfo,
    chargableAmountInfo,
    chargeAmountInfo
  );
  wageAmountInput.addEventListener("input", setChargeInfo);
  componentAmountInput.addEventListener("input", setChargeInfo);
  setChargeInfo();
}
