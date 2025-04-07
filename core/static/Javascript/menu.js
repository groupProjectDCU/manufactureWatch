document.addEventListener("DOMContentLoaded", function() {
    // Dynamically load the additional CSS for the dynamic menu
    var cssLink = document.createElement("link");
    cssLink.rel = "stylesheet";
    cssLink.href = "../static/styles/dynamicMenu.css";  // adjust the path as needed
    document.head.appendChild(cssLink);
    
    // Create the dynamic menu container (aside element)
    var dynamicMenu = document.createElement("aside");
    dynamicMenu.id = "dynamicMenu";
    dynamicMenu.className = "dynamic-menu";
    
    // Create the menu list with links
    var menuList = document.createElement("ul");
    menuList.className = "dynamic-menu-list";
    var menuItems = [
      { text: "Home", href: "home.html" },
      { text: "About", href: "about.html" },
      { text: "Contact", href: "contact.html" },
      { text: "Login", href: "login.html" }
    ];
    menuItems.forEach(function(item) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = item.href;
      a.textContent = item.text;
      li.appendChild(a);
      menuList.appendChild(li);
    });
    dynamicMenu.appendChild(menuList);
    document.body.appendChild(dynamicMenu);
    
    // Create the hamburger icon (menu trigger)
    var menuTab = document.createElement("div");
    menuTab.id = "menuTab";
    menuTab.className = "menu-tab";
    var iconSpan = document.createElement("span");
    iconSpan.className = "menu-tab-icon";
    iconSpan.innerHTML = "&#9776;"; // hamburger icon
    menuTab.appendChild(iconSpan);
    document.body.appendChild(menuTab);
    
    // Create the overlay element
    var overlay = document.createElement("div");
    overlay.id = "menuOverlay";
    overlay.className = "menu-overlay";
    document.body.appendChild(overlay);
    
    // Function to open the menu
    function openMenu() {
      dynamicMenu.classList.add("show");
      overlay.classList.add("show");
    }
    
    // Function to close the menu
    function closeMenu() {
      dynamicMenu.classList.remove("show");
      overlay.classList.remove("show");
    }
    
    // Toggle function for click event
    function toggleMenu() {
      if (dynamicMenu.classList.contains("show")) {
        closeMenu();
      } else {
        openMenu();
      }
    }
    
    // Click event listeners remain unchanged
    menuTab.addEventListener("click", toggleMenu);
    overlay.addEventListener("click", toggleMenu);
    
    // ----------------------------
    // NEW: Hover behavior to open menu
    // ----------------------------
    
    // Open the menu when mouse enters the menu trigger or menu area
    menuTab.addEventListener("mouseenter", openMenu);
    dynamicMenu.addEventListener("mouseenter", openMenu);
    
    // Close the menu when mouse leaves both the menu trigger and menu area.
    // A small delay is used to allow smooth transitions if moving between areas.
    function handleMouseLeave() {
      setTimeout(function() {
        if (!menuTab.matches(':hover') && !dynamicMenu.matches(':hover')) {
          closeMenu();
        }
      }, 200);
    }
    
    menuTab.addEventListener("mouseleave", handleMouseLeave);
    dynamicMenu.addEventListener("mouseleave", handleMouseLeave);
    overlay.addEventListener("mouseleave", handleMouseLeave);
  });
  