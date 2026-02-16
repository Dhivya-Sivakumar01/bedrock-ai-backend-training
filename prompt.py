import boto3
import json

region = 'us-east-1'
bedrockClient = boto3.client(service_name="bedrock-runtime", region_name=region)

def invoke_claudeSonnet_text( system_instr, prompt, model_id='anthropic.claude-3-5-sonnet-20240620-v1:0', region='us-east-1'):
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


# Role
# Task (e.g., instructions, requirements, examples)
# Context (e.g., RAG)
system_instr = '''You are an animal expert.
    You need to answer questions related to animals only. If the questions are not related to animals, reply with 'I can answer only questions related to animals and this is irrelevant question.'''

# Input (e.g., question)
# Output indicator (e.g., format)

#zero-shot prompting
zero_shot = '''
    Provide me domestic animal sounds
'''
#Few-shot prompting
few_shot = '''
    You are an animal expert.
    You need to answer questions related to animals only. If the questions are not related to animals, reply with 'I can answer only questions related to animals and this is irrelevant question.'
    Provide me domestic animal sounds
    Dog: bow bow
    Cat: meow meow
'''

#Chain-of-thought prompting
chain_of_thought = '''
    You are an animal expert.
    You need to answer questions related to animals only. If the questions are not related to animals, reply with 'I can answer only questions related to animals and this is irrelevant question.'

    Step 1: Identify whether the question is related to animals.
    Step 2: List out common domestic animal
    Step 3: Think about the typical sound each animal makes.
    Step 4: Provide the final answer along with animal names clearly.

    Provide me domestic animal sounds.
'''

#Structured output prompting
structured_output_strict = '''
    You are an animal expert.
    You need to answer questions related to animals only. If the questions are not related to animals, reply with 'I can answer only questions related to animals and this is irrelevant question.'
    You must return ONLY valid JSON with provided schema and not to include explanations.
    Do not include markdown.
    Do not include text outside JSON.

    Schema:
    {
        "animals": [
            {
            "name": "string",
            "sound": "string"
            }
        ]
    }
'''

response = invoke_claudeSonnet_text(system_instr,structured_output_strict)
print("response: ", response)
