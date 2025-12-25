import json
import subprocess
import os

from dotenv import load_dotenv

# Model ID can be obtained here: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
# refer to optimal prompt format from LLM ie for llama: https://www.llama.com/docs/model-cards-and-prompt-formats/meta-llama-3/
MODELS = {
    "deepseek": { "model_id": "us.deepseek.r1-v1:0", "prompt_format": "<｜begin_of_sentence｜><｜User｜>{user_prompt}<｜Assistant｜>" },
    "llama": { "model_id": "us.llama3.r1-v1:0", "prompt_format": "<｜begin_of_text｜><｜User｜>{user_prompt}<｜Assistant｜>" },
    "mistral": { "model_id": "us.mistral.r1-v1:0", "prompt_format": "<s>[INST] ... [/INST]" },
    "claude": { "model_id": "us.claude.r1-v1:0", "prompt_format": "\n\nHuman: ... \n\nAssistant:" }
}

def main():
    load_dotenv()

    # NOTE: Select a model. 
    model_id = MODELS["deepseek"]["model_id"]
    prompt_format = MODELS["deepseek"]["prompt_format"]
    
    # Prompt with DeepSeek template
    user_prompt = "Explain what Amazon Bedrock is in one sentence."
    formatted_prompt = prompt_format.replace("{user_prompt}", user_prompt)
    
    payload = {
        "prompt": formatted_prompt,
        "max_tokens": 1024,             # This limits the length of the answer. A token is roughly 0.75 words. 
        "temperature": 0.7,             # This controls creativity or randomness of the response. Lower values make the answer more deterministic.
        "top_p": 0.9                    # "Nucleus Sampling", this controls the diversity of the answer. Lower values make the answer more focused.
    }
    
    input_file = "input.json"
    output_file = "output.json"
    
    try:
        with open(input_file, "w") as f:
            json.dump(payload, f)
            
        print(f"\nInvoking model: {model_id} (via AWS CLI)")
        print(f"Prompt: {user_prompt}\n")

        cmd = [
            "aws", "bedrock-runtime", "invoke-model",
            "--model-id", model_id,
            "--body", f"fileb://{input_file}",
            output_file
        ]

        subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                response_body = json.load(f)
            
            if 'choices' in response_body:
                print("Response:")
                print(response_body['choices'][0]['text'])
            elif 'outputs' in response_body:
                print("Response:")
                print(response_body['outputs'][0]['text'])
            elif 'generation' in response_body:
                print("Response:")
                print(response_body['generation'])
            else:
                print("Full Response Body:", json.dumps(response_body, indent=2))
        else:
            print("Error: Output file not found after execution.")

    except subprocess.CalledProcessError as e:
        print(f"AWS CLI Error:\n{e.stderr}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

if __name__ == "__main__":
    main()
