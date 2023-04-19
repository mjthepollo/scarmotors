function getFontSize(element) {
  return parseInt(window.getComputedStyle(element).fontSize.replace("px", ""));
}

function getLineNumber(element) {
  return parseInt(element.clientHeight / getFontSize(element));
}

function adjustFontSize(element) {
  while (getLineNumber(element) != 1) {
    const adjustedFontSize = getFontSize(element) - 1;
    element.style.fontSize = `${adjustedFontSize}px`;
  }
}

const questionContents = document.querySelectorAll(".question_content");
console.log(questionContents);
for (var i = 0; i < questionContents.length; i++) {
  adjustFontSize(questionContents[i]);
}
