$(document).ready(function() {
    var selectedOptions = [];

    $(".choice").change(function() {
        var selected = $(this).val();
        var previous = $(this).data("previous");

        // Add the newly selected option to the array if it's not the default option
        if (selected !== "default") {
            selectedOptions.push(selected);
        }

        // Remove the previous selection from the array
        if (previous) {
            selectedOptions = selectedOptions.filter(function(value) {
                return value !== previous;
            });
        }

        // Update the previous value data
        $(this).data("previous", selected);

        // Disable the selected options in all select boxes
        $(".choice option").each(function() {
            if (selectedOptions.includes($(this).val()) && !$(this).is(":selected") && $(this).val() !== "default") {
                $(this).prop("disabled", true);
            } else {
                $(this).prop("disabled", false);
            }
        });
    }).change();  // Trigger the change event after setting up the event handler
});