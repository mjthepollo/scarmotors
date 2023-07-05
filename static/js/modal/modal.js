function getIdOfField(prefix, field, index) {
  return `id_${prefix}-${index}-${field}`;
}

function getNumberOfForms(prefix, modal) {
  const totalForm = modal.querySelector(`input[name=${prefix}-TOTAL_FORMS]`);
  return parseInt(totalForm.value);
}

function closeModal(e) {
  const modal = e.currentTarget.closest(".custom_modal");
  modal.remove();
}

function handleDeleteButton(e) {
  if (window.confirm("정말로 삭제하시겠습니까?")) {
    const redirectUrl = e.currentTarget.dataset.redirect_url;
    window.location.href = redirectUrl;
  }
}

function modalFuctionFactory(preprocessFunction, postprocessFunction) {
  return function (e) {
    preprocessFunction(e);
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
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, "text/html");
        const modal = doc.documentElement.querySelector("div.custom_modal");
        document.body.appendChild(modal);
        const closeButtons = modal.querySelectorAll(".close_modal");
        for (let i = 0; i < closeButtons.length; i++) {
          closeButtons[i].addEventListener("click", closeModal);
        }
        const deleteButton = modal.querySelector(".delete_button");
        if (deleteButton) {
          deleteButton.addEventListener("click", handleDeleteButton);
        }
        postprocessFunction(e, modal);
      })
      .catch((e) => {
        alert(e);
      });
  };
}

export {getIdOfField, getNumberOfForms, modalFuctionFactory};
