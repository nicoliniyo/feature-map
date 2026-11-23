function render() {
  const name = (location.hash.replace("#/", "") || "dashboard");
  const view = window.views[name] ? name : "dashboard";
  document.getElementById("view").innerHTML = window.views[view]();
  window.bind[view]();
}
window.addEventListener("hashchange", render); render();
