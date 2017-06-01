var xhttp = new XMLHttpRequest();
var currencyBaseSymbol = 'EUR';
var curFromElement = document.getElementById("cur_from");
var curToElement = document.getElementById("cur_to");
var curTextElement = document.getElementById("cur_text");
var resultElement = document.getElementById("result"); 

/*
    Implement function that fills currency from/to select boxes with currency codes
    and fills scrolling text with rates against currencyBaseSymbol
*/
function loadCurrency(currentCurrencyBase=currencyBaseSymbol) {
   // 2. Конфигурируем его: GET-запрос на URL 'phones.json'
	xhttp.open('GET', 
		'http://api.fixer.io/latest?base=' + currentCurrencyBase);

	xhttp.onload = function (e) {
	    if (xhttp.readyState == 4 && xhttp.status == 200) {
			// clear all privious options
			$(curFromElement).find('option').remove();
			$(curToElement).find('option').remove();
			
		   // вывести результат 
		    var result = JSON.parse( xhttp.responseText );
		    console.log(result);
	        $(curFromElement).append($("<option></option>")
			                    .attr("value",0)
			                    .text(result.base));
	        $(curTextElement).text('BASE - ' + currentCurrencyBase +' => ');
	        $.each(result.rates, function(key, value) {   
			     $(curFromElement).append($("<option></option>")
			                    .attr("value",value)
			                    .text(key)); 
			     $(curToElement).append($("<option></option>")
			                    .attr("value",value)
			                    .text(key));
				var newTextForCurText =  $(curTextElement).text() 
						+ key + ': ' + value + ', ';
	        	$(curTextElement).text(newTextForCurText);     
			});
	    } else {
	    	console.log( xhttp.status + ': ' + xhttp.statusText ); 
	    }
	};
	xhttp.send(null);

	// 3. Отсылаем запрос
	/*xhttp.send();

	// 4. Если код ответа сервера не 200, то это ошибка
	if (xhttp.status != 200) {
	  // обработать ошибку
	  console.log( xhttp.status + ': ' + xhttp.statusText ); // пример вывода: 404: Not Found
	} else {
		// clear all privious options
		$(curFromElement).find('option').remove();
		$(curToElement).find('option').remove();
		
	  // вывести результат 
	    var result = JSON.parse( xhttp.responseText );
	    console.log(result);
        $(curFromElement).append($("<option></option>")
		                    .attr("value",0)
		                    .text(result.base));
        $(curTextElement).text('BASE - ' + currentCurrencyBase +' => ');
        $.each(result.rates, function(key, value) {   
		     $(curFromElement).append($("<option></option>")
		                    .attr("value",value)
		                    .text(key)); 
		     $(curToElement).append($("<option></option>")
		                    .attr("value",value)
		                    .text(key));
			var newTextForCurText =  $(curTextElement).text() 
					+ key + ': ' + value + ', ';
        	$(curTextElement).text(newTextForCurText);     
		});
		
	}*/
}

 

/*
    Implement function that converts from one selected currency to another 
    filling result text area.
 */
function getRates() {
	// 1 is default value if nothing is inserted
    var amount = 1;
    var amount_inserted = + document.getElementById('cur_amount').value  ; 
    // if is not number return
    if(!isFinite(amount_inserted)){
    	alert('Not number inserted!');
    	return;
    }
    // if number inserted == 0 return
    if(amount_inserted ==0){  
    	alert('0 is not appropriate number!');
    	return;  
    }
    amount = amount_inserted;  
    // currency rate
    var rate = + $( curToElement ).children("option").filter(":selected").val();
    $(resultElement).text(rate * amount);
}

// Load currency rates when page is loaded
window.onload = function() {
    // Run loadCurrency func to fetch currencies data and set this function to run every 60 sec.
    //(() => {loadCurrency(); setInterval(loadCurrency, 1000 * 60);})();
    (() => {loadCurrency(); setInterval(function(){
    	var currentCurrencyBase = $( curFromElement ).children("option").filter(":selected").text();
	    if(currentCurrencyBase){
	    	loadCurrency(currentCurrencyBase);
	    } else {
	    	loadCurrency();
	    }
	    
    }, 1000 * 60);})();
    var btn = document.getElementById('run');
    btn.addEventListener("click", getRates);

    curFromElement.addEventListener("change", function(){
    	var currentCurrencyBase = $( curFromElement ).children("option").filter(":selected").text();
	    loadCurrency(currentCurrencyBase);
	}, false);

    
};
