import boto3
import json
from config import BedrockConfig

region = BedrockConfig.REGION
bedrockAgentClient = boto3.client(service_name="bedrock-agent")
bedrockRunClient = boto3.client("bedrock-runtime", region_name=region)

MODEL_ID = BedrockConfig.MODELS["claude"]
PROMPT_ID = BedrockConfig.EVALUATE_PROMPT["promptId"]
PROMPT_VERSION = BedrockConfig.EVALUATE_PROMPT["promptVersion"]


def fetch_prompt_template():

    response = bedrockAgentClient.get_prompt(
        promptIdentifier=PROMPT_ID, promptVersion=PROMPT_VERSION
    )

    # Correct printing
    print(json.dumps(response["variants"][0], indent=2))
    print(
        "system:",
        response["variants"][0]["templateConfiguration"]["text"].get("system", ""),
    )

    template = response["variants"][0]["templateConfiguration"]["text"]["text"]

    system_instruction = response["variants"][0]["templateConfiguration"]["text"].get(
        "system", ""
    )

    return system_instruction, template


# Step 1: Generate model output
def generate_output(user_prompt, system_instruction):
    response = bedrockRunClient.converse(
        modelId=MODEL_ID,
        system=[{"text": system_instruction}],
        messages=[{"role": "user", "content": [{"text": user_prompt}]}],
        inferenceConfig={"temperature": 0.7, "topP": 0.9, "maxTokens": 500},
    )
    return response["output"]["message"]["content"][0]["text"]


# Step 2: Call Bedrock Prompt Management evaluation prompt
def evaluate_prompt(prompt_input, prompt_output):
    system_instruction, template = fetch_prompt_template()

    final_prompt = template.replace("{{input}}", prompt_input)
    final_prompt = final_prompt.replace("{{output}}", prompt_output)

    converse_params = {
        "modelId": MODEL_ID,
        "messages": [{"role": "user", "content": [{"text": final_prompt}]}],
        "inferenceConfig": {"temperature": 0, "maxTokens": 1000},
    }
    # Only include system if not empty
    if system_instruction and system_instruction.strip():
        converse_params["system"] = [{"text": system_instruction}]
    response = bedrockRunClient.converse(**converse_params)
    result = response["output"]["message"]["content"][0]["text"]
    return json.loads(result)


# Step 3: Compare evaluation results
def compare_evaluations(eval1, eval2):
    score1 = eval1["answer-score"] + eval1["prompt-score"]
    score2 = eval2["answer-score"] + eval2["prompt-score"]
    print("\nPrompt 1 total score:", score1)
    print("Prompt 2 total score:", score2)
    if score1 > score2:
        return "Prompt 1 is better", eval1
    elif score2 > score1:
        return "Prompt 2 is better", eval2
    else:
        return "Both prompts are equal", None


# fetch_prompt_template()
# exit()

system_instruction = "You are a mathematics professor. Answer the questions related to mathematics only. If question is irrelevant, reply with 'I can only answer questions related to mathematics and this question is irrelevant'"

prompt1 = "Explain Pythagoras theorem"
prompt2 = """
    Explain the Pythagoras theorem.
    Your explanation must include:
    1. Clear definition of the theorem
    2. Mathematical formula with symbols
    3. Step-by-step explanation of why it works
    4. A solved numerical example
    5. Real-world application

    Ensure the explanation is structured, precise, and easy to understand.
    """

print("\nGenerating outputs...")

output1 = generate_output(prompt1, system_instruction)
output2 = generate_output(prompt2, system_instruction)

print("\nEvaluating prompt 1...")
eval1 = evaluate_prompt(prompt1, output1)
print("\nEvaluating prompt 2...")
eval2 = evaluate_prompt(prompt2, output2)

result, best_eval = compare_evaluations(eval1, eval2)
print("\nFINAL RESULT:")
print(result)

if best_eval:
    print("\nBest evaluation details:")
    print(json.dumps(best_eval, indent=2))
