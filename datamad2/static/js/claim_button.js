$(".claim-btn").click(function () {
            var $btn = $(this);
            console.log($btn);
            let url_claim = '/' + 'grant/' + $(this).attr('data-id') + '/claim';
            let url_unclaim = '/' + 'grant/' + $(this).attr('data-id') + '/unclaim';
            let cell = $btn.parent();
            let assign = cell[0].parentElement;
            console.log(assign)

            if ($btn.attr('id') == "claim-button") {
                url = url_claim;
                data = "UNCLAIM";
                data2 = "REASSIGN";
            } else {
                url = url_unclaim;
                data = "CLAIM";
                data2 = "ASSIGN";
            }
            $.ajax({
                type: "GET",
                url: url,

                // handle a successful response
                success: function () {
                    $btn[0].innerHTML = data;
                },
                // handle a non-successful response
                error: function () {
                    alert('Failed');
                }
            });
        });
