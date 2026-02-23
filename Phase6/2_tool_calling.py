import boto3
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_aws import ChatBedrockConverse
# from langsmith import traceable


load_dotenv()

@tool
def get_product_price(item: str) -> float:
    '''
    Tool the gets the price of items
    Args: 
        item: The name of the item
    Returns:
        price: float
    '''
    items = [{"name":"Laptop","price":1050}, {"name":"Headphone","price": 50}, {"name":"Mouse","price": 5}]
    for item_iter in items:
        if item_iter["name"].lower() == item.lower():
            return item_iter["price"]
    return 0.0

@tool
def get_discount(subscription_type: str) -> float:
    '''
    Tool the gets the discount of subscription, subscription_type available gold, silver, bronze
    Args: 
        subscription_type: The type of subscription
    Returns:
        discount: float
    '''
    discount_details = [{"Type":"Gold","Discount":0.2}, {"Type":"Silver","Discount":0.1}, {"Type":"Bronze","Discount":0.05}]
    for dis_iter in discount_details:
        if dis_iter["Type"].lower() == subscription_type.lower():
            return dis_iter["Discount"]
    return 0

@tool
def apply_discount(item_price: float, discount_applied: float) -> float:
    '''
    Tool that applies the discount on the product price
    Args:
        item_price: The price of an item
        discount_applied: The discount price
    Returns:
        final_price: float
    '''
    return item_price+(item_price*discount_applied)

# @traceable(name="langchain loop")
def run_agent(question: str):
    tools = [get_product_price, get_discount, apply_discount]
    tools_dict = {t.name: t for t in tools}
    llm = ChatBedrockConverse(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Example model ID
        region_name="us-east-1",  # Specify your AWS region
        model_kwargs={
            "max_tokens": 2048,
            "temperature": 0.7,
        }
    )
    
    # llm = init_chat_model("bedrock:anthropic.claude-3-haiku-20240307-v1:0", temperature=0.5)
    llm_with_tools = llm.bind_tools(tools)
    messages = [
        SystemMessage(
            content=('''You are a helpful AI Assistant. You have access to product catalog tool and discount tool.
                        Follow below rules and steps strictly.
                        1. Never guess or assume product price, instead use tools to get it
                        2. Never guess or assume disount, instead use tools and get value based on subscription type
                        3. Calculate final amount based on tool provided.
                      '''
                    )
            ),
        HumanMessage(content= question),
    ]

    for iteration in range(1,11):
        ai_message = llm_with_tools.invoke(messages)
        tools_calls = ai_message.tool_calls
        if not tools_calls:
            print('final answer: ',ai_message.content)
            return 
        tool_call = tools_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args",{})
        tool_call_id = tool_call.get("id")

        print(f'tool call {tool_name}, tool args {tool_args}, tool id: {tool_call_id}')

        tool_to_use = tools_dict.get (tool_name)
        if tool_to_use is None:
            raise ValueError(f"Tool '{tool_name}' not found" )
        observation = tool_to_use. invoke(tool_args)
        print(f" [Tool Result] {observation}")
        messages.append(ai_message)
        messages.append(ToolMessage(content=str(observation), tool_call_id=tool_call_id))


if __name__ == "__main__":
    run_agent("What will be the price of laptop for gold subscription")
