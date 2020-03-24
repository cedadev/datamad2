$(document).ready(function() {
    var table = $('#grants').DataTable( {
    } );

    new $.fn.dataTable.FixedHeader( table );
} );

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


$(".claim-btn").click(function () {
    let btn = $(this);
    let url = 'grant/' + $(this).attr('data-id') + '/claim';
    let cell = btn.parent();
    let data_centre = cell.parent()[0].cells[2];
    console.log(data_centre)
    $.ajax({
        type: "GET",
        url: url,

        // handle a successful response
        success: function () {
            cell.html("CLAIMED");
            cell.attr('id', 'claim');
            data_centre.innerHTML = "{{ user.data_centre }}"
            console.log(cell.parent())
        },
        // handle a non-successful response
        error: function () {
            alert('Claim failed');
        }
    });
});
