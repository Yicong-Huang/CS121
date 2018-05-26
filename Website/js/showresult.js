
function handleSearchInput(){
	let text = document.getElementsByName("Text")[0].value;
	text = text.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").replace(" ",",");
	console.log(text);
	
	return text;
}


function handleSearch(){
	let text = handleSearchInput();
	//handleSearchResult();
		
	
	jQuery.ajax{
		dataType:"json",
		url:"api/search?queries="+text,
		method:"POST",
		success:(resultData)=>handleSearchResult(resultData)
	};

	
}

function handleSearchResult(resultData){
	let showResultElement = jQuery("#show_result");
	showResultElement.empty();
	let rowHtml = "";
	for(let i = 0; i < min(10,resultData.length); i++){
		rowHtml += "<p id='url'><a href='" + resultData[i] + "'>" + resultData[i] + "</a></p>";
	}
	
	showResultElement.append(rowHtml);

}

function getParameterByName(target) {
        // Get request URL
        let url = window.location.href;
        // Encode target parameter name to url encoding
        target = target.replace(/[\[\]]/g, "\\$&");

        // Ues regular expression to find matched parameter value
        let regex = new RegExp("[?&]" + target + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';

        // Return the decoded parameter value
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

