"use strict";

const membersTable = document.querySelector("#members-table");
const btnSchool = document.querySelectorAll(".btn__tt");
const btnGroupNumber = document.getElementById("btn-show-number");
const inputGroupNumber = document.getElementById("read-group-number");

// Gets a member list from server side
async function fetchMembers() {
  try {
    const response = await fetch("http://127.0.0.1:5000/request_members", {
      method: "POST",
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}
// Deletes a chore by id
async function deleteChore(id) {
  fetch("http://127.0.0.1:5000/delete_chores", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(id),
  })
    .then(function (response) {
      return response.text();
    })
    .catch((err) => {
      console.log(err);
    });
}

// Send a chore id to be marked off as completed
async function choreCheck(id) {
  fetch("http://127.0.0.1:5000/complete_chore", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(id),
  })
    .then(function (response) {
      return response.text();
    })
    .catch((err) => {
      console.log(err);
    });
}

// Delete a member by sending name to a server
async function deleteMembers(name) {
  fetch("http://127.0.0.1:5000/delete_member", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(name),
  })
    .then(function (response) {
      return response.text();
    })
    .catch((err) => {
      console.log(err);
    });
}

// Delete admin
async function deleteAdmin(name) {
  fetch("http://127.0.0.1:5000/delete_admin", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(name),
  })
    .then(function (response) {
      return response.text();
    })
    .catch((err) => {
      console.log(err);
    });
}

// Refresh page on call
function refreshPage() {
  fetch("http://127.0.0.1:5000/refresh", {
    method: "POST",
  }).then(function () {
    window.location.reload(true);
  });
}
// Create a table with members and delete button for each member of a group
async function renderMembers() {
  const members = await fetchMembers();
  members.forEach(function (m) {
    const tableRow = document.createElement("tr");
    const name = document.createElement("td");
    const password = document.createElement("td");
    const slot = document.createElement("td");
    const btn = document.createElement("button");

    name.setAttribute("class", "align-middle text-start");
    name.innerHTML = m.name;

    password.setAttribute("class", "align-middle text-start");
    password.innerHTML = m.password;

    slot.setAttribute("class", "text-center");
    btn.setAttribute("class", "btn btn__delete");
    btn.setAttribute("data-name", `${m.name}`);
    btn.setAttribute("type", "button");
    btn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" class="bi bi-x-circle" viewBox="0 0 16 16">
      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
      <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
      </svg>`;
    slot.appendChild(btn);
    slot.classList.add("align-middle");

    tableRow.appendChild(name);
    tableRow.appendChild(password);
    tableRow.appendChild(slot);
    membersTable.appendChild(tableRow);
  });
  // Select delete member buttons
  const btnDelete = document.querySelectorAll(".btn__delete");
  btnDelete.forEach(function (button) {
    button.addEventListener("click", function (e) {
      const name = e.currentTarget.getAttribute("data-name");
      deleteMembers(name);
      location.reload();
    });
  });
}

// Complete chore button
async function memberCompleteChore() {
  const btnCompleteChore = document.querySelectorAll(".btn__complete__chore");
  btnCompleteChore.forEach(function (b) {
    b.addEventListener("click", function (e) {
      const id = e.currentTarget.getAttribute("data-id");
      choreCheck(id);
      refreshPage();
    });
  });
}

// Delete chore button
async function userChoreDelteBtn() {
  const btnDeleteChore = document.querySelectorAll(".btn__del__chore");

  btnDeleteChore.forEach(function (b) {
    b.addEventListener("click", function (e) {
      const id = e.currentTarget.getAttribute("data-id");
      deleteChore(id);
      location.reload();
    });
  });
}

// Render member time table
async function renderTables() {
  const members = await fetchMembers();
  const table = document.querySelector("#table-main");
  // Create time table for each member
  members.forEach(function (m, k) {
    const tableBody = document.createElement("tbody");
    tableBody.classList.add("border-1");
    tableBody.classList.add("members__table");
    tableBody.setAttribute("colspan", "4");
    tableBody.setAttribute("data-name", `${m.name}`);

    m.time_table.forEach(function (d, i) {
      const userTable = document.createElement("tr");
      const subjectIndex = document.createElement("td");
      subjectIndex.classList.add("text-start");
      subjectIndex.innerHTML = `${i + 1}.`;
      userTable.appendChild(subjectIndex);

      d.forEach(function (s) {
        const subject = document.createElement("td");
        subject.classList.add("text-center");
        subject.innerHTML = s;
        userTable.appendChild(subject);
      });
      tableBody.appendChild(userTable);
    });
    // Set only 1 table to be visable
    if (k === 0) {
      tableBody.style.display = "table-row-group";
    } else {
      tableBody.style.display = "none";
    }
    table.appendChild(tableBody);
  });
  // Button for changing table view
  const membersTable = document.querySelectorAll(".members__table");

  btnSchool.forEach(function (button) {
    button.addEventListener("click", function (e) {
      const name = e.currentTarget.getAttribute("data-name");
      membersTable.forEach(function (t) {
        const table = t.getAttribute("data-name");
        if (name != table) {
          t.style.display = "none";
        } else {
          t.style.display = "table-row-group";
        }
      });
    });
  });
}

const btnDeleteAdmin = document.querySelectorAll(".btn__remove__admin");
btnDeleteAdmin.forEach(function (button) {
  button.addEventListener("click", function (e) {
    const name = e.currentTarget.getAttribute("data-name");
    deleteAdmin(name);
    location.reload();
  });
});

// Render members on group panel page
if (window.location.pathname === "/group_panel") {
  renderMembers();
}

// Render tables
if (window.location.pathname === "/school") {
  renderTables();
}

// Select buttons for Chores
if (window.location.pathname === "/chores") {
  memberCompleteChore();
  userChoreDelteBtn();
}

// Show/Hide button for Group Number in settings
if (window.location.pathname === "/settings") {
  btnGroupNumber.addEventListener("click", function () {
    if (inputGroupNumber.type === "password") {
      btnGroupNumber.textContent = "Hide";
      inputGroupNumber.type = "text";
    } else {
      btnGroupNumber.textContent = "Show";
      inputGroupNumber.type = "password";
    }
  });
}
