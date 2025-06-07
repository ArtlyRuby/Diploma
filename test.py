data = [
    {'telegram_id': 489580031, 'product_name': 'Кровать детская', 'quantity': 2},
    {'telegram_id': 489580031, 'product_name': 'Стол из сосны', 'quantity': 4}
]

message_text = (
    f"📦ID заказа: `dadw12dasdd21d21d-12d12d12d12`\n"
    f"🛒Состав заказа:\n"
)

for i in data:
    message_text += (
        f"  - {i['product_name']} × {i['quantity']}\n"
    )


print(message_text)
