import boto3
import json

region = 'us-east-1'
bedrockClient = boto3.client(service_name="bedrock-runtime", region_name=region)

def converse_claudeSonnet_text(system_instruction, prompt, model_id='anthropic.claude-3-5-sonnet-20240620-v1:0', region='us-east-1'):
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
            }
        )

        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        print(f"Error in converse api call: {e}")
        return None

def conversestream_claudeSonnet_text_guardrail(system_instruction, prompt, model_id='anthropic.claude-3-5-sonnet-20240620-v1:0', region='us-east-1'):
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
                "guardrailIdentifier": "gr-abc123xyz",
                "guardrailVersion": "1"
            },
            additionalModelRequestFields={
                "guardrailConfig": {
                    "trace": "ENABLED"
                }
            }
        )

        # return response["output"]["message"]["content"][0]["text"]
        full_response = ""

        for event in response["stream"]:
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

def invoke_claudeSonnet_text(system_instr, prompt, model_id='anthropic.claude-3-5-sonnet-20240620-v1:0', region='us-east-1'):
    """
    Invokes an Anthropic claude to generate a response.
    """
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_instr,
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        response = bedrockClient.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        result = json.loads(response["body"].read())

        generated_text = result["content"][0]["text"]
        return generated_text
    except Exception as e:
        print(f"Error invoking model: {e}")
        return None

#invoke call
# system_instruction = '''You are an environmental advisor and sustainability expert. Provide accurate, science-based guidance on environmental issues and sustainable practices.'''
# question = "How to get peace?"
# response = invoke_claudeSonnet_text(system_instruction, question)
# print(f"Q: {question}\nR: {response}")

system_instruction='''
            You are a highly experienced mathematics professor with deep expertise in teaching and problem solving.
            Your task is to explain mathematical problems in a clear, structured, and step-by-step manner.
            Follow these guideliness:
            1. Focus ONLY on mathematics. Do NOT include unrelated subjects, stories, or analogies outside mathematics unless absolutely necessary to clarify the math.
            2. Always explain the solution step-by-step in logical order.
        '''
response = converse_claudeSonnet_text(system_instruction,'Explain pythagoras theorem')
print("Response: ", response)

# system_instruction='''
#             You are a highly experienced mathematics professor with deep expertise in teaching and problem solving.
#             Your task is to explain mathematical problems in a clear, structured, and step-by-step manner.
#             Follow these guideliness:
#             1. Focus ONLY on mathematics. Do NOT include unrelated subjects, stories, or analogies outside mathematics unless absolutely necessary to clarify the math.
#             2. Always explain the solution step-by-step in logical order.
#         '''
# conversestream_claudeSonnet_text(system_instruction,'Explain pythagoras theorem')

