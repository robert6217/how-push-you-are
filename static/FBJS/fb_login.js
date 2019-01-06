function FBlogin() {
    FB.login(function(response) {
        var obj = {
            userID: response.authResponse.userID,
            accessToken: response.authResponse.accessToken
        };
        var data_json = JSON.stringify(obj);
        $.ajax({
            url: "/API_FB_login",
            type: "POST",
            data: data_json,
            dataType: "json",
            async: false,
            contentType: "application/json",
            success: function(data, textStatus, jqXHR) {
                if (data == '11') {
                    console.log('data =' + data)
                    location.replace('/');
                }
            }
        });
    });
}


function checkFBlogin() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            var obj = {
                userID: response.authResponse.userID,
                accessToken: response.authResponse.accessToken
            };
            var data_json = JSON.stringify(obj);
            $.ajax({
                url: "/API_FB_login",
                type: "POST",
                data: data_json,
                dataType: "json",
                async: false,
                contentType: "application/json",
                success: function(data, textStatus, jqXHR) {
                    if (data == '11') {
                        console.log('data =' + data)
                        location.replace('/');
                    }
                }
            });
        } else if (response.status === 'not_authorized') {
            FBlogin();
            console.log("not_authorized.")
        } else {
            FBlogin();
            console.log("Please log into this app by Facebook.")
        }
    });
}