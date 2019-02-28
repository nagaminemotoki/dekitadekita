$(function () {

    // $(".btn").on('click',function(){
    $("#dekita_hanko img").delay(1000).animate({
        opacity: 1,
        "top": "30px",
        "right": "50px",
        "width": "130px"
    }, 1000, "easeOutBounce");
    // });

    if ($("#dekita_input").val().length == 0) {
        $("#dekita_submit").prop("disabled", true);
    }
    $("#dekita_input").on("keydown keyup keypress change", function () {
        if ($(this).val().length < 1) {
            $("#dekita_submit").prop("disabled", true);
        } else {
            $("#dekita_submit").prop("disabled", false);
        }
    });

});