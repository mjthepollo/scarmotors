const cameOutButtons = document.querySelectorAll(".came_out_button");

function closeModal(e) {
  console.log("closeModal");
  const modal = e.currentTarget.closest(".custom_modal");
  modal.remove();
}

function cameOutButtonHandler(e) {
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
        console.log("ADD EVENT LISTENR!");
        closeButtons[i].addEventListener("click", closeModal);
      }
    })
    .catch((e) => {
      alert(e);
    });
}

for (let i = 0; i < cameOutButtons.length; i++) {
  cameOutButtons[i].addEventListener("click", cameOutButtonHandler);
  console.log("HELLO WORLD!");
}
