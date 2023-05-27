import pynecone as pc
import uuid, json

class Order(pc.Model, Table=True):
    id: str
    item:str 
    price:float
    def __init__(self, item, price):
        pk = uuid.uuid4()
        # Make id JSON compatible
        self.id = json.dumps({"pk": pk}, default=str)
        self.item = item
        self.price = price
    def __repr__(self) -> str:
        return f"Order(food={self.item}, price={self.price})"

food_options = ["Burger", "Fries", "Coke", "Hot Dog"]
food_prices = [5.99, 1.99, 1.99, 2.99]

class OrderState(pc.State):
    orders:list[Order] = [Order("Burger", 5.99), Order("Fries", 1.99)]
    new_item: str
    new_price: float

    def add_item(self):
        item_index = food_options.index(self.new_item)
        self.new_price = food_prices[item_index]
        order = Order(self.new_item, self.new_price)
        self.orders += [order]
        self.new_item = ""
        self.new_price = 0

    def delete_item(self, order):
        self.orders.remove(order)

def show_order(order):
    print(order.price)
    order_layout = pc.list_item(
                        pc.hstack(
                            pc.button(
                                "x",
                                on_click=lambda: OrderState.delete_item(order),
                                height="1.5em",
                                bg="red",
                                color="white"
                            ),
                            pc.text(order.item, font_size="1.25em"),
                            pc.text(order.price, font_size="1.25em")
                    )
            )
    return order_layout


def order_list():
    """A view of the todo list."""
    return pc.container(
        pc.vstack(
            pc.heading("Order Request Form"),
            pc.select(
                food_options,
                placeholder="Select an example.",
                on_change=OrderState.set_new_item,
            ),
            pc.button("Add", on_click=OrderState.add_item, bg="green", color="white"),
            pc.divider(),
            pc.list(
                    pc.foreach(OrderState.orders, lambda order: show_order(order))
            ),
            pc.button("Pay", on_click=pc.redirect('/receipt'), bg="green", color="white"),
            bg="#ededed",
            margin="5em",
            padding="1em",
            border_radius="0.5em",
            shadow="lg",
        )
    )

def show_receipt(order:Order):
    return pc.tr(
        pc.td(order.item),
        pc.td(order.price),
    )

def receipt():
    return pc.container(
        pc.vstack(
            pc.heading('Receipt'),
            pc.table_container(
                pc.table(
                    pc.thead(
                        pc.tr(
                            pc.th("Name"),
                            pc.th("Price"),
                        )
                    ),
                    pc.tbody(pc.foreach(OrderState.orders, show_receipt)),
                )
            )
        )
    )

app = pc.App(state=OrderState)
app.add_page(order_list, route="/")
app.add_page(receipt, route="/receipt")
app.compile()
