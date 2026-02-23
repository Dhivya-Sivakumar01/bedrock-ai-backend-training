from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

class ItemDetails(TypedDict):
    name: str
    price: float
    description: str

class SubscriptionType(TypedDict):
    type: Literal["gold","silver","bronze"]
    discount: float 

class State(TypedDict):
    item: str
    subscription_type: Literal["gold","silver","bronze"]
    get_product_price: ItemDetails
    get_discount: SubscriptionType
    apply_discount: float

def get_product_price(state: State):
    '''
    Tool that gets the price of items
    '''
    items:list[ItemDetails] = [
        {"name":"Laptop","price":1050,"description":"laptop description"}, {"name":"Headphone","price": 50,"description":"laptop description"}, {"name":"Mouse","price": 5,"description":"laptop description"}
        ]
    for item_iter in items:
        if item_iter["name"].lower() == state['item'].lower():
            print("Get Product price: ", item_iter["price"])
            return {"get_product_price":item_iter}
    return {"get_product_price":{}}

def get_discount(state: State):
    '''
    Tool that gets the discount of subscription, subscription_type available gold, silver, bronze
    '''
    discount_details:list[SubscriptionType] = [{"type":"Gold","discount":0.2}, {"type":"Silver","discount":0.1}, {"type":"Bronze","discount":0.05}]
    for dis_iter in discount_details:
        if dis_iter['type'].lower() == state['subscription_type'].lower():
            print("Get discount: ", dis_iter['discount'])
            return {"get_discount":dis_iter}
    return {"get_discount":{}}

def apply_discount(state: State):
    '''
    Tool that applies the discount on the product price
    '''
    return {"apply_discount":state['get_product_price']['price']+(state['get_product_price']['price']*state['get_discount']['discount'])}

parallel_builder = StateGraph(State)
parallel_builder.add_node("get_product_price", get_product_price)
parallel_builder.add_node("get_discount", get_discount)
parallel_builder.add_node("apply_discount", apply_discount)

parallel_builder.add_edge(START, "get_product_price")
parallel_builder.add_edge(START, "get_discount")
parallel_builder.add_edge("get_product_price", "apply_discount")
parallel_builder.add_edge("get_discount", "apply_discount")
parallel_builder.add_edge("apply_discount", END)
parallel_workflow = parallel_builder.compile()

png_bytes = parallel_workflow.get_graph().draw_mermaid_png()
display(Image(png_bytes))
with open("graph.png", "wb") as f:
    f.write(parallel_workflow.get_graph().draw_mermaid_png())

state = parallel_workflow.invoke({"item": "laptop","subscription_type":"gold"})
print(state["apply_discount"])