<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>;

$(document).ready(function () {
  $("#trigger-span").click(function () {
    // Assuming api_data is a JavaScript object containing the data fetched from your API
    // var apiData = {{ api_data|safe }};

    // var index = $("#trigger-span").index("li");
    let nextDate = "{{ next_dates.0 }}";

    // Update the content of the div with the fetched data
    $("#date").text(nextDate);
  });
});
