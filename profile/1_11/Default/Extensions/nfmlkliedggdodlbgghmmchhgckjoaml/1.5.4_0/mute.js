if (typeof window.onlyonetimebugfix === 'undefined') 
{
    window.onlyonetimebugfix = 0; //initialize, just once
}
var time_ele = "";
var time_ele2 = "";
var observer;

console.log("mute");

if(document.readyState === 'complete')
{
    setTimeout(bugfixes, 1300);
    onload();
}
else
{
document.addEventListener('readystatechange', function(e) 
{
 if(document.readyState === 'complete') 
 {
      // The document is fully loaded.
      setTimeout(bugfixes, 1300);
      onload();
 }
 return;
});
}

function bugfixes()
{

//bug fix
var element = document.querySelector('[aria-label="error-dialog.generic.header"]');
var element2 = document.querySelector('[aria-label="Something went wrong"]');

if(element || element2) 
{
    var strmsg = 
    `Blockify can't work properly if there are other Spotify ad-blockers running. Please turn off other Spotify ad-blockers (except Blockify) and reload the page.\n\nAlso, if you have a general/generic ad-blocker installed, please add "open.spotify.com" to the list of exceptions.`;
    alert(strmsg);

    console.log(window.onlyonetimebugfix);
    //either of these elements
    if(element && element.querySelector('[data-encore-id="buttonPrimary"]') && window.onlyonetimebugfix === 0)
    {
        //if element exists and btn inside element and not clicked yet
        //click on button side that element, update flag
        window.onlyonetimebugfix = 1; 
        element.querySelector('[data-encore-id="buttonPrimary"]').click();
        console.log("Spotify bug fixed!"); //should auto-reload once
        if(window.event)
        {
        window.event.stopImmediatePropagation();
        window.event.stopPropagation();
        window.event.preventDefault();
        }
    }
    else if(element2 && element2.querySelector('[data-encore-id="buttonPrimary"]') && window.onlyonetimebugfix === 0)
    {
        window.onlyonetimebugfix = 1;  
        element2.querySelector('[data-encore-id="buttonPrimary"]').click();
        console.log("Spotify bug fixed!"); //should auto-reload once
        if(window.event)
        {
        window.event.stopImmediatePropagation();
        window.event.stopPropagation();
        window.event.preventDefault();
        }
    }
    else if(window.onlyonetimebugfix === 1)
    {
        //should be reloading now
        //should ignore 2nd click, w8
    }
    else
    {
        //window.location.reload();
        //button not found or something
        //can be risky, do not hide

        if(document.getElementById("bugfix_for_spotify"))
        {
          document.getElementById("bugfix_for_spotify").remove();
        } //can't see elements - something else - let the user tackle it

        console.log("Spotify bug found!");
    }
} 
else 
{  
  //all good
  console.log("All good!");
  if(document.getElementById("bugfix_for_spotify"))
  {
    document.getElementById("bugfix_for_spotify").remove();
  } //remove css hider
}
};

function hidetoast() 
{
    var snackbar = document.getElementById("snackbar");
    if(snackbar)
    {
        snackbar.className = snackbar.className.replace("show", ""); 
    }
};

function showToast3(text)
{
    var snackbar = document.getElementById("snackbar");
    if(snackbar)
    {
    snackbar.innerText = text;
    snackbar.className = "show";
    }
}


function onload()
{
    console.log("onlo");

    if(document.getElementsByClassName("playback-bar").length >= 1 && document.getElementsByClassName("playback-bar")[0].className == "playback-bar" && document.getElementsByClassName("playback-bar")[0].getElementsByTagName("input").length == 1)
    {
        time_ele2 = document.getElementsByClassName("playback-bar")[0].getElementsByTagName("input")[0];
        console.log("def1");
    }
    else if(document.querySelector('[data-testid="playback-duration"]'))
    {
        time_ele = document.querySelector('[data-testid="playback-duration"]');
        console.log("def2");
    }
    else if(document.getElementsByClassName("npFSJSO1wsu3mEEGb5bh").length == 1)
    {
        time_ele = document.getElementsByClassName("npFSJSO1wsu3mEEGb5bh")[0];
    }
    else if(document.getElementsByClassName("playback-bar").length >= 1 && document.getElementsByClassName("playback-bar")[0].className == "playback-bar" && (document.getElementsByClassName("playback-bar")[0].lastElementChild.tagName == "DIV" || document.getElementsByClassName("playback-bar")[0].lastElementChild.tagName == "div"))
    {
        time_ele = document.getElementsByClassName("playback-bar")[0].lastElementChild;
    }
    else if(document.getElementsByClassName("fcYQUS").length >= 1)
    {
        time_ele = document.getElementsByClassName("fcYQUS")[document.getElementsByClassName("fcYQUS").length - 1];
    }
    
    console.log(time_ele);
    
    if(time_ele2 != "" && time_ele2 != null && time_ele2 != undefined && time_ele2.getAttribute("max") != null)
    {
        observethis2(time_ele2);
    }
    else if(time_ele != "" && time_ele != null && time_ele != undefined && time_ele.innerText.indexOf(":") != -1)
    {
        observethis(time_ele);
    } 
    else
    {
        setTimeout(onload, 1200);
    }
};

function observethis2(inputElement)
{
// Listens for changes in attributes of the input element
var attributeObserver = new MutationObserver((mutationsList) => 
{
  mutationsList.forEach((mutation) => 
  {
    /*
    if (mutation.type == 'attributes') 
    {
        checkagain2();
    }*/
    checkagain2();
  });
});

var config = { attributes: true, subtree: true, characterData: true };

// Start observing the input element for attribute changes
attributeObserver.observe(inputElement, config);

};

function observethis(targetElement)
{
    console.log(targetElement);
        // Create a MutationObserver instance
        observer = new MutationObserver(function(mutationsList) 
        {
            //console.log(mutationsList);
            for (let mutation of mutationsList) 
            {
                if(mutation.target.textContent.indexOf(":") != -1)
                {
                    console.log('innerHTML changed:', mutation.target.textContent);
                    checkagain();
                }
            }
        });

        // Configure and start observing the target element for changes
        var config = { childList: true, characterData: true, subtree: true };

        observer.observe(targetElement, config);

        // observer.disconnect();
};

function checkagain2()
{
    console.log("check2");

    if(time_ele2.getAttribute("max"))
    {
      if(Number(time_ele2.getAttribute("max")) < 35 && Number(time_ele2.getAttribute("max")) > 1)
      {
        //ad detected!
        //mute now
        chrome.runtime.sendMessage({muteTab: true});

        //fallback also
        /*
        if(document.querySelector('[aria-label="Mute"]'))
        {
            document.querySelector('[aria-label="Mute"]').click();
        }*/

        if(document.querySelector('[aria-label="Next"]'))
        {
            document.querySelector('[aria-label="Next"]').click();
            console.log("clicked");
        } 
        else if(document.querySelector('[data-testid="control-button-skip-forward"]'))
        {
            document.querySelector('[data-testid="control-button-skip-forward"]').click();
            console.log("clicked");
        }
        else if(document.getElementsByClassName("player-controls__right").length > 0)
        {
            if(document.getElementsByClassName("player-controls__right")[0].firstElementChild)
            {
              document.getElementsByClassName("player-controls__right")[0].firstElementChild.click();
            }
        }

        //showToast("Ad Muted");
        //document.dispatchEvent(new CustomEvent('notify_muted'));
        //document.body.setAttribute("a_m_t_d", "true");
        showToast3("Ad Silenced");
        //updateCounter();

        if(Number(time_ele2.getAttribute("max")) === Number(time_ele2.getAttribute("value")) && Number(time_ele2.getAttribute("value")) > 0)
        {
          //recheck and crossconfirm
          setTimeout(checkagain2, 1600);
        }
      }
      else
      {
        //no ads
        //unmute now
        chrome.runtime.sendMessage({Unmute: true});
        //document.dispatchEvent(new CustomEvent('notify_unmuted'));
        //document.body.setAttribute("a_m_t_d", "false");
        hidetoast();

        //fallback also
        /*
        if(document.querySelector('[aria-label="Unmute"]'))
        {
            document.querySelector('[aria-label="Unmute"]').click();
        }
        */
      }
    }
};

function checkagain()
{
    console.log("check");

    var parts = time_ele.innerText.split(":"); // Split the string into parts using colon as separator
    var minutes = parseInt(parts[0]); // Convert the first part to an integer
    var seconds = parseInt(parts[1]); // Convert the second part to an integer
    console.log("m" + minutes + " s" + seconds);

    if(time_ele.innerText.indexOf("-") != -1 && !isNaN(seconds))
    {
        //is not not a number => is a number
        //only click if seconds is a number
        //dont click if seconds is not a number because then it must be "-" or "--"
        //-- or - meaning still loading & in that case loading wala infinite loop, stack over flows 
        
        //negative 
        //negative chal ra
        time_ele.click();
        setTimeout(checkagain, 1000);
        return;
    }


    if(minutes == 0 && seconds < 35 && seconds > 1 && !isNaN(seconds))
    //if(time_ele.innerText == '0:28' || time_ele.innerText == '0:29' || time_ele.innerText == '0:30' || time_ele.innerText == '0:31')
    {
        //ad detected!
        //mute now
        chrome.runtime.sendMessage({muteTab: true});

        //fallback also
        /*
        if(document.querySelector('[aria-label="Mute"]'))
        {
            document.querySelector('[aria-label="Mute"]').click();
        }*/

        if(document.querySelector('[aria-label="Next"]'))
        {
            document.querySelector('[aria-label="Next"]').click();
            console.log("clicked");

            setTimeout(checkagain, 2000); //try one more time in 2 seconds
        }
        else if(document.querySelector('[data-testid="control-button-skip-forward"]'))
        {
            document.querySelector('[data-testid="control-button-skip-forward"]').click();
            console.log("clicked");

            setTimeout(checkagain, 2000); //try one more time in 2 seconds
        }
        else if(document.getElementsByClassName("player-controls__right").length > 0)
        {
            if(document.getElementsByClassName("player-controls__right")[0].firstElementChild)
            {
              document.getElementsByClassName("player-controls__right")[0].firstElementChild.click();

              setTimeout(checkagain, 2000); //try one more time in 2 seconds
            }
        } 

        //showToast("Ad Muted");
        //document.dispatchEvent(new CustomEvent('notify_muted'));
        //document.body.setAttribute("a_m_t_d", "true");
        showToast3("Ad Silenced");
        //updateCounter();
    }
    else
    {
        //no ads
        //unmute now
        chrome.runtime.sendMessage({Unmute: true});
        //document.dispatchEvent(new CustomEvent('notify_unmuted'));
        //document.body.setAttribute("a_m_t_d", "false");
        hidetoast();

        //fallback also
        /*
        if(document.querySelector('[aria-label="Unmute"]'))
        {
            document.querySelector('[aria-label="Unmute"]').click();
        }
        */
    }
};