window.addEventListener("DOMContentLoaded", () => {
  const wrappers = document.querySelector(".archive");

  wrappers.addEventListener("click", (e) => {
    target = e.target;
    if (target && target.matches(".fold-button")) {
      if (target.parentElement.classList.contains("folded")) {
        target.innerHTML = "Свернуть";
        target.parentElement.classList.remove("folded");
      } else {
        console.log(target.parentElement);
        target.innerHTML = "Развернуть";
        target.parentElement.classList.add("folded");
      }
    }
  });

  //   for (let i = 0; i < foldBtns.length; i++) {
  //     foldBtns[i].addEventListener("click", (e) => {
  //       if (e.target.className == "fold-button folded") {
  //         e.target.innerHTML = "свернуть";
  //         e.target.className = "fold-button";
  //         var displayState = "block";
  //       } else {
  //         e.target.innerHTML = "развернуть";
  //         e.target.className = "fold-button folded";
  //         var displayState = "none";
  //       }
  //       e.target.parentElement.getElementsByClassName(
  //         "article-author"
  //       )[0].style.display = displayState;
  //       e.target.parentElement.getElementsByClassName(
  //         "article-created-date"
  //       )[0].style.display = displayState;
  //       e.target.parentElement.getElementsByClassName(
  //         "article-text"
  //       )[0].style.display = displayState;
  //     });
  //   }
});
