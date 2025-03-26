const baseUrl = window.location.origin;
const recipeUrl = `${baseUrl}/recipes/recipe/`;

const search = instantsearch({
    indexName: "recipes",
    searchClient: algoliasearch("6RFFC8176O", "392c97f7418954752024680452574f5d"),
    searchParameters: {
        "exactOnSingleWordQuery": "word"
    },
    searchFunction(helper) {
        if (helper.state.query) {
            helper.search();
        }
    },
});

// Add a search box
search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
        placeholder: 'Search for recipes...',
        showSubmit: true,
        queryHook(query, search) {
            search(query);
            },
    }),

    // Display search results
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item(hit, { html, components }) {
                return html`
                <li class="hit">
                    <a href="${recipeUrl + hit.slug}" class="hit-title">${components.Highlight({ attribute: 'title', hit })}</a>
                    <p>${hit.description}</p>
                </li>
                
                `;
            },
            },
    }),
]);

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const query = getQueryParam("q");  // Extracts the query from /search/?q=something

search.start();

if (query) {
    console.log(query);
    document.getElementById("searchbox").value = query;
    search.helper.setQuery(query).search();
}
