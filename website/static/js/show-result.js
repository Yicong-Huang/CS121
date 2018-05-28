
function handleSearchInput(){
	//get the search input and get rid of the 
	let textlist = document.getElementsByName("Text")[0].value.split(" ");
	textlist = textlist.map(text => {return text.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"")});
	console.log(textlist);

	return textlist.join(',');
}


function handleSearch(){
	let text = handleSearchInput();
	//handleSearchResult();
	console.log(text);

	jQuery.ajax({
		dataType:"json",
		data:{'queries':text},
		url:"api/search",
		method:"POST",
		success:(resultData)=>handleSearchResult(resultData)
	});
}

function handleSearchResult(resultData){
	//show the search result
	console.log(resultData);

	let showResultElement = jQuery("#show_result");
	showResultElement.empty();
	let rowHtml = "";
	for(let i = 0; i < Math.min(10,resultData.length); i++){
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
