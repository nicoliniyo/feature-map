const store = JSON.parse(localStorage.getItem("settings") || '{"theme":"light","digest":"weekly"}');
window.views = {
  dashboard: () => `<h1>Dashboard</h1><div class="card">Open tickets: 12</div><div class="card">Revenue: $4,210</div>`,
  profile: () => `<h1>Profile</h1><label>Name</label><input id="name" value="Ada">
    <div class="actions"><button id="profile-save">Update profile</button></div>`,
  settings: () => `<h1>Settings</h1>
    <label for="theme">Theme</label><select id="theme"><option>light</option><option>dark</option></select>
    <label for="digest">Email digest</label><select id="digest"><option>daily</option><option>weekly</option><option>never</option></select>
    <p style="height:30vh"></p>
    <div class="actions"><button id="settings-save" data-testid="settings-save">Save</button></div>`,
};
window.bind = {
  settings: () => {
    document.getElementById("theme").value = store.theme;
    document.getElementById("digest").value = store.digest;
    document.getElementById("settings-save").addEventListener("click", () => {
      store.theme = document.getElementById("theme").value;
      store.digest = document.getElementById("digest").value;
      localStorage.setItem("settings", JSON.stringify(store));
      toast("Settings saved");
    });
  },
  profile: () => document.getElementById("profile-save").addEventListener("click", () => toast("Profile updated")),
  dashboard: () => {},
};
