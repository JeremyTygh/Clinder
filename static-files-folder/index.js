!(function(d){

  var itemClassName = "carousel__photo";
      items = d.getElementsByClassName(itemClassName),
      totalItems = items.length,
      activeSlides = 5;
      slideLeft = 0,
      slideRight = slideLeft + activeSlides - 1;

 
  //set previous, active and next images (minimum of 3 images)
  function setClasses(previous, firstActive, next) {
      items[previous].className = itemClassName + " prev";
      items[firstActive].className = itemClassName + " active";
      for (let i = 1; i < activeSlides; i++) {
          items[slideLeft + i].className = itemClassName + " active";
      }
      items[next].className = itemClassName + " next";
  }

  //set event listeners
  function setEventListeners() {
      var next = d.getElementsByClassName('carousel__button--next')[0],
          prev = d.getElementsByClassName('carousel__button--prev')[0];
      next.addEventListener('click', moveNext);
      prev.addEventListener('click', movePrev);
  }

  //next navigation handler
  function moveNext() {
      
      //if right-most slide has reached end of carousel, reset carousel to start
      if (slideRight == (totalItems-1)) {
          slideLeft = 0;
          
      //else right-shift carousel based on number of slides remaining until end
      } else {
          var slidesRemaining = totalItems - slideRight - 1;
          slideLeft = (slidesRemaining >= activeSlides) ? slideLeft + activeSlides : slideLeft + slidesRemaining;
      }

      moveCarouselTo(slideLeft);
  }

  //previous navigation handler
  function movePrev() {

      //if left-most slide has reached start of carousel, reset carousel to end
      if (slideLeft === 0) {
          slideLeft = (totalItems - activeSlides);

      //left-shift carousel based on number of slides remaining until start
      } else {
          slideLeft = (slideLeft >= activeSlides) ? slideLeft - activeSlides : 0; 
      }

      moveCarouselTo(slideLeft);
  }

  function moveCarouselTo(slideLeft) {

      slideRight = slideLeft + activeSlides - 1;
      
      //previous slide is always 1 slide before left-most slide, unless left-most slide is at start
      var newPrevious = (slideLeft != 0) ? slideLeft - 1 : totalItems - 1;
      
      //next slide is always 1 slide after right-most slide, unless right-most slide is at end
      var newNext = (slideRight != totalItems - 1) ? slideRight + 1 : 0;
      
      //reset images to default classes
      for (let item of items) {
          item.className = itemClassName;
      }

      //set new previous, active and next images
      setClasses(newPrevious, slideLeft, newNext);
  }

  function initCarousel() {
      setClasses(totalItems - 1, 0, activeSlides);
      setEventListeners();
  }

  initCarousel();

}(document));


const imgContainer = document.querySelector('.carousel-wrapper')
const dotsContainer = document.querySelector('.nav__dots')


document.getElementById('dot1').addEventListener('click', ()=>{
    imgContainer.className = 'carousel-wrapper first-active'
    dotsContainer.className = 'nav__dots first-current'
})
document.getElementById('dot2').addEventListener('click', ()=>{
    imgContainer.className = 'image__container second-active'
    dotsContainer.className = 'nav__dots second-current'
})
document.getElementById('dot3').addEventListener('click', ()=>{
    imgContainer.className = 'image__container third-active'
    dotsContainer.className = 'nav__dots third-current'
})

