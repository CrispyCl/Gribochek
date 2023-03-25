const nav = document.querySelector('.nav'),
    searchIcon = document.querySelector('#searchIcon'),
    navOpenBtn = document.querySelector('.navOpenBtn'),
    navCloseBtn = document.querySelector('.navCloseBtn'),
    searchBox = document.querySelector('.search-box'),
    BadAlertClose = document.querySelector('.bad_alert_box .close'),
    GoodAlertClose = document.querySelector('.good_alert_box .close'),
    GoodAlertBox = document.querySelector('.good_alert_box'),
    BadAlertBox = document.querySelector('.bad_alert_box'),
    GoodAlertProgress = document.querySelector('.good_alert_progress'),
    BadAlertProgress = document.querySelector('.bad_alert_progress'),
    wrapper = document.querySelector('.wrapper-login'),
    btn_login = document.querySelector('.btn_login'),
    btn_login_2 = document.querySelector('.btn_login_2'),
    closeBtn = document.querySelector('.icon-close'),
    btn_for_wrapper_login = document.querySelector('.btn_for_wrapper-login'),
    Badmess = document.querySelector('.bad_alert_message .text.text-2'),
    Goodmess = document.querySelector('.good_alert_message .text.text-2');

let mes = JSON.parse(document.querySelector('.message-content').innerHTML);


$(function () {
    if (mes['status'] != 404) {
        mes = JSON.parse(mes);
        if (mes['status'] == 404) {
            return
        }
        if (mes['status'] == 0) {
            BadAlertBox.classList.add('alert_show');
            BadAlertProgress.classList.add('active');
            Badmess.appendChild(document.createTextNode(mes['text']));


            if (BadAlertBox.classList.contains('alert_show')) {
                setTimeout(() => {
                    BadAlertBox.classList.remove('alert_show');
                    setTimeout(() => {
                        BadAlertProgress.classList.remove('active');
                    }, 4900);
                }, 5000);
            };
        }
        else {
            GoodAlertBox.classList.add('alert_show')
            GoodAlertProgress.classList.add('active')
            Goodmess.appendChild(document.createTextNode(mes['text']))


            if (GoodAlertBox.classList.contains('alert_show')) {
                setTimeout(() => {
                    GoodAlertBox.classList.remove('alert_show')
                    setTimeout(() => {
                        GoodAlertProgress.classList.remove('active')
                    }, 4900);
                }, 5000);
            }
        }
    }

});





BadAlertClose.addEventListener('click', () => {
    BadAlertBox.classList.remove('alert_show');

});

GoodAlertClose.addEventListener('click', () => {
    GoodAlertBox.classList.remove('alert_show');
});





searchIcon.addEventListener("click", () => {
    nav.classList.toggle("openSearch");
    nav.classList.remove("openSideNav");
    if (wrapper.classList.contains('Login')) {
        wrapper.classList.remove('Login');
    }
    if (nav.classList.contains("openSearch")) {
        return searchIcon.classList.replace("bx", "fa-solid"),
            searchIcon.classList.replace("bx-search", "fa-xmark");
    }
    searchIcon.classList.replace("fa-solid", "bx");
    searchIcon.classList.replace("fa-xmark", "bx-search");
});

navOpenBtn.addEventListener("click", () => {
    nav.classList.add("openSideNav");
    nav.classList.remove("openSearch");
    wrapper.classList.remove('Login');
    searchIcon.classList.replace("fa-solid", "bx");
    searchIcon.classList.replace("fa-xmark", "bx-search");
});

navCloseBtn.addEventListener("click", () => {
    nav.classList.remove("openSideNav");
});

// window.onclick = (event) => {
//     if (!event.target.matches('.search-box')) {
//         if (nav.classList.contains("openSearch")) {
//             nav.classList.remove("openSearch");
//             searchIcon.classList.replace("fa-solid", "bx");
//             searchIcon.classList.replace("fa-xmark", "bx-search");
//         }
//     }
// };

// window.onclick = (event) => {
//     if (!event.target.matches('.nav')) {
//         if (nav.classList.contains("openSideNav")) {
//             nav.classList.remove("openSideNav");
//             searchIcon.classList.replace("fa-solid", "bx");
//             searchIcon.classList.replace("fa-xmark", "bx-search");
//         }
//     }
// };

// nav.addEventListener('click', event => event.stopPropagation());




const reg_div = document.querySelector('.reg_div');
var x = window.matchMedia('(max-width: 910px)')

function add_show() {
    if (x.matches) {
        if (reg_div.classList.contains('show')) {
            reg_div.classList.remove('show');
        }
        else {
            reg_div.classList.add('show');
        };

    };
};

const uch_div = document.querySelector('.uch_div');

function add_show_uch() {
    if (x.matches) {
        if (uch_div.classList.contains('show')) {
            uch_div.classList.remove('show');
        }
        else {
            uch_div.classList.add('show');
        };

    };
};


// var xx = window.matchMedia('(max-width: 920px)');
// const img_href = document.querySelector('#href_link');

// function href_link() {
//     if (xx.matches) {
//         img_href.href = '/profile/{{current_user.id}}'
//     }
// }


!function () { "use strict"; function e(e, t) { const s = e.target.closest(`[${t.toggle}]`), o = e.target.closest(`[${t.remove}]`), l = e.target.closest(`[${t.add}]`); s && (e.preventDefault(), ((e, t) => { const s = e.getAttribute(t.toggle); document.querySelectorAll(`[${t.toggle}]`).forEach((s => { if (!s.hasAttribute(t.parallel) && s !== e) { document.querySelector(s.getAttribute(t.toggle)).classList.remove(s.getAttribute(t.class)); const o = e.getAttribute(t.self); o && e.classList.remove(o) } })), document.querySelector(s)?.classList.toggle(e.getAttribute(t.class)); const o = e.getAttribute(t.self); o && e.classList.toggle(o), t.onToggle(e) })(s, t)), o && (e.preventDefault(), ((e, t) => { const s = e.getAttribute(t.remove), o = e.getAttribute(t.class); document.querySelectorAll(s).forEach((e => { e.classList.remove(o) })); const l = e.getAttribute(t.self); l && e.classList.remove(l), t.onRemove(e) })(o, t)), l && (e.preventDefault(), ((e, t) => { const s = e.getAttribute(t.add), o = e.getAttribute(t.class); document.querySelectorAll(s).forEach((e => { e.classList.add(o) })); const l = e.getAttribute(t.self); l && e.classList.add(l), t.onAdd(e) })(l, t)), s || o || l || ((e, t) => { const s = document.querySelectorAll(`[${t.rcoe}]`); Array.from(s).forEach((s => { let o = s.getAttribute(t.toggle), l = s.getAttribute(t.class); if (!e.target.closest(o)) { document.querySelector(o)?.classList.remove(l); const e = s.getAttribute(t.self); e && s.classList.remove(e), t.onRcoe(s) } })) })(e, t) } const t = { toggle: "easy-toggle", add: "easy-add", remove: "easy-remove", class: "easy-class", rcoe: "easy-rcoe", parallel: "easy-parallel", self: "easy-self", selfRcoe: "easy-self-rcoe", onToggle(e) { }, onAdd(e) { }, onRemove(e) { }, onRcoe(e) { } }; document.addEventListener("DOMContentLoaded", (() => { document.addEventListener("click", (s => { e(s, t) })) })) }();