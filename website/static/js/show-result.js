function handleSearchInput() {
    console.log("in search");
    let textlist = $('#search-query').val().trim().split(" ");
    textlist = textlist.map(text => {
        return text.replace(/[.,\/#!$%^&*;:{}=\-_`~()]/g, "")
    });

    textlist = textlist.filter(text => text !== "");
    console.log(textlist);

    return textlist.join(',');

}


function handleSearch() {
    jQuery.ajax({
        dataType: "json",
        data: {'queries': handleSearchInput()},
        url: "api/search",
        method: "POST",
        success: (resultData) => handleSearchResult(resultData)
    });
}

function handleSearchResult(resultData) {
    //show the search result
    console.log(resultData);

    let showResultElement = jQuery("#show_result");
    showResultElement.empty();

    if (resultData.length === 0) {

        template =
            $("<div>", {
                class: "container",
                html: $("<div>", {
                    class:
                        "row justify-content-empty-center mb-5 ",
                    html: $("<div>", {
                        class: "col-centered",
                        html: $("<div>", {

                            class: "card",
                            html: $("<div>", {
                                class: "card-block",
                                html: $("<div>", {
                                    class: "card-text",
                                    text: "No Result"
                                })
                            })
                        }),
                        style: "width:80%; margin-left :10%"
                    }),


                })
            });
        showResultElement.append(template);

    } else {
        let template;
        for (let i = 0; i < Math.min(10, resultData.length); i++) {

            template =
                $("<div>", {
                    class: "container",
                    html: $("<div>", {
                        class:
                            "row justify-content-empty-center mb-5 ",
                        html: $("<div>", {
                            class: "col-centered",
                            html: $("<div>", {

                                class: "card",
                                html: $("<div>", {
                                    class: "card-block",
                                    html: $("<div>", {
                                        class: "card-text",
                                        html: $("<a>", {href: resultData[i], text: resultData[i]})
                                    })
                                })
                            }),
                            style: "width:80%; margin-left :10%"
                        }),


                    })
                });
            showResultElement.append(template);
        }
    }
}

function handleEnter(event) {
    if (event.keyCode === 13) {

        handleSearch();
    }
}


