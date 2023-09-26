from evals.api import CompletionFn, CompletionResult
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class LLaMA2FineTunedCompletionResult(CompletionResult):
    def __init__(self, response) -> None:
        self.response = response

    def get_completions(self) -> list[str]:
        return [self.response.strip()]


class LLaMA2FineTunedCompletionFn(CompletionFn):
    def __init__(self, model_id: str, base_model:str, **kwargs) -> None:
        # llm = OpenAI(temperature=0)
        # self.llm_math = LLMMathChain(llm=llm)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, load_in_8bit=True, torch_dtype=torch.bfloat16, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)

    def __call__(self, prompt, **kwargs) -> LLaMA2FineTunedCompletionResult:

        # prompt_template=f'''[INST] <<SYS>>
        # You are a helpful, respectful and honest math tutor. You are to respond the question with only the numeric answer.
        # <</SYS>>
        # {prompt}[/INST]

        # '''

        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.15
        )
        response = pipe(prompt)
        return LLaMA2FineTunedCompletionResult(response[0]['generated_text'])
        # prompt = CompletionPrompt(prompt).to_formatted_prompt()
        # response = self.llm_math.run(prompt)
        # # The LangChain response comes with `Answer: ` ahead of this, let's strip it out
        # response = response.strip("Answer:").strip()
        # record_sampling(prompt=prompt, sampled=response)
        # return LangChainCompletionResult(response)