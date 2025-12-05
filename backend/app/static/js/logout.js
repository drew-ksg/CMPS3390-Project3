document.addEventListener('DOMContentLoaded', () => {
    const logout = document.getElementById('logout');
    console.log('Logout script loaded');
    if (logout) {
        logout.addEventListener('click', function(event) {
            
            localStorage.removeItem('jwt'); 
            window.location.href = '/login';
        });
    }
});
