document.addEventListener("DOMContentLoaded", function () {
  const makeModels = {
    Honda: ["Accord", "Civic", "CR-V"],
    Lexus: ["GX470", "RX350"],
    Nissan: ["Sentra", "Altima"],
    Volkswagen: ["Jetta", "Golf"]
  };

  const makeButton = document.getElementById("makeButton");
  const makeItems = makeButton.nextElementSibling.querySelectorAll(".dropdown-item");
  const modelButton = document.getElementById("modelButton");
  const modelDropdown = document.getElementById("modelDropdown");

  makeItems.forEach(item => {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      const selectedMake = this.textContent.trim();
      makeButton.textContent = selectedMake;

      // Clear previous model options
      modelDropdown.innerHTML = "";

      // Add new model options
      const models = makeModels[selectedMake] || [];
      models.forEach(model => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.classList.add("dropdown-item");
        a.href = "#";
        a.textContent = model;
        a.addEventListener("click", function (e) {
          e.preventDefault();
          modelButton.textContent = model;
        });
        li.appendChild(a);
        modelDropdown.appendChild(li);
      });

      // Reset model button text
      modelButton.textContent = "Model";
    });
  });
});
