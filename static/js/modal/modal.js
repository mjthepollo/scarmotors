function closeModal(e) {
  const modal = e.currentTarget.closest(".custom_modal");
  modal.remove();
}

function modalFuctionFactory(preprocessFunction, postprocessFunction) {
  return function (e) {
    const url = e.currentTarget.dataset.modal_url;
    fetch(url)
      .then((data) => {
        if (data.status == 200) {
          return data.text();
        } else {
          throw Error("서버응답에 오류가 있습니다.");
        }
      })
      .then((html) => {
        preprocessFunction(e);
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, "text/html");
        const modal = doc.documentElement.querySelector("div.custom_modal");
        document.body.appendChild(modal);
        const closeButtons = modal.querySelectorAll(".close_modal");
        for (let i = 0; i < closeButtons.length; i++) {
          closeButtons[i].addEventListener("click", closeModal);
        }
        postprocessFunction(e);
      })
      .catch((e) => {
        alert(e);
      });
  };
}

export {modalFuctionFactory};
