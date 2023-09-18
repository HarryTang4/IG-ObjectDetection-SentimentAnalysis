// 
// 
//

// Sidebar

const menuItems = document.querySelectorAll(".menu-item");
const currentPage = document.querySelector('body').id;

const changeActiveMenuItems = () => {
    menuItems.forEach((item) => {
        item.classList.remove("active");
        if (item.id === window.location.pathname) {
            item.classList.add("active");
        }
    });
}

let dropdown = false;
menuItems.forEach((item) => {
    item.addEventListener("click", () => {
        if (item.id === 'analytics/') {
            return;
        }
        changeActiveMenuItems();
        item.classList.add("active");
        if (item.id != "settings" || dropdown == true) {
            document.querySelector('.settings-dropdown').style.display = "none";
            dropdown = (false);
            if (item.id === window.location.pathname || item.id == "settings"){
                changeActiveMenuItems();
            }
            else{
            location.replace("https://localhost:8000/" + item.id);
            }
        }
        else{
            document.querySelector('.settings-dropdown').style.display = "flex";
            dropdown = (true);
        }
    })
})

changeActiveMenuItems();


