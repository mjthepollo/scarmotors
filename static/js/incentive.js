import {numberWithCommas} from "./utility.js";

const incentiveChecks = document.querySelectorAll(".incentive_check");
const incentivePaids = document.querySelectorAll(".incentive_paid");

const incentiveInfo = document.querySelector("#incentive_info");
const turnoverInfo = document.querySelector("#turnover_info");

function setIncentiveInfo(e) {
  let totalIncentive = 0;
  let totalTurnover = 0;
  for (let i = 0; i < incentiveChecks.length; i++) {
    const incentivePaidCheckbox = incentiveChecks[i].querySelector("input[type='checkbox']");
    if (incentivePaidCheckbox.checked) {
      totalIncentive += parseInt(incentiveChecks[i].dataset.incentive);
      totalTurnover += parseInt(incentiveChecks[i].dataset.turnover);
    }
  }
  incentiveInfo.innerText = numberWithCommas(totalIncentive);
  turnoverInfo.innerText = numberWithCommas(totalTurnover);
}

function clickIncentivePaid(e) {
  console.log("SEX");
  const incentivePaidCheck = e.currentTarget;
  const incentivePaidCheckInput = incentivePaidCheck.querySelector("input[type='checkbox']");
  const siblingIncentiveCheck = incentivePaidCheck.parentElement.querySelector(".incentive_check");
  const siblingIncentiveCheckInput = siblingIncentiveCheck.querySelector("input[type='checkbox']");
  console.log(incentivePaidCheckInput, siblingIncentiveCheckInput);
  console.log(incentivePaidCheckInput.checked, siblingIncentiveCheckInput.checked);
  siblingIncentiveCheckInput.checked = incentivePaidCheckInput.checked;
  console.log(incentivePaidCheckInput.checked, siblingIncentiveCheckInput.checked);
  setIncentiveInfo();
}

for (let i = 0; i < incentiveChecks.length; i++) {
  incentiveChecks[i].addEventListener("click", setIncentiveInfo);
  incentivePaids[i].addEventListener("click", clickIncentivePaid);
}
setIncentiveInfo();
