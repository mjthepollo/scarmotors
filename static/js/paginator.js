const pageNumberInput = document.querySelector("input#page_number_input");
const urlWithoutPage = pageNumberInput.dataset.url_without_page;

console.log(urlWithoutPage);
function goToPage(e) {
  const pageNumber = pageNumberInput.value;
  const url = urlWithoutPage + pageNumber;
  console.log(pageNumber, url);
  window.location.href = url;
}
// goToPage is called when the user presses enter in the input field
