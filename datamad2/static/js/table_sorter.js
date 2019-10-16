$(document).ready(function() {
    var table = $('#grants').DataTable( {
    } );

    new $.fn.dataTable.FixedHeader( table );
} );

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})