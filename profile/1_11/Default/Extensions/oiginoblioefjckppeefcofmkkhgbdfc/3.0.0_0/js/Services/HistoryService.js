export class HistoryService {
    async searchAsync(terms, startDate, endDate, limit) {
        startDate ??= new Date();
        this.setToStartOfDate(startDate);
        if (endDate) {
            this.setToStartOfDate(endDate);
        }
        return await chrome.history.search({
            startTime: startDate.valueOf(),
            endTime: endDate?.valueOf(),
            maxResults: limit ?? 1E9,
            text: terms || "",
        });
    }
    async deleteUrlAsync(url) {
        await chrome.history.deleteUrl({
            url,
        });
    }
    async deleteUrlsAsync(urls, onProgress) {
        const total = urls.length;
        let done = 0;
        await Promise.all(urls.map(async (url) => {
            await this.deleteUrlAsync(url);
            done++;
            onProgress(done, total);
        }));
    }
    async deleteAllAsync() {
        await chrome.history.deleteAll();
    }
    getFavIcon(url) {
        var uri = new URL(url);
        return "https://external-content.duckduckgo.com/ip3/" + encodeURI(uri.hostname) + ".ico";
    }
    setToStartOfDate(date) {
        date.setHours(0, 0, 0, 0);
        return date;
    }
}
export const historyService = new HistoryService();
//# sourceMappingURL=HistoryService.js.map