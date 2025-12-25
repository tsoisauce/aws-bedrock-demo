# AWS Bedrock Demo

This is a simple demo of how to use AWS Bedrock to invoke a model.

## Setup

Easiest way to setup is to use the AWS CLI and UV for dependencies and environment management.

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [UV](https://github.com/astral-sh/uv)

AWS CLI will allow you to use the `aws` command to invoke the model without dealing with credentials directly in the code.

- Create a .env file with the following variables:

```
AWS_PROFILE=your_aws_profile
```

install dependencies:

```
uv sync
```

run the script:

```
uv run main.py
```

## Understanding the prompt

The prompt is formatted based on the model's requirements. For example, the DeepSeek model requires a specific format for the prompt. You can find the optimal prompt format from the model's documentation.

``` python
payload = {
    "prompt": formatted_prompt,
    "max_tokens": 1024,
    "temperature": 0.7, 
    "top_p": 0.9                   
}
```

- `prompt`: This is the actual input text you send to the model. It contains your question ("Explain what Amazon Bedrock is...") wrapped in the special formatting (<｜User｜>...) so the model understands the context.
- `max_tokens`: This limits the length of the answer. A token is roughly 0.75 words. Setting this to 1024 means the model will stop generating text once it produces approx. 750 words, preventing it from rambling endlessly or using up your budget.
- `temperature`: This controls the creativity or randomness of the response.
    - Low (0.0 - 0.3): Very predictable, factual, and consistent. Good  for code or math.
    - Medium (0.5 - 0.7): Balanced. Good for general explanations and writing.
    - High (0.8 - 1.0+): More creative, diverse, but can be less coherent or hallucinate.
- `top_p`: Also known as "Nucleus Sampling", this controls the diversity of vocabulary.
    - It tells the model: "Only consider the top X% most likely next words that add up to this probability."
    - 0.9 means it considers the top 90% of likely words, filtering out the very weird/unlikely text.
    - Similar to temperature, but works by chopping off the "tail" of unlikely options rather than scaling probabilities.


## Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [UV](https://github.com/astral-sh/uv)
- [AWS Bedrock Model](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- Python 3.12+
- [dotenv](https://github.com/theskumar/python-dotenv)# aws-bedrock-demo
