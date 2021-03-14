$(document).ready(function() {
    var heroSlideIndex = 0;
    function heroCarousel(){
        var y;
        var z = $('.hero-slide');
        if (z.length > 1) {
        for (y=0; y<z.length; y++) {
            z[y].style.display = "none";
        }
        heroSlideIndex++;
        if (heroSlideIndex > z.length) {heroSlideIndex=1}
        z[heroSlideIndex-1].style.display = "block";
        setTimeout(heroCarousel, 4000);
    }
    }

    function showEditForm(){
      $('#prof-edit').on('click', function(e){
        e.preventDefault();
      });
    }
    function preventIt(){
      $('#justwords').on('click', function(e){
        e.preventDefault();
      });
    }
    function preventIt2(){
      $('#justwords2').on('click', function(e){
        e.preventDefault();
      });
    }

    /*function modalShow(){
        $('#contshow').removeClass('hidden');
    }
    function modalHide(){
        $('#contshow').addClass('hidden');
    } */
      heroCarousel();
      showEditForm();
      preventIt();
      preventIt2();

    /*  
      $('#show-modal').on('click', function(e){
        e.preventDefault();
          modalShow();
      });

      $('#hide-modal').on('click', function(e){
        e.preventDefault();
        modalHide();
       });
       */

    });
    