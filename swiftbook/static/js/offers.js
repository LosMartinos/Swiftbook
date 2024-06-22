// static/js/offers.js
document.addEventListener('DOMContentLoaded', function() {
    const offersContainer = document.getElementById('offersContainer');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const pagination = document.getElementById('pagination');
    let currentPage = 1;

    function fetchOffers(query = '', page = 1) {
        fetch(`/offers?q=${query}&page=${page}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                displayOffers(data.offers);
                setupPagination(data.num_pages);
            })
            .catch(error => console.error('Error fetching offers:', error));
            
    }
    

    function displayOffers(offers) {
        offersContainer.innerHTML = '';
        offers.forEach(offer => {
            const offerElement = document.createElement('div');
            offerElement.className = 'col-md-4';
            offerElement.innerHTML = `
                <div class="card mb-4" onclick="location.href='/service/${offer.service_id}'" style="cursor: pointer;">
                    <div class="card-body overflow-y-auto" style="max-height: 20vh;">
                        <h5 class="card-title">${offer.provider_name} - ${offer.service_name}</h5>
                        <p class="card-text">${offer.description}</p>
                    </div>
                </div>
            `;
            offersContainer.appendChild(offerElement);
            console.log(offer.length)
        });
    }

    function setupPagination(numPages) {
        pagination.innerHTML = '';
        for (let i = 1; i <= numPages; i++) {
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            pageItem.addEventListener('click', (e) => {
                e.preventDefault();
                currentPage = i;
                fetchOffers(searchInput.value, currentPage);
            });
            pagination.appendChild(pageItem);
        }
    }

    searchButton.addEventListener('click', () => {
        currentPage = 1;
        fetchOffers(searchInput.value, currentPage);
    });

    // Initial fetch
    fetchOffers();
});
