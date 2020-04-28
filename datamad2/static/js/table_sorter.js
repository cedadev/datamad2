$(document).ready(function() {
    $.fn.dataTable.moment( 'DD MMM YYYY' );
    var table = $('#grants').DataTable( {
        order: [[4, 'desc']]
    } );

    new $.fn.dataTable.FixedHeader( table );
} );

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})


$( ".claim-btn" ).click(function(){
        let btn = $(this);
        let url = 'grant/' + $(this).attr('data-id') + '/claim';
        let cell = btn.parent();

        $.ajax({
            type: "GET",
            url: url,

            // handle a successful response
            success: function () {
                cell.html("CLAIMED");
                cell.attr('id', 'claim');
            },
            // handle a non-successful response
            error: function () {
                alert('Claim failed');
            }
        });
    });
