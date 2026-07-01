const header = document.querySelector("[data-header]");
const toggle = document.querySelector("[data-nav-toggle]");
const menu = document.querySelector("[data-nav-menu]");

const setHeaderState = () => {
  if (!header) return;
  header.classList.toggle("is-scrolled", window.scrollY > 24);
};

setHeaderState();
window.addEventListener("scroll", setHeaderState, { passive: true });

if (toggle && menu) {
  toggle.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("is-open");
    document.body.classList.toggle("nav-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.remove("is-open");
      document.body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

const revealItems = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

document.querySelectorAll("[data-carousel]").forEach((carousel) => {
  let direction = 1;
  let timer = window.setInterval(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const maxScroll = carousel.scrollWidth - carousel.clientWidth;
    if (maxScroll <= 0) return;
    if (carousel.scrollLeft >= maxScroll - 4) direction = -1;
    if (carousel.scrollLeft <= 4) direction = 1;
    carousel.scrollBy({ left: direction * 340, behavior: "smooth" });
  }, 5200);

  carousel.addEventListener("pointerenter", () => window.clearInterval(timer));
});

const lightbox = document.querySelector("[data-lightbox-modal]");
if (lightbox) {
  const lightboxImage = lightbox.querySelector("img");
  const closeButton = lightbox.querySelector("[data-lightbox-close]");

  const closeLightbox = () => {
    lightbox.hidden = true;
    lightboxImage.src = "";
    lightboxImage.alt = "";
  };

  document.querySelectorAll("[data-lightbox]").forEach((button) => {
    button.addEventListener("click", () => {
      lightboxImage.src = button.dataset.lightbox;
      lightboxImage.alt = button.dataset.alt || "";
      lightbox.hidden = false;
      closeButton.focus();
    });
  });

  closeButton.addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !lightbox.hidden) closeLightbox();
  });
}

const bookingForm = document.querySelector("[data-booking-form]");
if (bookingForm) {
  bookingForm.addEventListener("submit", (event) => {
    const requiredFields = bookingForm.querySelectorAll("[required]");
    let firstInvalid = null;
    requiredFields.forEach((field) => {
      field.setCustomValidity("");
      if (!field.value.trim()) {
        field.setCustomValidity("Please complete this field.");
        firstInvalid = firstInvalid || field;
      }
    });
    const email = bookingForm.querySelector('input[type="email"]');
    if (email && email.value && !email.value.includes("@")) {
      email.setCustomValidity("Please enter a valid email address.");
      firstInvalid = firstInvalid || email;
    }
    if (firstInvalid) {
      event.preventDefault();
      firstInvalid.reportValidity();
    }
  });
}
