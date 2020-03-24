$(".claim-btn").click(function () {
            let btn = $(this);
            let url = '/' + 'grant/' + $(this).attr('data-id') + '/claim';
            let cell = btn.parent();
            let assign = cell[0].parentElement;
            $.ajax({
                type: "GET",
                url: url,

                // handle a successful response
                success: function () {
                    assign.innerHTML = "<td class=\"column-id\" id=\"right\">\n" +
                        "                                        <a><button data-id=\"{{ imported_grant.grant.pk }}\" class=\"btn btn-primary claim-btn\"  id=\"claim-button\"> UNCLAIM </button></a>\n" +
                        "                                        <a href=\"{% url 'change_claim' pk=imported_grant.grant.pk %}\"><button class=\"btn btn-primary\" id=\"claim\"> REASSIGN </button></a>\n" +
                        "                                    </td>"
                    cell.attr('id', 'claim');
                },
                // handle a non-successful response
                error: function () {
                    alert('Claim failed');
                }
            });
        });

        $(".claim-btn").click(function () {
            let btn = $(this);
            let url = '/' + 'grant/' + $(this).attr('data-id') + '/unclaim';
            let cell = btn.parent();
            let assign = cell[0].parentElement;
            $.ajax({
                type: "GET",
                url: url,

                // handle a successful response
                success: function () {
                    assign.innerHTML = "<td class=\"column-id\" id=\"right\">\n" +
                        "                                        <a><button data-id=\"{{ imported_grant.grant.pk }}\" class=\"btn btn-primary claim-btn\"  id=\"claim-button\"> CLAIM</button></a>\n" +
                        "                                        <a href=\"{% url 'change_claim' pk=imported_grant.grant.pk %}\"><button class=\"btn btn-primary\" id=\"claim\"> ASSIGN </button></a>\n" +
                        "                                    </td>"
                    cell.attr('id', 'claim');
                },
                // handle a non-successful response
                error: function () {
                    alert('Unclaim failed');
                }
            });
        });