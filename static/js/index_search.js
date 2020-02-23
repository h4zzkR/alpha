$(function(){
	initGlossaryFilter();
});

// Filter Glossary items
function initGlossaryFilter(){
		// Filter using search box
    $("#glossarySearchInput").bind("keyup", function(){
        var inputValue = $(this).val();

        // Hide all the results & Cards
        $(".glossary__results__row").addClass("inactive");
        $(".glossary__results__item").hide();

        $(".glossary__results__row").each(function(){
            $(".glossary__results__item").each(function(){
                var item = $(this).attr("data-item");

                if(item.toUpperCase().indexOf(inputValue.toUpperCase()) != -1){
                    $(this).parents(".glossary__results__row").removeClass("inactive");
                    $(this).show();
                }
            });
        });
    });
	
		// Filter using navigation
    $(".glossary__nav a").click(function(){
        var nav = $(this).attr("data-nav");
        console.log(nav);

        // Remove & Add active class
        $(".glossary__nav__item").removeClass("active");
        $(this).parent().toggleClass("active");

        // Hide all the results
        $(".glossary__results__row").addClass("inactive");

        // Loop through the row
        $(".glossary__results__row").each(function(){
            var term = $(this).attr("data-term");

            if(nav == term){
                $(this).removeClass("inactive");
            }
        });

        // Only return false if data-toggle is glossary
        if($(this).attr("data-toggle") == "glossary"){
            return false;
        }
    });
}