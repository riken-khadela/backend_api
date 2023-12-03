function opensp() 
{
    chrome.tabs.create({
      url: "https://open.spotify.com/",
      selected: true,
    });
};
//open spotify

function onins(details)
{
  if (details.reason === chrome.runtime.OnInstalledReason.INSTALL) 
  {
    //var url = "https://docs.google.com/forms/d/e/1FAIpQLSfDRdS5-QxUv2_rUA_R5Xuu6F4Imm6KXwEV41L7ZPkAswJDrg/viewform";
    var url = "https://bit.ly/blockify-feedback";
    //"https://chrome.google.com/webstore/detail/"+chrome.runtime.id+"/support"
    chrome.runtime.setUninstallURL(url); //fallback! unintall url

    opensp();//open spotify
    openwelcome(); //welcome the user
  }
  else
  {
    //updated
  }
};

function openwelcome() 
{
  chrome.tabs.create({
    url: chrome.runtime.getURL("welcome/welcome.html"),
    selected: true,
  });
};

function kbshortcut(command) 
{
  console.log(command);
  if (command === "open_spotify") 
  {
    opensp();//open spotify
  }
};