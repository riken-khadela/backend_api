window.onload = function()
{
    document.getElementById("star5").addEventListener("click", thanks);
    document.getElementById("star4").addEventListener("click", thanks);
    document.getElementById("star3").addEventListener("click", thanks);

    document.getElementById("star2").addEventListener("click", openL);
    document.getElementById("star1").addEventListener("click", openL);

    document.getElementById("cross").addEventListener("click", bandkro);
};

function thanks()
{
    document.getElementById("h1").innerHTML = "Thank you for the feedback.";
    document.getElementById("h2").innerHTML = "&nbsp;";
    setTimeout(bandkro, 2400);
    return false;
};

function openL()
{
    chrome.tabs.create({
        url: "https://chrome.google.com/webstore/detail/"+chrome.runtime.id+"/reviews"
      });
    
    setTimeout(bandkro, 2000);
    return false;
};

function bandkro()
{
    window.parent.postMessage('Close the BCE-rating boxx nao', '*');
};