const templateProductRelated = (item) => {
    return `
        <div class="col-lg-4 col-md-6 col-sm-6">
            <div class="product__item">
                <div class="product__item__pic set-bg"
                    style="background-image: url('${item.image}')">
                    <ul class="product__item__pic__hover">
                        <li>
                            <a href="#"><i class="fa fa-heart"></i></a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-retweet"></i></a>
                        </li>
                        <li>
                            <a href="${item.link}">
                                <i class="fa fa-shopping-cart"></i>
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="product__item__text">
                    <h6>
                        <a href="${item.link}">
                            ${item.name}
                        </a>
                    </h6>
                    <h6 class="price_old">${format_currency(
                      get_price_old(item.price, item.price_sale)
                    )}</h6>
                    <h5>${format_currency(item.price_real)}</h5>
                </div>
            </div>
        </div>`;
};

const templateProductsSpecial = (item) => {
    return `
        <div class="col-lg-3 col-md-4 col-sm-6 mix product-item category-${item.category}">
            <div class="featured__item">
                <div
                    class="featured__item__pic set-bg"
                    data-setbg="${item.image}"
                    style="background-image: url('${item.image}')"
                >
                    <ul class="featured__item__pic__hover">
                        <li>
                            <a href="#"><i class="fa fa-heart"></i></a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-retweet"></i></a>
                        </li>
                        <li>
                            <a href="${item.link}">
                                <i class="fa fa-shopping-cart"></i>
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="featured__item__text">
                    <h6><a href="${item.link}">${item.name}</a></h6>
                    <h5>${item.price_real}</h5>
                </div>
            </div>
        </div>`;
};
