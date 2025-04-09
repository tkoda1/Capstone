from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load local LLM (first time will download ~5GB)
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="auto"
)

def generate_recommendation(pattern_summary):
    prompt = f"""### Instruction:
You are a helpful healthcare assistant AI. A user has trouble taking their medication on schedule. Based on the pattern below, give a friendly summary and specific suggestions for how they can improve their medication routine.

### User Pattern:
{pattern_summary}

### Response:"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=300, do_sample=True, temperature=0.7)
    result = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract only the AI's response
    return result.split("### Response:")[-1].strip()

if __name__ == "__main__":
    # Example pattern summary from rule-based or ML logic
    summary = """
User missed 3 doses this week:
- Monday morning (Lisinopril)
- Friday evening (Metformin)
- Sunday evening (Metformin)

Most missed doses happen during the transition from or into weekends.
"""

    print("\n🧠 Personalized AI Feedback:\n")
    feedback = generate_recommendation(summary)
    print(feedback)
