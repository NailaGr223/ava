// Preloader
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    preloader.style.opacity = '0';
    setTimeout(() => preloader.style.display = 'none', 600);
});

// Dark Mode
const toggleBtn = document.getElementById('theme-toggle');
const body = document.body;

toggleBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('darkMode', 'true');
    } else {
        toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('darkMode', 'false');
    }
});

if (localStorage.getItem('darkMode') === 'true') {
    body.classList.add('dark-mode');
    toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
}

// Success Message
function showPurchaseSuccess() {
    const msg = document.createElement('div');
    msg.style.cssText = `position:fixed; top:30px; right:30px; background:#1a2e1a; color:#d9b206; padding:20px 30px; 
                         border-radius:10px; box-shadow:0 10px 30px rgba(0,0,0,0.4); z-index:10000; font-size:1.1rem;`;
    msg.innerHTML = '🎉 Thank you! Your bird has been successfully added to cart.';
    document.body.appendChild(msg);
    
    setTimeout(() => msg.remove(), 4500);
}