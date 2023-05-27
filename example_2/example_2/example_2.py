import pynecone as pc


class State(pc.State):
    items = ["Sandwich", "Beer", "Chips"]
    new_item: str

    def add_item(self):
        self.items += [self.new_item]
        self.new_item = ""

    def delete_item(self, item):
        self.items = [i for i in self.items if i != item]


def render_item(item):
    """Render an item in the todo list."""
    return pc.list_item(
        pc.hstack(
            pc.button(
                "x",
                on_click=lambda: State.delete_item(item),
                height="1.5em",
                bg="red",
                color="white"
            ),
            pc.text(item, font_size="1.25em"),
        )
    )


def todo_list():
    """A view of the todo list."""
    return pc.container(
        pc.vstack(
            pc.heading("Order Request Form"),
            pc.input(
                on_blur=State.set_new_item,
                placeholder="Add a todo...",
                bg="white",
            ),
            pc.button("Add", on_click=State.add_item, bg="green", color="white"),
            pc.divider(),
            pc.ordered_list(
                pc.foreach(State.items, lambda item: render_item(item)),
            ),
            bg="#ededed",
            margin="5em",
            padding="1em",
            border_radius="0.5em",
            shadow="lg",
        )
    )


app = pc.App(state=State)
app.add_page(todo_list, route="/")
app.compile()