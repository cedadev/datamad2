// $(document).ready(function() {
//     $.fn.dataTable.moment( 'DD MMM YYYY' );
//     var table = $('#grants').DataTable( {
//         order: [[4, 'desc']]
//     } );
//
//     new $.fn.dataTable.FixedHeader( table );
// } );

function display_hidden_facets(event, facet){
    let hidden =  $('dd[id=hidden-'+facet +']')
    hidden.toggleClass('d-none')

    let e = $(event)
    if (e.html().startsWith("Show More")){
        e.html("Hide")
    } else {
        e.html("Show More (" + hidden.length +")" )
    }
};

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
