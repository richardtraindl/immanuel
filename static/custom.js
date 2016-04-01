    function performMove(){
        $('#board td').click(function(){
            if( $(this).hasClass("marked") ){
                $(this).removeClass("marked");
                $('#white-pieces').addClass("invisible");
                $('#black-pieces').addClass("invisible");
                $('#prom-piece').attr("readonly", "readonly");
                if( $('#move-dst').val().trim() == $(this).attr("id") ){
                    $('#move-dst').val("");
                }
                else if( $('#move-src').val().trim() == $(this).attr("id") ){
                    $('#move-src').val("");
                    $('#move-dst').val("");
                }
            }
            else{
                $(this).addClass("marked");
                var src = $('#move-src').val();
                if(! src.trim() ){
                    $('#move-src').val($(this).attr("id"));
                }
                else{
                    $('#move-dst').val($(this).attr("id"));
                    var fieldid = $('#move-src').val();
                    var piece = $('#' + fieldid).attr("value");
                    if( piece == '2' ){
                        var row = $('#move-dst').val();
                        if( row.charAt(1) == '8' ){
                            $('#white-pieces').removeClass("invisible");
                            $('#prom-piece').removeAttr("readonly");
                            return;
                        }
                    }
                    else if( piece == '10' ){
                        var row = $('#move-dst').val();
                        if( row.charAt(1) == '1' ){
                            $('#black-pieces').removeClass("invisible");
                            $('#prom-piece').removeAttr("readonly");
                            return;
                        }
                    }
                    $("#move").submit()
                }
            }
        });
    }