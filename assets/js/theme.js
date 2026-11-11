/* Sets the saved theme before the page paints (kept in a file so the site can block inline scripts). */
try{var t=localStorage.getItem('xt-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}
