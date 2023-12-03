posthog.init('phc_UODIWhWQFLuBJ6sGTleJ4n8wUMgsAB8RZkKHJeYqjro',{api_host:'https://app.posthog.com',persistence:'localStorage'});

// Listen for the 'message' event
/*
window.addEventListener('message', function(event) 
{
    console.log(event.origin);
    if(event.origin.indexOf(".spotify.com") != -1) 
    {
        // == -1 is not found
        // != -1 is found
        //found correct origin
        if(event.data == "blckfy_potential_impression")
        {

         //posthog.capture('potential_impression', {});

        }
    }
  });
*/
window.onload = function()
{
    /*
    if(typeof(posthog) == 'undefined')
    {
      //is undefined - define now    
    }*/
      chrome.storage.local.get(["removedcount"]).then((result) => 
      {
         console.log(result.removedcount);
         chrome.storage.local.get(["installdate"]).then((result) => 
         {
            console.log(result.installdate);
            posthog.capture('onload_userdat', { removedcount: result.removedcount, installdate: result.installdate });
         }); 
      });
};
  