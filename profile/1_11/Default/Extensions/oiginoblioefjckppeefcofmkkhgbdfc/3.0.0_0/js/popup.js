import { historyService } from "./Services/HistoryService.js";
class PopupPage {
    lstHistory = document.querySelector(".list-history");
    historyTemplate = this.lstHistory.querySelector("template").innerHTML;
    txtSearch = document.querySelector(".txt-search");
    async init() {
        this.initRateUs();
        document.body.loc();
        await this.showList();
        this.txtSearch.addEventListener("input", () => this.showList());
        this.lstHistory.addDelegate("click", ".btn-delete", (_, el) => this.onDelete(el));
    }
    async showList() {
        const term = this.txtSearch.value;
        const items = await historyService.searchAsync(term);
        const frag = new DocumentFragment();
        for (let item of items) {
            const el = this.historyTemplate.toElement();
            el.item = item;
            el.setChildContent(".item-title", item.title);
            el.setChildContent(".item-time", new Date(item.lastVisitTime).toLocaleTimeString());
            el.querySelector(".img-icon").setAttribute("src", historyService.getFavIcon(item.url));
            el.querySelector(".item-link").setAttribute("href", item.url);
            frag.appendChild(el);
        }
        const lst = this.lstHistory;
        lst.innerHTML = "";
        lst.appendChild(frag);
    }
    async onDelete(el) {
        const item = el.closest(".history-item").item;
        await historyService.deleteUrlAsync(item.url);
        this.showList();
    }
    initRateUs() {
        const updateUrl = chrome.runtime.getManifest().update_url?.toLowerCase();
        const id = chrome.runtime.id;
        const storeUrl = (updateUrl && updateUrl.includes("microsoft")) ?
            `https://microsoftedge.microsoft.com/addons/detail/` + id :
            "https://chrome.google.com/webstore/detail/" + id;
        document.querySelectorAll(".btn-rate").forEach(el => el.setAttribute("href", storeUrl));
    }
}
new PopupPage().init();
//# sourceMappingURL=popup.js.map