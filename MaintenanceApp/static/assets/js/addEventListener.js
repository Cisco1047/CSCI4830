document.addEventListener("DOMContentLoaded", function () {
  const dropdowns = document.querySelectorAll(".dropdown");

  dropdowns.forEach(dropdown => {
    const button = dropdown.querySelector(".dropdown-toggle");
    const items = dropdown.querySelectorAll(".dropdown-item");

    items.forEach(item => {
      item.addEventListener("click", function (event) {
        event.preventDefault();
        button.textContent = this.textContent;
      });
    });
  });
});
