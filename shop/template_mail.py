from string import Template

TEMPLATE_CONTACT = Template('''
    <p>Chào bạn, cảm ơn bạn đã liên hệ với ZendVN.</p>
    <p>Sau đây là thông tin mà bạn đã để lại:</p>
    <p>Họ Tên: $name</p>
    <p>Email: $email</p>
    <p>Số Điện Thoại: $phone</p>
    <p>Lời Nhắn: $message</p>
    <p>Chúng tôi sẽ liên hệ lại với bạn trong thời gian sớm nhất!</p>
''')

TEMPLATE_ORDER = Template('''
    <p>Chào bạn, cảm ơn bạn đã đặt hàng tại ZendVN.</p>
    <p>Sau đây là thông tin đơn hàng:</p>
    <p>Mã Đơn Hàng: <b>$order_code</b></p>
    <p>Họ Tên: $name</p>
    <p>Email: $email</p>
    <p>Số Điện Thoại: $phone</p>
    <p>Địa Chỉ: $address</p>
    <p>Tổng tiền: $total_order</p>
    <p><b>Danh Sách Sản Phẩm:</b></p>
    <ol>
        $order_items
    </ol>
    <p>Bạn có thể kiểm tra trạng thái đơn hàng tại liên kết sau đây: <a href="$link_order_check">Kiểm tra đơn hàng</a></p>
''')

TEMPLATE_ORDER_ITEMS = Template('''
    <li>$product - Số lượng: $quantity - Đơn giá: $price - Thành tiền: $total</li>
''')