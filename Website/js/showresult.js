
function handleSearchInput(){
	let text = document.getElementsByName("Text")[0].value;
	text = text.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").replace(" ",",");
	console.log(text);
	
	return text;
}


function handleSearch(){
	let text = handleSearchInput();
	handleSearchResult();
		
	/*
	jQuery.ajax{
		dataType:"json",
		url:"",
		method:"GET",
		success:(resultData)=>handleSearchResult(resultData)
	}*/

	
}

function handleSearchResult(){
	let showResultElement = jQuery("#show_result");
	showResultElement.empty();
	let rowHtml = "";
	for(let i = 0; i < 10; i++){
		rowHtml += "<p id='url'><a href='www.baidu.com'>WWW.baidu.com</a></p>";
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

