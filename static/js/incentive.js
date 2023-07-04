import {numberWithCommas} from "./utility.js";

const incentiveChecks = document.querySelectorAll(".incentive_check");

const incentiveInfo = document.querySelector("#incentive_info");
const turnoverInfo = document.querySelector("#turnover_info");

function setIncentiveInfo(e) {
  let totalIncentive = 0;
  let totalTurnover = 0;
  for (let i = 0; i < incentiveChecks.length; i++) {
    const incentivePaidCheckbox = incentiveChecks[i].querySelector("input");
    if (incentivePaidCheckbox.checked) {
      totalIncentive += parseInt(incentiveChecks[i].dataset.incentive);
      totalTurnover += parseInt(incentiveChecks[i].dataset.turnover);
    }
  }
  incentiveInfo.innerText = numberWithCommas(totalIncentive);
  turnoverInfo.innerText = numberWithCommas(totalTurnover);
}

for (let i = 0; i < incentiveChecks.length; i++) {
  incentiveChecks[i].addEventListener("click", setIncentiveInfo);
}
setIncentiveInfo();

const incentiveNotes = document.querySelectorAll(".incentive_note");

function showIncentiveNotes(e) {
  const incentiveNote = e.currentTarget.querySelector(".incentive_note");
  incentiveNote.classList.remove("hidden");
}

function hideIncentiveNotes(e) {
  const incentiveNote = e.currentTarget.querySelector(".incentive_note");
  incentiveNote.classList.add("hidden");
}

console.log(incentiveNotes);
for (let i = 0; i < incentiveNotes.length; i++) {
  incentiveNotes[i].parentElement.addEventListener("mouseover", showIncentiveNotes);
  incentiveNotes[i].parentElement.addEventListener("mouseout", hideIncentiveNotes);
}
