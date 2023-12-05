// script.js
var fs = require("fs");

function updateGrid(posts) {
  console.log("Grid ku vantom", posts);
  const gridContainer = document.getElementById("gridContainer");
  gridContainer.innerHTML = "";

  posts.forEach((post) => {
    const postElement = document.createElement("div");
    postElement.classList.add("post");
    postElement.addEventListener("click", function () {
      window.location.href = post.target;
    });
    const imgElement = document.createElement("img");
    imgElement.src = post.url;
    imgElement.alt = "Post Image";

    postElement.appendChild(imgElement);
    const postInfo = document.createElement("div");
    postInfo.classList.add("post-info");
    postInfo.innerHTML = `
            <p>${post.owner} <br> ${post.date} <br> ${post.location}</p>
          `;
    postElement.appendChild(postInfo);

    gridContainer.appendChild(postElement);
  });
  hide();
  gridContainer.style.display = "grid";
}

async function fetchBot() {
  show();
  const hashtag = document.getElementById("hashtagInput").value;
  const limit = document.getElementById("limitInput").value;

  const response = await fetch(`/api/Bot/${hashtag}/${limit}`);
  const posts = await response.json();
  updateGrid(posts);
}

async function fetchModule() {
  show();
  const hashtag = document.getElementById("hashtagInput").value;
  const limit = document.getElementById("limitInput").value;

  const response = await fetch(`/api/Module/${hashtag}/${limit}`);
  const res = await response.json();
  updateGrid(res);
}

function show() {
  document.getElementsByClassName("loader")[0].style.display = "block";
}

function hide() {
  document.getElementsByClassName("loader")[0].style.display = "none";
}
