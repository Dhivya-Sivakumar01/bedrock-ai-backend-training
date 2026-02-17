import boto3
from config import BedrockConfig

region = BedrockConfig.REGION
bedrockClient = boto3.client(service_name="bedrock-runtime", region_name=region)
MODEL_ID = BedrockConfig.MODELS["claude"]

def converse_claudeSonnet_guardrail(system_instruction, prompt, model_id=MODEL_ID):
    """
    Using Converse an Anthropic claude text model to generate a response.
    """
    try:
        response = bedrockClient.converse(
            modelId=model_id,
            system=[{"text": system_instruction}],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "temperature": 1,
                "maxTokens": 512,
                "topP": 0.9
            },
            guardrailConfig={
                "guardrailIdentifier": "tca33k9ab4md",
                "guardrailVersion": "1",
                "trace": "enabled"
            }
        )
        if(response["stopReason"]=="guardrail_intervened"):
            print("Guardrail interrupt")

        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        print(f"Error in converse api call: {e}")
        return None

def conversestream_claudeSonnet_text_guardrail(system_instruction, prompt, model_id=MODEL_ID):
    """
    Using Converse Stream api an Anthropic claude text model to generate a streaming response.
    """
    try:
        response = bedrockClient.converse_stream(
            modelId=model_id,
            system=[{"text": system_instruction}],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "temperature": 1,
                "maxTokens": 512,
                "topP": 0.9
            },
            guardrailConfig={
                "guardrailIdentifier": "tca33k9ab4md",
                "guardrailVersion": "1",
                "trace": "enabled"
            }
        )

        # return response["output"]["message"]["content"][0]["text"]
        full_response = ""

        for event in response["stream"]:
            # 🛑 Check stop reason
            if "messageStop" in event:
                stop_reason = event["messageStop"].get("stopReason")
                if stop_reason == "GUARDRAIL_INTERVENED":
                    print("🚨 Guardrail blocked before model execution")
                    return "Blocked Content"
            # Text chunk event
            if "contentBlockDelta" in event:
                delta = event["contentBlockDelta"]
                if "delta" in delta and "text" in delta["delta"]:
                    text_chunk = delta["delta"]["text"]
                    print(text_chunk, end="", flush=True)  # streaming output
                    full_response += text_chunk

        return full_response
    except Exception as e:
        print(f"Error in converse api call: {e}")
        return None

# system_instruction='''
#             You are a suggestion tool. Answer the question raised by users
#         '''
# response = converse_claudeSonnet_guardrail(system_instruction,'how to kill a person')
# print("Response: ", response)

system_instruction='''
            You are a highly experienced mathematics professor with deep expertise in teaching and problem solving.
            Your task is to explain mathematical problems in a clear, structured, and step-by-step manner.
            Follow these guideliness:
            1. Focus ONLY on mathematics. Do NOT include unrelated subjects, stories, or analogies outside mathematics unless absolutely necessary to clarify the math.
            2. Always explain the solution step-by-step in logical order.
        '''
response = conversestream_claudeSonnet_text_guardrail(system_instruction,'Explain pythagoras theorem')
# print("Response: ", response)

# system_instruction='''
#             You are a suggestion tool. Answer the question raised by users
#         '''
# response = conversestream_claudeSonnet_text_guardrail(system_instruction,'how to kill a person')
# print("Response: ", response)