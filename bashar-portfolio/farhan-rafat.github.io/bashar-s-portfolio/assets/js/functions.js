$(".toggleNav").on("click", function (event) {
  event.preventDefault();
  event.stopPropagation();
  $("body").toggleClass("nav-expanded");
});

function darkModeListener() {
  document.querySelector("html").classList.toggle("dark");
}

document
  .querySelector("input[type='checkbox']#dark-toggle")
  .addEventListener("click", darkModeListener);

// ratings javaScript code
var stars = document.querySelectorAll(".star a");

stars.forEach((item, index1) => {
  item.addEventListener("click", () => {
    stars.forEach((star, index2) => {
      index1 >= index2
        ? star.classList.add("active")
        : star.classList.remove("active");
    });
  });
});

// Preloader jQuery code

$(window).on("load", function () {
  setTimeout(function () {
    $("html").removeClass("loading").addClass("loaded");
  }, 2000);
});

// scroll reveal javaScript code

const scrollers = document.querySelectorAll("[data-scroll]");

function check(entries) {
  entries.map((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("in-view");
      observer.unobserve(entry.target);
    }
  });
}

const observer = new IntersectionObserver(check);
scrollers.forEach((scroller) => observer.observe(scroller));
