
btn_login.addEventListener('click', () => {
    wrapper.classList.add('Login');
    nav.classList.remove("openSearch");
    if (nav.classList.contains("openSearch")) {
        return searchIcon.classList.replace("bx", "fa-solid"),
            searchIcon.classList.replace("bx-search", "fa-xmark");
    }
    searchIcon.classList.replace("fa-solid", "bx");
    searchIcon.classList.replace("fa-xmark", "bx-search");
    nav.classList.remove("openSideNav");

})

btn_login_2.addEventListener('click', () => {
    wrapper.classList.add('Login');
    nav.classList.remove("openSearch");
    if (nav.classList.contains("openSearch")) {
        return searchIcon.classList.replace("bx", "fa-solid"),
            searchIcon.classList.replace("bx-search", "fa-xmark");
    }
    searchIcon.classList.replace("fa-solid", "bx");
    searchIcon.classList.replace("fa-xmark", "bx-search");
    nav.classList.remove("openSideNav");

})

closeBtn.addEventListener('click', () => {
    wrapper.classList.remove('Login');
})


