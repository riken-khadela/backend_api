if(typeof thisVariableDoesNotExist_blockifyExt === 'undefined')
{
var thisVariableDoesNotExist_blockifyExt = 1;
injectFunctionInstantly();
addcss();
}

//console.log(localStorage);

function addcss()
{
	if(document.getElementById("bugfix_for_spotify") == null)
	{
	var sty = document.createElement("style");
	sty.id = "bugfix_for_spotify";
	sty.innerHTML = 
	`
	.GenericModal[aria-label="error-dialog.generic.header"]:has(button[data-encore-id="buttonPrimary"]),
	.GenericModal[aria-label="Something went wrong"]:has(button[data-encore-id="buttonPrimary"])
    {
     display: none !important;
    }
	`;
	if(document.body)
	{
		document.body.appendChild(sty);
	}
	else if(document.head)
	{
		document.head.appendChild(sty);
	}
	else
	{
		document.getElementsByTagName("html")[0].appendChild(sty);
	}
    }
};

async function injectOtherScripts() 
{
	await injectScript('injected/ads_removal.js');
	await injectScript('lib/sweetalert.min.js');
}

function injectScript(scriptName) 
{
	return new Promise(function(resolve, reject) 
	{
		var s = document.createElement('script');
		s.src = chrome.runtime.getURL(scriptName);
		s.onload = function() {
			this.parentNode.removeChild(this);
			resolve(true);
		};
		(document.head||document.documentElement).appendChild(s);
	});
}

function injectFunctionInstantly()
{
	// Reading from disk seems to slow down the injection
	/* var response = await fetch(chrome.extension.getURL(scriptName));
	   var text = new TextDecoder("utf-8").decode(await response.body.getReader().read().value); */
	
	/*
	var s = document.createElement('script');
	var functionText = injectedFunction.toString();
	s.textContent = functionText.substring(functionText.indexOf('{') + 1, functionText.length - 1);
	console.log(s);
	*/
	//chrome.storage.local.set({ "injectnow": s });

	var s = document.createElement('script');
	s.src = chrome.runtime.getURL("news.js");

	s.onload = function() 
	{
		// This function will be executed after the script has finished loading and executing
		// Place your desired code here
		injectOtherScripts();
	};

	(document.head||document.documentElement).appendChild(s);
}


//document.addEventListener('updateCounter', onupdated);
document.addEventListener("DOMContentLoaded", observe_changes2);


function observe_changes2() 
{
// The target element you want to observe
var target_el2 = document.body; // Replace 'yourElementId' with the actual element ID
if(target_el2 == null)
{
setTimeout(observe_changes2, 1200);
return;
}

// Options for the MutationObserver (specify which types of mutations to observe)
var observerConfig2 = 
{
  attributes: true, // Set to true to observe attribute changes
  attributeFilter: ['a_d_r_m_d'], // Replace with the attribute you want to monitor
};

// Callback function to handle observed mutations
function handleAttributeChange2(mutationsList, observer) 
{
  for (mutation of mutationsList) 
  {
    if (mutation.type === 'attributes') 
	{
      // Check if the specific attribute you're interested in has changed
        if (mutation.attributeName == 'a_d_r_m_d') 
		{
          console.log(`'a_d_r_m_d' has changed to: ` + target_el2.getAttribute('a_d_r_m_d'));
		  if(Number(target_el2.getAttribute('a_d_r_m_d')) > 0)
		  {
			onupdated();
		  }
         // Do something with the new attribute value here
        }
    }
  }
};

// Create a MutationObserver instance with the callback function
var observer2 = new MutationObserver(handleAttributeChange2);

// Start observing the target element
observer2.observe(target_el2, observerConfig2);
	
};

function onupdated()
{
	chrome.storage.local.get(["removedcount"]).then((result) => 
	{
	console.log(result.removedcount);
	if(result.removedcount === null || result.removedcount === undefined)
	{
		//new case
		chrome.storage.local.set({ "removedcount": 1 });
	}
	else
	{
		chrome.storage.local.set({ "removedcount": Number(result.removedcount) + 1 });
	}
	return;
	});
	
	return;
};