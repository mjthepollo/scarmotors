const pageNumberInputBox = document.querySelector("#page_number_input_box");
const pageNumberButton = document.querySelector("#page_number_button");
const pageNumberMoveButton = document.querySelector("#page_number_move_button");
const pageNumberCancelButton = document.querySelector("#page_number_cancel_button");
const pageNumberInput = document.querySelector("input#page_number_input");
const urlWithoutPage = pageNumberInputBox.dataset.url_without_page;

console.log(urlWithoutPage);

function handlePageNumberButtonClick(e) {
  pageNumberInputBox.classList.remove("inactive");
  pageNumberInput.focus();
  pageNumberInput.select();
}
function handlePageNumberMoveButtonClick(e) {
  const pageNumber = pageNumberInput.value;
  const url = urlWithoutPage + pageNumber;
  window.location.href = url;
}

function handlePageNumberCancelButtonClick(e) {
  pageNumberInputBox.classList.add("inactive");
}

pageNumberButton.addEventListener("click", handlePageNumberButtonClick);
pageNumberMoveButton.addEventListener("click", handlePageNumberMoveButtonClick);
pageNumberCancelButton.addEventListener("click", handlePageNumberCancelButtonClick);
