var change = 0;
$( window ).on('load', function() {
    setInterval(function () {
        var x = $('div#reveal');
        x.removeClass('background' + (change%3));
        x.addClass('background' + (change+1)%3);
        change += 1;
        change = change % 3
     }, 7000);

  });