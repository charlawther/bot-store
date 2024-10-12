from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Пример товаров
products = {
    '1': {'name': 'Товар 1', 'price': 100},
    '2': {'name': 'Товар 2', 'price': 200},
    '3': {'name': 'Товар 3', 'price': 300},
}

cart = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Добро пожаловать в наш интернет-магазин! Введите /catalog для просмотра товаров.')

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(product['name'], callback_data=product_id) for product_id, product in products.items()]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите товар:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_id = query.data
    product = products[product_id]
    cart[product_id] = cart.get(product_id, 0) + 1
    await query.edit_message_text(text=f"Вы добавили {product['name']} в корзину. Цена: {product['price']}₽.\n\nВведите /cart для просмотра корзины.")

async def cart_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cart:
        await update.message.reply_text('Ваша корзина пуста.')
        return
    message = 'Ваша корзина:\n'
    total = 0
    for product_id, quantity in cart.items():
        product = products[product_id]
        message += f"{product['name']} (x{quantity}) - {product['price'] * quantity}₽\n"
        total += product['price'] * quantity
    message += f'\nИтого: {total}₽\n\nВведите /checkout для оформления заказа.'
    await update.message.reply_text(message)

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cart:
        await update.message.reply_text('Ваша корзина пуста. Добавьте товары перед оформлением заказа.')
        return
    total = sum(products[product_id]['price'] * quantity for product_id, quantity in cart.items())
    await update.message.reply_text(f'Спасибо за заказ на сумму {total}₽! Ваши товары будут отправлены в ближайшее время.')
    cart.clear()  # Очистка корзины после оформления заказа

if __name__ == '__main__':
    app = ApplicationBuilder().token('7473297038:AAEkuQvfq78PJxoAyAOyaVEz98n5xqf9xTM').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('catalog', catalog))
    app.add_handler(CommandHandler('cart', cart_view))
    app.add_handler(CommandHandler('checkout', checkout))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
