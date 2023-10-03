from num2words import num2words

# EXAMPLE OPENAI EVALS JSONL FORMAT
# {"input": [{"role": "system", "content": "Complete the phrase as concisely as possible."}, {"role": "user", "content": "Once upon a "}], "ideal": "time"}
# {"input": [{"role": "system", "content": "Complete the phrase as concisely as possible."}, {"role": "user", "content": "The first US president was "}], "ideal": "George Washington"}
# {"input": [{"role": "system", "content": "Complete the phrase as concisely as possible."}, {"role": "user", "content": "OpenAI was founded in 20"}], "ideal": "15"}

def to_openai_eval_format(input_data: dict) -> list:
    output_data = []
    for ex in input_data["examples"]:
        alpha_rep = num2words(ex["target"])
        formatted_ex = {
            "input": [
                {
                    "role": "user",
                    "content": ex["input"]
                }
            ],
            "ideal": [ex["target"], alpha_rep, alpha_rep.replace("-", " ")]
        }
        output_data.append(formatted_ex)
    
    return output_data
