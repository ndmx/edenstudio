(function () {
    "use strict";

    var INDEX_URL = "../assets/document-index.json";
    var TYPE_VALUES = { all: true, privacy: true, terms: true, support: true, compliance: true };
    var TYPE_LABELS = {
        privacy: "Privacy",
        terms: "Terms",
        support: "Support",
        compliance: "App Store review"
    };
    var PRODUCT_ORDER = {
        "PulseTrackr": 0,
        "JxL Scheduler": 1,
        "ParkMemory Hub": 2
    };
    var STOPWORDS = {
        a: true, an: true, the: true, of: true, and: true, or: true, to: true,
        for: true, in: true, on: true, at: true, by: true, is: true, it: true
    };
    var MONTHS = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    var form = document.getElementById("document-search-form");
    var input = document.getElementById("document-search-input");
    var clearButton = document.getElementById("document-search-clear");
    var status = document.getElementById("document-search-status");
    var results = document.getElementById("document-search-results");
    var browse = document.getElementById("document-browse");
    var controls = document.getElementById("document-search-controls");
    var typeButtons = controls
        ? Array.prototype.slice.call(controls.querySelectorAll("[data-document-type]"))
        : [];

    if (!form || !input || !results || !browse) {
        return;
    }

    var documents = [];
    var currentType = "all";
    var searchAvailable = false;

    function tokenize(value) {
        return String(value || "")
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, " ")
            .trim()
            .split(/\s+/)
            .filter(function (token) {
                return token.length >= 2 && !STOPWORDS[token];
            });
    }

    function normalized(value) {
        return String(value || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
    }

    function fieldHas(value, token) {
        return normalized(value).indexOf(token) !== -1;
    }

    function readQuery() {
        return input.value.replace(/\s+/g, " ").trim();
    }

    function readUrlState() {
        var params = new URLSearchParams(window.location.search);
        var query = params.get("q") || "";
        var type = params.get("type") || "all";
        if (!Object.prototype.hasOwnProperty.call(TYPE_VALUES, type)) {
            type = "all";
        }
        return { query: query, type: type };
    }

    function writeUrlState(query, type, replace) {
        var url = new URL(window.location.href);
        if (query) {
            url.searchParams.set("q", query);
        } else {
            url.searchParams.delete("q");
        }
        if (type && type !== "all") {
            url.searchParams.set("type", type);
        } else {
            url.searchParams.delete("type");
        }
        var next = url.pathname + url.search + url.hash;
        if (replace) {
            window.history.replaceState({ q: query, type: type }, "", next);
        } else {
            window.history.pushState({ q: query, type: type }, "", next);
        }
    }

    function setStatus(message) {
        if (status) {
            status.textContent = message;
        }
    }

    function setType(type) {
        currentType = Object.prototype.hasOwnProperty.call(TYPE_VALUES, type) ? type : "all";
        typeButtons.forEach(function (button) {
            var value = button.getAttribute("data-document-type") || "all";
            button.setAttribute("aria-pressed", value === currentType ? "true" : "false");
        });
    }

    function documentHref(url, anchor) {
        if (!/^\.\.\/docs\/[a-z0-9-]+\.html$/i.test(String(url || ""))) {
            return "#";
        }
        if (!anchor) {
            return url;
        }
        if (!/^[A-Za-z][\w:.-]*$/.test(String(anchor))) {
            return url;
        }
        return url + "#" + anchor;
    }

    function formatReviewed(iso) {
        var parts = String(iso || "").split("-");
        if (parts.length !== 3) {
            return "";
        }
        var year = Number(parts[0]);
        var month = Number(parts[1]);
        var day = Number(parts[2]);
        if (!year || !month || !day || !MONTHS[month - 1]) {
            return iso;
        }
        return MONTHS[month - 1] + " " + day + ", " + year;
    }

    function makeExcerpt(text, tokens, limit) {
        var compact = String(text || "").replace(/\s+/g, " ").trim();
        if (!compact) {
            return "";
        }
        var max = limit || 180;
        var lower = compact.toLowerCase();
        var at = -1;
        var i;
        for (i = 0; i < tokens.length; i += 1) {
            var index = lower.indexOf(tokens[i]);
            if (index !== -1 && (at === -1 || index < at)) {
                at = index;
            }
        }
        if (at === -1) {
            if (compact.length <= max) {
                return compact;
            }
            return compact.slice(0, max).replace(/\s+\S*$/, "") + "…";
        }
        var start = Math.max(0, at - Math.floor(max / 3));
        var end = Math.min(compact.length, start + max);
        if (end - start < max) {
            start = Math.max(0, end - max);
        }
        if (start > 0) {
            var nextSpace = compact.indexOf(" ", start);
            if (nextSpace !== -1 && nextSpace - start < 24) {
                start = nextSpace + 1;
            }
        }
        if (end < compact.length) {
            var prevSpace = compact.lastIndexOf(" ", end);
            if (prevSpace > start + 40) {
                end = prevSpace;
            }
        }
        var slice = compact.slice(start, end).trim();
        if (start > 0) {
            slice = "…" + slice;
        }
        if (end < compact.length) {
            slice += "…";
        }
        return slice;
    }

    function tokenHits(value, tokens) {
        var count = 0;
        var i;
        for (i = 0; i < tokens.length; i += 1) {
            if (fieldHas(value, tokens[i])) {
                count += 1;
            }
        }
        return count;
    }

    function matchDocument(doc, tokens) {
        var titleField = doc.title + " " + doc.product;
        var headingField = doc.sections.map(function (section) {
            return section.title;
        }).join(" ");
        var bodyField = doc.sections.map(function (section) {
            return section.text;
        }).join(" ");
        var combined = titleField + " " + headingField + " " + bodyField;
        var i;

        for (i = 0; i < tokens.length; i += 1) {
            if (!fieldHas(combined, tokens[i])) {
                return null;
            }
        }

        var titleHits = tokenHits(titleField, tokens);
        var headingHits = tokenHits(headingField, tokens);
        var bodyHits = tokenHits(bodyField, tokens);
        var sectionMatches = [];

        for (i = 0; i < doc.sections.length; i += 1) {
            var section = doc.sections[i];
            var sectionTitleHits = tokenHits(section.title, tokens);
            var sectionBodyHits = tokenHits(section.text, tokens);
            if (sectionTitleHits || sectionBodyHits) {
                sectionMatches.push({
                    title: section.title,
                    anchor: section.anchor,
                    text: section.text,
                    titleHits: sectionTitleHits,
                    bodyHits: sectionBodyHits
                });
            }
        }

        sectionMatches.sort(function (a, b) {
            if (b.titleHits !== a.titleHits) {
                return b.titleHits - a.titleHits;
            }
            if (b.bodyHits !== a.bodyHits) {
                return b.bodyHits - a.bodyHits;
            }
            return 0;
        });

        var excerptSource = "";
        if (sectionMatches.length) {
            excerptSource = sectionMatches[0].titleHits
                ? sectionMatches[0].title + ". " + sectionMatches[0].text
                : sectionMatches[0].text;
        } else if (doc.sections.length) {
            excerptSource = doc.sections[0].text;
        }

        return {
            doc: doc,
            titleHits: titleHits,
            headingHits: headingHits,
            bodyHits: bodyHits,
            sections: sectionMatches.slice(0, 3),
            excerpt: makeExcerpt(excerptSource, tokens, 180)
        };
    }

    function filteredDocuments(query, type) {
        var tokens = tokenize(query);
        var pool = documents.filter(function (doc) {
            return type === "all" || doc.type === type;
        });

        if (!tokens.length) {
            return pool.slice().sort(function (a, b) {
                var productDelta = productRank(a.product) - productRank(b.product);
                if (productDelta) {
                    return productDelta;
                }
                return a.title.localeCompare(b.title);
            }).map(function (doc) {
                return {
                    doc: doc,
                    titleHits: 0,
                    headingHits: 0,
                    bodyHits: 0,
                    sections: [],
                    excerpt: doc.sections.length ? makeExcerpt(doc.sections[0].text, [], 180) : ""
                };
            });
        }

        var matches = [];
        pool.forEach(function (doc) {
            var match = matchDocument(doc, tokens);
            if (match) {
                matches.push(match);
            }
        });
        matches.sort(function (a, b) {
            if (b.titleHits !== a.titleHits) {
                return b.titleHits - a.titleHits;
            }
            if (b.headingHits !== a.headingHits) {
                return b.headingHits - a.headingHits;
            }
            if (b.bodyHits !== a.bodyHits) {
                return b.bodyHits - a.bodyHits;
            }
            var productDelta = productRank(a.doc.product) - productRank(b.doc.product);
            if (productDelta) {
                return productDelta;
            }
            return a.doc.title.localeCompare(b.doc.title);
        });
        return matches;
    }

    function productRank(product) {
        return PRODUCT_ORDER[product] === undefined ? 99 : PRODUCT_ORDER[product];
    }

    function createEl(tagName, className, text) {
        var node = document.createElement(tagName);
        if (className) {
            node.className = className;
        }
        if (text) {
            node.textContent = text;
        }
        return node;
    }

    function renderResults(matches, query, type) {
        results.replaceChildren();
        matches.forEach(function (match) {
            var doc = match.doc;
            var article = createEl("article", "search-result");
            var reviewed = formatReviewed(doc.reviewed);
            var metaParts = [doc.product, TYPE_LABELS[doc.type] || doc.type];
            if (reviewed) {
                metaParts.push("Reviewed " + reviewed);
            }
            article.appendChild(createEl("p", "search-result-meta", metaParts.join(" · ")));

            var titleLink = createEl("a", "search-result-title", doc.title);
            titleLink.setAttribute("href", documentHref(doc.url));
            var heading = createEl("h2");
            heading.appendChild(titleLink);
            article.appendChild(heading);

            if (match.excerpt) {
                article.appendChild(createEl("p", "search-result-excerpt", match.excerpt));
            }

            if (match.sections.length) {
                var sectionList = createEl("div", "search-result-sections");
                match.sections.forEach(function (section) {
                    if (!section.anchor) {
                        return;
                    }
                    var link = createEl("a", "", section.title || section.anchor);
                    link.setAttribute("href", documentHref(doc.url, section.anchor));
                    sectionList.appendChild(link);
                });
                if (sectionList.childNodes.length) {
                    article.appendChild(sectionList);
                }
            }

            results.appendChild(article);
        });

        if (!matches.length) {
            var empty = createEl("p", "search-result-excerpt");
            if (query && type !== "all") {
                empty.textContent = "No " + (TYPE_LABELS[type] || type).toLowerCase() + " documents match “" + query + "”. Try another term or choose All.";
            } else if (query) {
                empty.textContent = "No documents match “" + query + "”. Try another term, or clear search to browse by product.";
            } else {
                empty.textContent = "No documents in this category.";
            }
            results.appendChild(empty);
        }
    }

    function statusMessage(matches, query, type) {
        var count = matches.length;
        var noun = count === 1 ? "document" : "documents";
        if (!count) {
            if (query && type !== "all") {
                return "No " + (TYPE_LABELS[type] || type).toLowerCase() + " documents match “" + query + "”.";
            }
            if (query) {
                return "No documents match “" + query + "”.";
            }
            return "No documents in this category.";
        }
        if (query && type !== "all") {
            return count + " " + (TYPE_LABELS[type] || type).toLowerCase() + " " + noun + (count === 1 ? " matches “" : " match “") + query + "”.";
        }
        if (query) {
            return count + " " + noun + (count === 1 ? " matches “" : " match “") + query + "”.";
        }
        if (type !== "all") {
            return count + " " + (TYPE_LABELS[type] || type).toLowerCase() + " " + noun + ".";
        }
        return count + " " + noun + ".";
    }

    function showBrowse() {
        results.replaceChildren();
        results.hidden = true;
        browse.hidden = false;
        setStatus("");
    }

    function showResults(matches, query, type) {
        browse.hidden = true;
        results.hidden = false;
        renderResults(matches, query, type);
        setStatus(statusMessage(matches, query, type));
    }

    function apply(options) {
        var query = readQuery();
        var type = currentType;
        var updateUrl = !options || options.updateUrl !== false;

        if (updateUrl) {
            writeUrlState(query, type, true);
        }

        if (!query && type === "all") {
            showBrowse();
            return;
        }

        showResults(filteredDocuments(query, type), query, type);
    }

    function setUnavailable() {
        searchAvailable = false;
        form.setAttribute("aria-disabled", "true");
        input.disabled = true;
        typeButtons.forEach(function (button) {
            button.disabled = true;
        });
        if (clearButton) {
            clearButton.disabled = true;
        }
        results.hidden = true;
        browse.hidden = false;
        setStatus("Document search is unavailable. Browse the library below.");
        if (controls && status && controls.contains(status)) {
            controls.hidden = false;
        }
    }

    function bind() {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            if (searchAvailable) {
                apply({ updateUrl: true });
            }
        });

        input.addEventListener("input", function () {
            if (searchAvailable) {
                apply({ updateUrl: true });
            }
        });

        if (clearButton) {
            clearButton.addEventListener("click", function () {
                if (!searchAvailable) {
                    return;
                }
                input.value = "";
                setType("all");
                apply({ updateUrl: true });
                input.focus();
            });
        }

        typeButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                if (!searchAvailable) {
                    return;
                }
                setType(button.getAttribute("data-document-type") || "all");
                apply({ updateUrl: true });
            });
        });

        window.addEventListener("popstate", function () {
            if (!searchAvailable) {
                return;
            }
            var state = readUrlState();
            input.value = state.query;
            setType(state.type);
            apply({ updateUrl: false });
        });
    }

    function revealControls() {
        if (controls) {
            controls.hidden = false;
        }
    }

    bind();

    fetch(INDEX_URL, { cache: "no-cache" })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Index request failed");
            }
            return response.json();
        })
        .then(function (payload) {
            var list = Array.isArray(payload) ? payload : payload && payload.documents;
            if (!Array.isArray(list) || !list.length) {
                throw new Error("Index is empty");
            }
            documents = list;
            searchAvailable = true;
            revealControls();
            var state = readUrlState();
            input.value = state.query;
            setType(state.type);
            apply({ updateUrl: false });
        })
        .catch(function () {
            setUnavailable();
        });
})();
