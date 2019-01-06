function logout() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            FB.logout(function(response) {
                localStorage.clear();
                location.replace("/logout");
            });
        } else if (response.status === 'not_authorized') {
            // user has login Facebook, but not yours app
            FB.logout(function(response) { // user has logout
                alert("請重新登入！");
                location.replace("/logout");
            });
        } else { // user didnt login Facebook
            alert("請重新登入！");
            location.replace("/logout");
        }
    });
}