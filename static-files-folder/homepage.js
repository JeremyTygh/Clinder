
(function(){
    var animating = false;
    var likedList = [];
  
    function animatecard(ev) {

      if (animating === false) {
        var t = ev.target;
        if (t.className === 'but-dislike') {
          t.parentNode.classList.add('nope');
          animating = true;
          fireCustomEvent('nopecard',
            {
              origin: t,
              container: t.parentNode,
              card: t.parentNode.querySelector('.clinderCard')
            }
          );
        }
        if (t.className === 'but-like') {
          t.parentNode.classList.add('yes');
          animating = true;
          /*Adding image address to list*/
          var imageAddress = document.getElementById("image").alt;
          likedList.push(imageAddress);
            console.log("hello");
             // POST
            fetch('/liked', {

                // Declare what type of data we're sending
                headers: {
                'Content-Type': 'application/json'
                },

                // Specify the method
                method: 'POST',

                // A JSON payload
                body: JSON.stringify({
                    imageAddress
                })
            }).then(function (response) { // At this point, Flask has printed our JSON
                return response.text();
            }).then(function (text) {

                console.log('POST response: ');

                // Should be 'OK' if everything was successful
                console.log(text);
            });


          console.log(likedList);
          fireCustomEvent('yepcard',
            {
              origin: t,
              container: t.parentNode,
              card: t.parentNode.querySelector('.clinderCard')
            }
          );
        }
        if (t.classList.contains('current')) {
          fireCustomEvent('cardchosen',
            {
              container: getContainer(t),
              card: t
            }
          );
        }
      }
    }
  
    function fireCustomEvent(name, payload) {
      var newevent = new CustomEvent(name, {
        detail: payload
      });
      document.body.dispatchEvent(newevent);
    }
  
    function getContainer(elm) {
      var origin = elm.parentNode;
      if (!origin.classList.contains('cardcontainer')){
        origin = origin.parentNode;
      }
      return origin;
    }
  
    function animationdone(ev) {
      animating = false;
      var origin = getContainer(ev.target);
      if (ev.animationName === 'yay') {
        origin.classList.remove('yes');
      }
      if (ev.animationName === 'nope') {
        origin.classList.remove('nope');
      }
      if (origin.classList.contains('list')) {
        if (ev.animationName === 'nope' ||
            ev.animationName === 'yay') {
          origin.querySelector('.current').remove();
          if (!origin.querySelector('.clinderCard')) {
            fireCustomEvent('deckempty', {
              origin: origin.querySelector('button'),
              container: origin,
              card: null
            });
          } else {
            origin.querySelector('.clinderCard').classList.add('current');
          }
        }
      }
    }
    document.body.addEventListener('animationend', animationdone);
    document.body.addEventListener('webkitAnimationEnd', animationdone);
    document.body.addEventListener('click', animatecard);
    window.addEventListener('DOMContentLoaded', function(){
      document.body.classList.add('clinder');
    });

    // GET is the default method, so we don't need to set it
    // fetch('/liked')
    // .then(function (response) {
    //     return response.text();
    // }).then(function (text) {
    //     console.log('GET response text:');
    //     console.log(text); // Print the greeting as text
    // });

    // // Send the same request
    // fetch('/liked')
    // .then(function (response) {
    //     return response.json(); // But parse it as JSON this time
    // })
    // .then(function (json) {
    //     console.log('GET response as JSON:');
    //     console.log(json); // Here’s our JSON object
    // })



  })();