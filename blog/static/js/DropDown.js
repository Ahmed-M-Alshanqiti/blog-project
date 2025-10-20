document.addEventListener("DOMContentLoaded", () => {

  document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    toggle.addEventListener("click", (e) => {
      const dropdown = e.target.closest(".dropdown");
      dropdown.classList.toggle("show");
    });
  });


  window.addEventListener("click", (e) => {
    if (!e.target.closest(".dropdown")) {
      document.querySelectorAll(".dropdown").forEach(d => d.classList.remove("show"));
    }
  });
});
