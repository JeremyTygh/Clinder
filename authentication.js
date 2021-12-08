
(function(){

    function loginPressed(ev) {

        var t = ev.target;
        
        if (t.className === 'login-btn') {
        //   t.parentNode.classList.add('yes');
          
          var username = document.getElementById("username").value;
          var password = document.getElementById("password").value;
            console.log(username + " " + password);
             // POST
            fetch('/login', {

                // Declare what type of data we're sending
                headers: {
                'Content-Type': 'application/json'
                },

                // Specify the method
                method: 'POST',

                // A JSON payload
                body: JSON.stringify({
                    username, password
                })
            }).then(function (response) { // At this point, Flask has printed our JSON
                return response.text();
            }).then(function (text) {

                console.log('POST response: ');

                // Should be 'OK' if everything was successful
                console.log(text);
            });

          
        } else if (t.className === 'register-btn') {
            //   t.parentNode.classList.add('yes');
          
          var username = document.getElementById("username").value;
          var password = document.getElementById("password").value;
            console.log(username + " " + password);
             // POST
            fetch('/register', {

                // Declare what type of data we're sending
                headers: {
                'Content-Type': 'application/json'
                },

                // Specify the method
                method: 'POST',

                // A JSON payload
                body: JSON.stringify({
                    username, password
                })
            }).then(function (response) { // At this point, Flask has printed our JSON
                return response.text();
            }).then(function (text) {

                console.log('POST response: ');

                // Should be 'OK' if everything was successful
                console.log(text);
            });

        }
      }
      document.body.addEventListener('click', loginPressed);
    }

    

)();