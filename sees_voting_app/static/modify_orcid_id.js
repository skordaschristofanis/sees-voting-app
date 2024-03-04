$(document).ready(function() {
    $("#orcid").on("input", function() {

        // Remove non-digits and limit to 16 digits
        var input = $(this).val().replace(/\D/g, "").split("");
        if(input.length > 16) {
            input = input.slice(0, 16);
        }

        // Insert hyphens every 4 digits, not after 16th digit
        for(var i = 4; i < input.length; i += 5) {
            if(i != input.length) {
                input.splice(i, 0, "-");
            }
        }

        // Update the input field value
        $(this).val(input.join(""));
    });
});