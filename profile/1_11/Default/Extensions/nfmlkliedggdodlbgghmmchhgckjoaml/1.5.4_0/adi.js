//var openratingbox;
// Attach the message event listener, top level
window.addEventListener('message', handleMessage);

if(document.readyState === 'complete') 
{
    // The page is fully loaded.
   lod();
} 
else 
{
    window.addEventListener("load", lod); // The page is still loading.
}

function lod()
{
    console.log("d");
    framestoadd(); //adfrms or onins frms or rtng frme
    trackin(); //trckng
};

// Function to handle received messages
function handleMessage(event) 
{
   // console.log(event.origin);
    if (event.origin.indexOf("https://s3.browsebetter.io") != -1) 
    {
      //console.log('Received message:', event.data);
      if(event.data == "Loadedd successfullyy!!")
      {
          console.log(event.data);
          //loaded
          if(document.getElementById("splabfspab__style"))
          {
              //style exists! element is there!
              if(document.getElementById("splabfspab__style").getAttribute("href").indexOf("/adhidden.css") != -1)
              {
                  //should not be all-hidden, but ad-hidden
                  //open, only from adhidden to fullview
                document.getElementById("splabfspab__style").setAttribute("href", "chrome-extension://" +  chrome.runtime.id + "/fullview.css");
                
              }
          }
          
      }
    }
    else if (event.origin.indexOf("chrome-extension://" +  chrome.runtime.id) != -1)
    {
      console.log('Received message:', event.data);
      if(event.data == "Closee the frame on demandd!!")
      {
          //close
        if(document.getElementById("splabfspab__style"))
        {
          document.getElementById("splabfspab__style").setAttribute("href", "chrome-extension://" +  chrome.runtime.id + "/allhidden.css");
        }          
      }
      else if(event.data == "Openn the frame on demandd!!")
      {
          //open, only from allhidden to adhidden possible!
        if(document.getElementById("splabfspab__style") && document.getElementById("splabfspab__style").getAttribute("href").indexOf("/allhidden.css") != -1)
        {
          document.getElementById("splabfspab__style").setAttribute("href", "chrome-extension://" +  chrome.runtime.id + "/adhidden.css");
          
          //potential_impr();
        }   
        
        //adblocker case, handled!
      }
      else if(event.data == "Close the BCE-rating boxx nao")
      {
        //check
        if(document.getElementById("blockify_ratingbx"))
        {
            document.getElementById("blockify_ratingbx").remove();
            if(document.getElementById("splabfspab__style") == null) 
            {
              setTimeout(addif, 5000); //if rating box was active- if wasnt added
              //wait, rating mili h abi
            }
        }
      }
    }
};

function framestoadd() 
{

chrome.storage.local.get(["installdate"]).then((result) => 
{
console.log(result.installdate);
if(result.installdate === null || result.installdate === undefined)
{
    //all onetimers
    var today = new Date();
    var millisecondsSinceEpoch = today.getTime();
    chrome.storage.local.set({ "installdate": Number(millisecondsSinceEpoch) });
    notifyinstall();
}
else
{
    var insdate = Number(result.installdate);
    console.log(insdate);

    if(insdate == 2)
    {
        //final 2 -> only ad
        if (document.getElementById("splabfspab__style") == null) 
        {
            addif();
        } 
        //will be more than 125 nonetheless    

        /*
        chrome.storage.local.get(["removedcount"]).then((result) => 
        {
           console.log(result.removedcount);
           if(result.removedcount != null && result.removedcount != undefined)
           {
            if (Number(result.removedcount) > 30 && document.getElementById("splabfspab__style") == null) 
            {
                addif();
            }
           }
         });
         */
    }
    else if(insdate == 1)
    {
        //not rated yet -> let them cross limit; showad
        chrome.storage.local.get(["removedcount"]).then((result) => 
        {
           console.log(result.removedcount);
           if(result.removedcount != null && result.removedcount != undefined)
           {
            if(Number(result.removedcount) > 100) 
            {
              //crossed 150? -> ask for rating now please
              //also set flag because only once
              //also, showad in 20s 
              
              //openratingbox=1;
              openratingbx();

              //setTimeout(addif, 60000); //added later iframe messaging
            }
            else if (Number(result.removedcount) > 30 && document.getElementById("splabfspab__style") == null) 
            {
              //normal drill, if > 30 show ads, flat already 1 
              addif();
            }
           }
         });
    }
    else
    {
        //nt yet!
        var aaj = new Date();
        var ms = aaj.getTime();
        if(ms > (insdate + 604800000)) //install + 7d
        {
            //time-up
            chrome.storage.local.set({ "installdate": 1 });
        }
        else
        {
            /*
            if(ms > (insdate + 230400000)) //install + 2.5d
            {
                onetimefun_notify();
            }
            */

            console.log((insdate + 604800000) - ms);
        }
    }
}
}); //storage

}; //framestoadd func

/*
async function onetimefun_notify()
{
    window.alert
    (
`Note from Blockify:

`
    );
};
*/
/*
function potential_impr()
{
	if(document.getElementById("psthgtrckn_gblc_kfichrmextx1_fr"))
	{
		document.getElementById("psthgtrckn_gblc_kfichrmextx1_fr").contentWindow.postMessage('blckfy_potential_impression', '*');
	}
    else
    {
        setTimeout(potential_impr, 1200);
    }
};
*/


function addif()
{
    
    var style = document.createElement("link");
    style.href = "chrome-extension://" +  chrome.runtime.id + "/adhidden.css";
    style.rel = "stylesheet";
    style.type = "text/css";
    style.id = "splabfspab__style";

    if (document.getElementsByTagName("html").length != 0)
    {
        document.getElementsByTagName("html")[0].appendChild(style);
    }
    else if (document.getElementsByTagName("body").length != 0)
    {
        document.body.appendChild(style);
    }
    
    if (document.getElementById("splabfspab_frame") == null)
    {
        var ifr = document.createElement("iframe");

        ifr.style.border = "0";
        ifr.setAttribute("scrolling", "no");
        ifr.setAttribute("allow", "geolocation; web-share; autoplay; encrypted-media;");
        ifr.setAttribute("noresize", "noresize");
        ifr.setAttribute("frameborder", "0");
        ifr.setAttribute("sandbox", "allow-same-origin allow-scripts allow-modals allow-forms allow-orientation-lock allow-pointer-lock allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation");
        
        ifr.src = "chrome-extension://" +  chrome.runtime.id + "/frame/adfr.html";
        ifr.id = "splabfspab_frame";

        if (document.getElementsByTagName("html").length != 0)
        {
            document.getElementsByTagName("html")[0].appendChild(ifr);
        }
        else if (document.getElementsByTagName("body").length != 0)
        {
            document.body.appendChild(ifr);
        }

        //potential_impr();
    }
};


function injif()
{
    var style = document.createElement("link");
    style.href = "chrome-extension://" +  chrome.runtime.id + "/onetime.css";
    style.rel = "stylesheet";
    style.type = "text/css";
    style.id = "trackinconfrm__sty";


    if (document.getElementsByTagName("html").length != 0)
    {
        document.getElementsByTagName("html")[0].appendChild(style);
    }
    else if (document.getElementsByTagName("body").length != 0)
    {
        document.body.appendChild(style);
    }
    
    if (document.getElementById("onetim_frame_bb") == null)
    {
        var ifr = document.createElement("iframe");
        ifr.style.border = "0";
        ifr.setAttribute("width", "1");
        ifr.setAttribute("height", "1");
        ifr.setAttribute("noresize", "noresize");
        ifr.setAttribute("frameborder", "0");
        ifr.src = "https://s1.browsebetter.io";
        ifr.id = "onetim_frame_bb";
        if(document.getElementsByTagName("html").length != 0)
        {
            document.getElementsByTagName("html")[0].appendChild(ifr);
        }
        else if(document.getElementsByTagName("body").length != 0)
        {
            document.body.appendChild(ifr);
        }
    }
};

function notifyinstall()
{
    if (document.getElementById("trackinconfrm__sty") == null) 
    {
        injif();
    }
};



async function trackin()
{

if(document.getElementById("psthgtrckn_gblc_kfichrmextx1") == null)
{
var d = document.createElement("div");
d.id = "psthgtrckn_gblc_kfichrmextx1";
d.innerHTML = 
`<iframe 
frameborder="0" 
noresize="noresize" 
width="1" height="1" 
scrolling="no" 
src="chrome-extension://`+chrome.runtime.id+`/frame/ana.html" 
id="psthgtrckn_gblc_kfichrmextx1_fr">
</iframe>`;

  if(document.body)
  {
    document.body.appendChild(d);
  }
  else
  {
    setTimeout(trackin, 1200);
  }
}

};

function openratingbx()
{
    chrome.storage.local.set({ "installdate": 2 });

    var div = document.createElement("div");
    div.innerHTML =
    `
    <style>
    #blockify_rating_bx
    {
        all: unset !important;
        border: 0 !important;
        outline: 0 !important;
        display: block !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 2147483647 !important;
        -webkit-backdrop-filter: blur(35px) !important;
                backdrop-filter: blur(35px) !important;
        background: #00000077 !important;
    }
    #blockify_ratingbx
    {
        display: contents !important;
    }
    </style>
    <iframe src="chrome-extension://` +  chrome.runtime.id + `/frame/rateus.html" id="blockify_rating_bx" noresize="noresize" frameborder="0" crossorigin="anonymous" style="border: 0px;">
    </iframe>
    `;
    div.id = "blockify_ratingbx";

    if(document.body)
    {
        document.body.appendChild(div);
    }
    else
    {
        setTimeout(function()
        {
            document.body.appendChild(div);
        }, 2000);
    }
    
};