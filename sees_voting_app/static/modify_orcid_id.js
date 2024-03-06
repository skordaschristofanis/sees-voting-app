$(document).ready(function() {
    $("#orcid").on("input", function() {
        // Remove input hyphens
        var input = $(this).val().replace(/-/g, "");

        // Ensure the first 15 characters are digits
        if(input.length > 15) {
            input = input.slice(0, 15).replace(/\D/g, "") + input.charAt(15).toUpperCase().replace(/[^0-9X]/, "");
        } else {
            input = input.replace(/\D/g, "");
        }

        // Insert hyphens every 4 characters, not after 16th character
        input = input.replace(/(\d{4})/g, '$1-').replace(/-$/, '');

        // Update the input field value
        $(this).val(input);
    });
});