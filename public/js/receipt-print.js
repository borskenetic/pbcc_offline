(function () {
    function esc(value) {
        return String(value == null ? '' : value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    window.printThermalReceipt = function printThermalReceipt(receipt) {
        if (!receipt || !receipt.books || receipt.books.length === 0) {
            return;
        }

        const servedBy = String(receipt.served_by || '').trim();
        const servedLine = servedBy ? esc(servedBy) : '______________________';
        const booksHtml = receipt.books.map(function (book) {
            const extra = (book.extra || []).map(function (line) {
                return '<div>' + esc(line) + '</div>';
            }).join('');

            return (
                '<div class="book">' +
                    '<div class="title">' + esc(book.title) + '</div>' +
                    '<div>' + esc(book.author) + '</div>' +
                    '<div>Barcode: ' + esc(book.barcode) + '</div>' +
                    '<div>Due Date: ' + esc(book.due_date) + '</div>' +
                    extra +
                '</div>'
            );
        }).join('');

        const html =
            '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Receipt</title><style>' +
            '@page{size:80mm auto;margin:3mm;}' +
            'html,body{margin:0;padding:0;width:74mm;color:#000;background:#fff;}' +
            'body{font-family:Consolas,"Courier New",monospace;font-size:12px;line-height:1.35;}' +
            'h1{font-size:13px;line-height:1.3;margin:0 0 6px;font-weight:700;}' +
            '.gap{height:10px;}' +
            '.rule{border:0;border-top:1px dashed #000;margin:6px 0;}' +
            '.book{margin:0 0 8px;}' +
            '.title{font-weight:700;}' +
            '</style></head><body>' +
            '<h1>' + esc(receipt.library_name || 'Pangantucan Bukidnon Community College Library') + '</h1>' +
            '<div>' + esc(receipt.when || '') + '</div>' +
            '<div class="gap"></div>' +
            '<div><strong>' + esc(String(receipt.student_name || '').toUpperCase()) + '</strong></div>' +
            '<div>' + esc(receipt.id_number) + '</div>' +
            '<div class="gap"></div>' +
            '<div>' + esc(receipt.heading || "Today's Checkouts") + '</div>' +
            '<hr class="rule">' +
            booksHtml +
            '<hr class="rule">' +
            '<div>Served By: ' + servedLine + '</div>' +
            '</body></html>';

        const iframe = document.createElement('iframe');
        iframe.setAttribute('title', 'Receipt');
        iframe.style.position = 'fixed';
        iframe.style.left = '0';
        iframe.style.top = '0';
        iframe.style.width = '80mm';
        iframe.style.height = '120mm';
        iframe.style.border = '0';
        iframe.style.opacity = '0';
        document.body.appendChild(iframe);

        const frameWindow = iframe.contentWindow;
        const doc = frameWindow.document;
        doc.open();
        doc.write(html);
        doc.close();

        let removed = false;
        function cleanup() {
            if (removed) return;
            removed = true;
            if (iframe.parentNode) iframe.parentNode.removeChild(iframe);
        }

        setTimeout(function () {
            frameWindow.focus();
            frameWindow.onafterprint = cleanup;
            frameWindow.print();
            setTimeout(cleanup, 60000);
        }, 200);
    };
})();
