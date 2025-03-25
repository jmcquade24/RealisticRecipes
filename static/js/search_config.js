const search = instantsearch({
    indexName: "recipes",
    searchClient: algoliasearch("6RFFC8176O", "392c97f7418954752024680452574f5d"),
});

// Add a search box
search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
        placeholder: 'Search for recipes...',
    }),

    // Display search results
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item: `
                <div>
                    <h2>{{name}}</h2>
                    <p>{{description}}</p>
                    <p><strong>Category:</strong> {{category}}</p>
                </div>
            `,
        },
    }),
]);

search.start();