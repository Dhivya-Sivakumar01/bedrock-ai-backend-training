import os 
from bedrock_agentcore.memory import MemoryClient

memory_client = MemoryClient(region_name="us-east-1")
basic_memory = memory_client.create_memory(
    name="EmployeeManagementMemory",
    description="Basic memory for testing short-term functionality"
)

memory_id = basic_memory.get('id')
print(f"Created memory with ID: {memory_id}")
os.environ['AGENTCORE_MEMORY_ID'] = memory_id