const tabs = document.querySelectorAll(".tabs ul li");
const signInContainer = document.getElementById("sign-in-container");
const signUpContainer = document.getElementById("sign-up-container");

function toggleContainer(index) {
    if (index === 0) {
        signInContainer.style.display = "block";
        signUpContainer.style.display = "none";
    } else {
        signInContainer.style.display = "none";
        signUpContainer.style.display = "block";
    }
    localStorage.setItem("activeTab", index);
    updateHash(index);
}

function updateHash(index) {
    if (index === 0) {
        window.location.hash = "sign-in";
    } else {
        window.location.hash = "sign-up";
    }
}

tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("is-active"));
        tab.classList.add("is-active");
        toggleContainer(index);
    });
});

function setInitialFormFromHash() {
    const savedTabIndex = localStorage.getItem("activeTab");
    let initialIndex = savedTabIndex !== null ? parseInt(savedTabIndex) : 0;

    if (window.location.hash === "#sign-up") {
        initialIndex = 1;
    } else if (window.location.hash === "#sign-in") {
        initialIndex = 0;
    }

    tabs.forEach(t => t.classList.remove("is-active"));
    tabs[initialIndex].classList.add("is-active");
    toggleContainer(initialIndex);
}

setInitialFormFromHash();

window.addEventListener("hashchange", function () {
    setInitialFormFromHash();
});

document.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", (event) => {
        if (link.href.includes("#sign-up")) {
            window.location.hash = "sign-up";
        } else if (link.href.includes("#sign-in")) {
            window.location.hash = "sign-in";
        }

        event.preventDefault();
    });
});


const senhaField = document.getElementById('sign-up-password');
const confirmSenhaField = document.getElementById('confirm-password');
const errorMessage = document.getElementById('password-error');
const successMessage = document.getElementById('password-success');

function validatePasswords() {
    const senha = senhaField.value;
    const confirmSenha = confirmSenhaField.value;

    if (confirmSenha && senha !== confirmSenha) {
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
    } else if (senha && confirmSenha && senha === confirmSenha) {
        errorMessage.style.display = 'none';
        successMessage.style.display = 'block';
    } else {
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
    }
}

senhaField.addEventListener('input', validatePasswords);
confirmSenhaField.addEventListener('input', validatePasswords);
