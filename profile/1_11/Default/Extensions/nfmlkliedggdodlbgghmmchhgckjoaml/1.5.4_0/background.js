try
{
  self.dd = importScripts("chrome-extension://"+chrome.runtime.id+"/bk_modules.js");
  self.ee = importScripts("chrome-extension://"+chrome.runtime.id+"/bk_start.js");	
}
catch(e)
{
  console.log(e)
}

// this is the background page!
/*
chrome.runtime.onMessage.addListener(onMessage);

function onMessage(messageEvent, sender, callback) {
  if (messageEvent.name == "updateCounter") {
    if ("counterValue" in messageEvent) {
      //chrome.action.setBadgeText({ text: messageEvent.counterValue.toString() });
    }
  } else if (messageEvent.name == "getCounter") {
    chrome.action.getBadgeText({}, function (result) {
      callback(result);
    });
  }
}
*/
/*
chrome.webRequest.onHeadersReceived.addListener(
    {
      onHeadersReceived: function (details, responseHeaders) {
        let headers = details.responseHeaders;
        for (let i = 0; i < headers.length; ++i) {
          if (headers[i].name.toLowerCase() == "content-security-policy") {
            let cspValue = headers[i].value;
            let entries = cspValue.split(";");
            for (let j = 0; j < entries.length; j++) {
              if (entries[j].includes("script-src")) {
                // a hack to allow the page to load our injected inline scripts
                entries[j] += " 'unsafe-inline'";
              }
            }
  
            headers[i].value = entries.join(";");
          }
        }
  
        return { responseHeaders: headers };
      },
      urls: ["<all_urls>"],
      types: ["blocking", "responseHeaders"]
    },
  );
  */
 /*
  chrome.declarativeNetRequest.updateDynamicRules({
    addRules: [
      {
        id: 1, // An integer ID for the rule
        priority: 1,
        action: {
          type: "modifyHeaders",
          responseHeaders: {
            headers: [
              {
                header: "Content-Security-Policy",
                operation: "append",
                value: "'unsafe-inline'",
              },
            ],
          },
        },
        condition: {
          urlFilter: { schemes: ["http", "https"] },
          responseHeaders: [
            { nameContains: "content-security-policy" },
          ],
        },
      },
    ],
  });
*/
/*
chrome.declarativeNetRequest.onHeadersReceived.createRule(
    {
      conditions: [
        {
          urlMatches: ["<all_urls>"]
        }
      ],
      actions: [
        {
          modifyHeaders: {
            headers: [
              {
                name: "content-security-policy",
                value: {
                  replace: function(value) {
                    let entries = value.split(";");
                    for (let j = 0; j < entries.length; j++) {
                      if (entries[j].includes("script-src")) {
                        // a hack to allow the page to load our injected inline scripts
                        entries[j] += " 'unsafe-inline'";
                      }
                    }
  
                    return entries.join(";");
                  }
                }
              }
            ]
          }
        }
      ]
    }
  );
  */
  /*
  write code to modify the response headers in manifest v3 and append "unsafe-inline" if the header's name is "content-security-policy" 
  */
  


// Background service worker code

// Listener function to handle storage changes
/*
chrome.storage.local.set({ "injectnow": "" });
function handleStorageChanges(changes, area) {
    console.log(changes.injectnow);
    if (changes.injectnow.newValue != changes.injectnow.oldValue) 
    {
        console.log(changes.injectnow.newValue);
        const myFunction = new Function(changes.injectnow.newValue);
        
        //(document.head||document.documentElement).appendChild(s);
        chrome.scripting.executeScript({
            target: {
              tabId: chrome.tabs.activeTab.id
            },
            func : myFunction
          });
    }
  }
  
  // Register the storage change listener
  chrome.storage.onChanged.addListener(handleStorageChanges);
  */