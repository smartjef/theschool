

let thumbnails = document.getElementsByClassName('thumbnail')
let activeImages = document.getElementsByClassName('active')

//for(var i=0; i<thumbnails.length; i++){
    //thumbnails[i].addEventListener('mouseover', function(){
       // if(activeImages.length > 0){
           // activeImages[0].classList.remove('active')
       // }
        //this.classList.add('active')
        //document.getElementById('featured').src = this.src
   // })
//}

let buttonLeft = document.getElementById('slideLeft');
let buttonRight = document.getElementById('slideRight');

buttonLeft.addEventListener('click', function(){
    document.getElementById('slider').scrollLeft -= 180
})

buttonRight.addEventListener('click', function(){
    document.getElementById('slider').scrollLeft += 180
} )


/*====================*/

var slideIndex = 0;
showSlides();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
        slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1
    }    
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
    setTimeout(showSlides, 2000);
}