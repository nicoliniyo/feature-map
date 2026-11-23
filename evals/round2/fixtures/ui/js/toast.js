window.toast = function (msg) {
  const el = document.createElement("div");
  el.className = "toast"; el.setAttribute("role", "status"); el.textContent = msg;
  document.getElementById("toast-root").appendChild(el);
  setTimeout(() => el.remove(), 4000);
};
