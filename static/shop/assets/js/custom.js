const currentUrl = window.location.href;
const currentParams = new URLSearchParams(window.location.search);

// http://localhost:8000/shop.html?order=price --> /shop.html
const currentPath = new URL(currentUrl).pathname;
const currentCategory = getSlug();
const currentPlanting = currentParams.get("planting");
const currentOrder = currentParams.get("order") || "-price";

const relatedProductsSection = $(".product-related-item");
const productId = relatedProductsSection.attr("data-id");

const categorySelect = $(".category-select");
const specialProductsSection = $(".featured__filter");

$(`ul.list-category > li[data-active="${currentCategory}"]`).addClass("active");

$(
  `.list-planting-method > a > span[data-active="${currentPlanting}"]`
).addClass("active");

$(`select#sort-product > option[data-active="${currentOrder}"]`).attr(
  "selected",
  true
);

$(`ul.main-nav > li > a[href="${currentPath}"]`).parent().addClass("active");

$(`ul.main-nav > li[data-active="${currentCategory}"]`).addClass("active");

$("#sort-product").change(function () {
  let selectedValue = $(this).val();
  window.location.href = selectedValue;
});

function getSlug() {
  let pathname = new URL(currentUrl).pathname;
  let slug = pathname.substring(1, pathname.lastIndexOf(".html"));

  return slug;
}

if (productId) loadProductsRelated(productId);
function loadProductsRelated(productId) {
  $.ajax({
    url: `/api/products/related/${productId}/?order=price&limit=10`,
    method: "GET", // GET,POST,PUT,DELETE
    dataType: "json",
    contentType: "json",
    beforeSend: function (xhr) {
      xhr.setRequestHeader(
        "Authorization",
        "Basic " + btoa("admin@example.com" + ":" + "123")
      );
    },
    success: function (data) {
      data.forEach(function (item) {
        const productHtml = templateProductRelated(item);
        relatedProductsSection.append(productHtml);
      });
    },
    error: function (xhr, status, error) {
      console.error(error);
    }
  });
}
categorySelect.first().attr("data-get", "clicked");
loadProductsSpecial(
  categorySelect.first().attr("data-filter").replace(".category-", ""),
  categorySelect.first()
);

categorySelect.click(function () {
  const self = $(this);
  const categoryId = self.attr("data-filter");
  if (self.attr("data-get") == "clicked") {
    $(".product-item").hide();
    $(categoryId).show();
  } else {
    loadProductsSpecial(categoryId.replace(".category-", ""), self);
  }
});
function loadProductsSpecial(categoryId, self) {
  $.ajax({
    url: `/api/products/category/${categoryId}/?order=price`,
    method: "GET", // GET,POST,PUT,DELETE
    dataType: "json",
    contentType: "json",
    beforeSend: function (xhr) {
      xhr.setRequestHeader(
        "Authorization",
        "Basic " + btoa("admin@example.com" + ":" + "123")
      );
    },
    success: function (data) {
      console.log(data);
      $(".product-item").hide();
      data.forEach(function (item) {
        const productHtml = templateProductsSpecial(item);
        specialProductsSection.append(productHtml);
      });
      self.attr("data-get", "clicked");
    },
    error: function (xhr, status, error) {
      console.error(error);
    }
  });
}

function get_price_old(price, price_sale) {
  return price_sale ? price : "";
}

function format_currency(price) {
  if (price == "") {
    return "";
  }
  const formatted_number = new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND"
  }).format(price);
  return formatted_number.replace(/\s/g, "");
}
