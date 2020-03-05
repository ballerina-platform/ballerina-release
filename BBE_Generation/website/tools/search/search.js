require.config({
    baseUrl: "/search/"
});

require([
    'mustache.min',
    'lunr.min',
    'text!search-results-template.mustache',
    'text!search_index.json',
], function(Mustache, lunr, results_template, data) {
    "use strict";

    function getSearchTerm() {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == 'q') {
                return decodeURIComponent(sParameterName[1].replace(/\+/g, '%20'));
            }
        }
    }

    function getMaxTitles(matchingTitles, allDocs) {
        var maxTitles = {};
        if (matchingTitles.length > 0) {
            for (var i = 0; i < matchingTitles.length; i++) {
                var result = matchingTitles[i];
                var doc = allDocs[result.ref];
                if (maxTitles[doc.title]) {
                    if (maxTitles[doc.title].score < result.score) {
                        maxTitles[doc.title] = doc;
                    }
                } else {
                    maxTitles[doc.title] = doc;
                }
            }
        }
        return maxTitles;
    }

    var index = lunr(function() {
        this.field('text');
        this.ref('index');
    });

    // separate index to search through titles only
    // then add title only once
    // ex: lets say there are two search indexes like below
    //      title : "foo bar" , path: "/samepath" , text : "sample",
    //      title : "foo bar" , path: "/samepath" , text : "sample"
    // when user search for bar, it will return both of above entries
    // But only one is enough to represent the title
    // therefore we do separate seaches for titles and texts and if title is included in the texts we will ignore
    // that particular title result from "title results". If not we will add the max score title result to all list
    var title_index = lunr(function() {
        this.field('title');
        this.ref('index');
    });


    data = JSON.parse(data);
    var documents = {};

    for (var i = 0; i < data.docs.length; i++) {
        var doc = data.docs[i];
        doc.location = "/" + doc.location;
        index.add(doc);
        title_index.add(doc);
        documents[doc.index] = doc;
    }

    var search_results = document.getElementById("mkdocs-search-results");
    var search_input = document.getElementById('mkdocs-search-query');

    var search = function() {
        var query = document.getElementById('mkdocs-search-query').value;
        if (query.length > 1) {
            while (search_results.firstChild) {
                search_results.removeChild(search_results.firstChild);
            }

            if (query === '') {
                return;
            }

            var results = index.search(query);
            var title_results = title_index.search(query);

            var maxTitles = getMaxTitles(title_results, documents);
            var modified_results = [];
            if (results.length > 0) {
                for (var i = 0; i < results.length; i++) {
                    var result = results[i];
                    var doc = documents[result.ref];
                    if (maxTitles[doc.title]) {
                        delete maxTitles[doc.title];
                    }
                    doc.base_url = base_url;
                    doc.summary = doc.text.substring(0, 200);
                    modified_results.push(doc);
                }
            }

            for (var title in maxTitles) {
                var doc = maxTitles[title];
                doc.base_url = base_url;
                doc.summary = doc.text.substring(0, 200);
                modified_results.push(doc);
            }

            if (modified_results.length > 0) {
                for (var i = 0; i < modified_results.length; i++) {
                    var html = Mustache.to_html(results_template, modified_results[i]);
                    search_results.insertAdjacentHTML('beforeend', html);
                }

            } else {
                search_results.insertAdjacentHTML('beforeend', '<p class="error">No results found</p>');
            }

            if (jQuery) {
                /*
                 * We currently only automatically hide bootstrap models. This
                 * requires jQuery to work.
                 */
                jQuery('#mkdocs_search_modal a').click(function() {
                    jQuery('#mkdocs_search_modal').modal('hide');
                });
            }
        } else {
            search_results.innerHTML = '';
        }

    };

    var term = getSearchTerm();
    if (term) {
        search_input.value = term;
        search();
    }

    var typingTimer;

    if (search_input) {
        search_input.addEventListener("keyup", function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(search(), 1000);
        });

        search_input.addEventListener("keydown", function() {
            clearTimeout(typingTimer);
        });
    }

});