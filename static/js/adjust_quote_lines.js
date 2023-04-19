function getFontSize(element) {
  return parseInt(window.getComputedStyle(element).fontSize.replace("px", ""));
}

function getLineNumber(element) {
  const lineHeight = parseInt(window.getComputedStyle(element).lineHeight.replace("px", ""));
  return parseInt(element.clientHeight / lineHeight);
}

function adjustFontSize(element) {
  while (getLineNumber(element) > 15) {
    const adjustedFontSize = getFontSize(element) - 1;
    element.style.fontSize = `${adjustedFontSize}px`;
    if (adjustedFontSize < 10) return;
  }
}

const quoteContent = document.querySelector("a.content");
adjustFontSize(quoteContent);
