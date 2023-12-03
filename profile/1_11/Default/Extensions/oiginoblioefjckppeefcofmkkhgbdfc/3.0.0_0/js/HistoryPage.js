import { historyService } from "./Services/HistoryService.js";
class HistoryPage {
    loader = document.querySelector(".loader");
    pgbProgress = document.querySelector(".progress");
    lstHistory = document.querySelector(".list-history");
    historyTemplate = this.lstHistory.querySelector("#template-item").innerHTML;
    anchorTemplate = this.lstHistory.querySelector("#template-anchor").innerHTML;
    lblItemCount = document.querySelector(".item-count");
    cboJump = document.querySelector(".cbo-jump");
    btnDeleteFiltered = document.querySelector(".btn-delete-filtered");
    lblDeleteFiltered = document.querySelector(".lbl-delete-filtered");
    btnClear = document.querySelector(".btn-clear");
    txtSearch = document.querySelector("#txt-search");
    txtStart = document.querySelector("#txt-start");
    txtEnd = document.querySelector("#txt-end");
    currCount = 0;
    init() {
        var now = new Date();
        this.txtEnd.value = this.toStandardDateString(now);
        now.setDate(now.getDate() - 7);
        this.txtStart.value = this.toStandardDateString(now);
        this.lstHistory.addDelegate("click", ".btn-delete", (_, el) => this.onDeleteSingleItem(el));
        document.querySelector(".frm-filter").addEventListener("submit", e => {
            e.preventDefault();
            this.onFilter();
        });
        this.cboJump.addEventListener("change", () => this.onJumpRequested());
        this.btnDeleteFiltered.addEventListener("click", () => this.onDeleteFiltered());
        this.btnClear.addEventListener("click", () => this.onDeleteAllRequested());
        document.body.loc();
        this.showItemCount(0);
        this.showLoader(false);
    }
    async searchAsync(limit) {
        await this.runWithLoadingAsync(async () => {
            this.showLoader(true);
            const term = this.txtSearch.value;
            const now = new Date();
            let start = new Date(this.txtStart.value);
            let end = new Date(this.txtEnd.value);
            end.setDate(end.getDate() + 1);
            if (end > now) {
                end = now;
            }
            if (start > end) {
                start = end;
            }
            const items = await historyService.searchAsync(term, start, end, limit);
            this.showItems(items);
        });
    }
    showItems(items) {
        const lst = this.lstHistory;
        if (items.length == 0) {
            lst.innerHTML = "";
            this.showItemCount(0);
            return;
        }
        let currDate = new Date(items[0].lastVisitTime);
        historyService.setToStartOfDate(currDate);
        const frag = new DocumentFragment();
        const firstAnchor = this.appendAnchor(frag, currDate);
        const dateAnchors = [firstAnchor,];
        for (const item of items) {
            const d = new Date(item.lastVisitTime);
            if (d < currDate) {
                currDate = new Date(item.lastVisitTime);
                historyService.setToStartOfDate(currDate);
                const anchor = this.appendAnchor(frag, currDate);
                dateAnchors.push(anchor);
            }
            const el = this.historyTemplate.toElement();
            el.item = item;
            el.setAttribute("title", item.title + "\r\n" + item.url);
            const titleEl = el.querySelector(".item-title");
            const titleContent = item.title || item.url;
            titleEl.textContent = titleContent;
            el.setChildContent(".item-url", item.url);
            el.setChildContent(".item-time", d.toLocaleTimeString());
            el.querySelector(".img-icon").setAttribute("src", historyService.getFavIcon(item.url));
            el.querySelector(".item-link").setAttribute("href", item.url);
            frag.appendChild(el);
        }
        lst.innerHTML = "";
        lst.appendChild(frag);
        this.showItemCount(items.length);
        this.showAnchors(dateAnchors);
    }
    showAnchors(anchors) {
        const frag = new DocumentFragment();
        for (let anchor of anchors) {
            const opt = document.createElement("option");
            opt.value = anchor.anchorId;
            opt.text = anchor.anchorText;
            frag.appendChild(opt);
        }
        const cbo = this.cboJump;
        cbo.innerHTML = "";
        cbo.appendChild(frag);
        this.onJumpRequested();
    }
    onJumpRequested() {
        const id = this.cboJump.value;
        document.querySelector("#" + id).scrollIntoView();
    }
    appendAnchor(frag, date) {
        const el = this.anchorTemplate.toElement();
        const a = el.querySelector(".date-link");
        a.id = "date-" + this.toStandardDateString(date);
        a.href = "#" + a.id;
        const anchorText = date.toDateString();
        el.setChildContent(".date-text", anchorText);
        el.anchorId = a.id;
        el.anchorText = anchorText;
        frag.appendChild(el);
        return el;
    }
    showItemCount(count) {
        this.currCount = count;
        this.lblItemCount.innerHTML = "ItemCount".loc().formatUnicorn(count);
        this.lblDeleteFiltered.innerHTML = "RemoveFiltered".loc().formatUnicorn(count);
        this.cboJump.disabled = this.btnDeleteFiltered.disabled = count <= 0;
    }
    onFilter() {
        this.searchAsync();
    }
    toStandardDateString(d) {
        return d.toJSON().substr(0, 10);
    }
    async onDeleteFiltered() {
        if (!confirm("RemoveFilteredConfirm".loc().formatUnicorn(this.currCount))) {
            return;
        }
        await this.runWithLoadingAsync(async () => {
            const urls = [];
            this.lstHistory.querySelectorAll(".history-item").forEach(el => urls.push(el.item.url));
            await historyService.deleteUrlsAsync(urls, (done, total) => this.setProgress(Math.floor(done / total * 100)));
        }, true);
        await this.searchAsync();
    }
    async onDeleteAllRequested() {
        if (!confirm("RemoveAllConfirm".loc())) {
            return;
        }
        await this.runWithLoadingAsync(async () => {
            await historyService.deleteAllAsync();
        });
        await this.searchAsync();
    }
    async runWithLoadingAsync(action, showProgressBar = false) {
        try {
            this.showLoader(true, showProgressBar);
            await action();
        }
        catch (e) {
            console.error(e);
        }
        finally {
            this.showLoader(false);
        }
    }
    async onDeleteSingleItem(el) {
        const historyEl = el.closest(".history-item");
        const item = historyEl.item;
        await historyService.deleteUrlAsync(item.url);
        historyEl.remove();
        this.showItemCount(this.currCount - 1);
    }
    showLoader(isLoading, showProgressBar = false) {
        this.loader.classList.toggle("d-none", !isLoading);
        this.pgbProgress.classList.toggle("d-none", !showProgressBar);
    }
    setProgress(perc) {
        this.pgbProgress.querySelector(".progress-bar")
            .style.width = perc + "%";
    }
}
new HistoryPage().init();
//# sourceMappingURL=HistoryPage.js.map