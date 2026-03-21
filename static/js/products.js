const productList = document.getElementById("productList");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const sortStatus = document.getElementById("sortStatus");

function renderProducts(items) {
  productList.innerHTML = "";

  if (items.length === 0) {
    productList.innerHTML = "<p>😣 No products found.</p>";
    return;
  }

  items.forEach(product => {
    const card = document.createElement("article");
    card.className = "card product";

    card.innerHTML = `
      <h3>${product.name}</h3>
      <p class="price">NOK ${Number(product.price)}</p>
      <p>Stock: ${product.stock}</p>
      <p>Category: ${product.category}</p>
      <a class="btn primary" href="/product/${product.productId}">View details</a>
    `;

    productList.appendChild(card);
  });
}

function filterProducts(items, searchText) {
  const keywords = searchText
    .toLowerCase()
    .trim()
    .split(/\s+/)
    .filter(word => word.length > 0);

  if (keywords.length === 0) return items;

  return items.filter(product => {
    const text = `
      ${product.name}
      ${product.category}
    `.toLowerCase();

    return keywords.every(keyword => text.includes(keyword));
  });
}

function sortProducts(items, sortValue) {
  const sorted = [...items];

  if (sortValue === "name-asc") {
    sorted.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sortValue === "price-asc") {
    sorted.sort((a, b) => Number(a.price) - Number(b.price));
  } else if (sortValue === "price-desc") {
    sorted.sort((a, b) => Number(b.price) - Number(a.price));
  }

  return sorted;
}

function updateSortStatus(sortValue) {
  const labels = {
    "name-asc": "Sorted by Name in Ascending Order",
    "price-asc": "Sorted by Price in Ascending Order",
    "price-desc": "Sorted by Price in Descending Order"
  };

  sortStatus.textContent = labels[sortValue] || "";
}

function applyFiltersAndRender() {
  const searchText = searchInput.value;
  const sortValue = sortSelect.value;

  let result = filterProducts(products, searchText);
  result = sortProducts(result, sortValue);

  renderProducts(result);
  updateSortStatus(sortValue);

  localStorage.setItem("productSort", sortValue);
}

searchInput.addEventListener("input", applyFiltersAndRender);
sortSelect.addEventListener("change", applyFiltersAndRender);

const savedSort = localStorage.getItem("productSort");
if (savedSort) {
  sortSelect.value = savedSort;
}

applyFiltersAndRender();