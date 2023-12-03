chrome.runtime.onInstalled.addListener(onins);
chrome.action.onClicked.addListener(opensp);
chrome.commands.onCommand.addListener(kbshortcut);
chrome.runtime.onMessage.addListener((request, sender) => 
{
    if (request.muteTab) 
    {
      chrome.tabs.update(sender.tab.id, {muted: true});
    }
    else if (request.Unmute) 
    {
      chrome.tabs.update(sender.tab.id, {muted: false});
    }

    return true;
});