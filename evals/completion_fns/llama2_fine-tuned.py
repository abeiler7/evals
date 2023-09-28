from evals.api import CompletionFn, CompletionResult
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import time

class LLaMA2FineTunedCompletionResult(CompletionResult):
    def __init__(self, response) -> None:
        self.response = response

    def get_completions(self) -> list[str]:
        return [self.response.strip()]


class LLaMA2FineTunedCompletionFn(CompletionFn):
    def __init__(self, model_id: str, base_model:str, **kwargs) -> None:
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map={"":torch.cuda.current_device()})
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)

        self.model.eval()

    def __call__(self, prompt, **kwargs) -> LLaMA2FineTunedCompletionResult:

        # prompt_template=f'''[INST] <<SYS>>
        # You are a helpful, respectful and honest math tutor. You are to respond the question with only the numeric answer.
        # <</SYS>>
        # {prompt}[/INST]

        # '''

        #pipe = pipeline(
        #    "text-generation",
        #    model=self.model,
        #    tokenizer=self.tokenizer,
        #    max_new_tokens=512,
        #    temperature=0.7,
        #    top_p=0.95,
        #    repetition_penalty=1.15,
            #device=torch.cuda.current_device(),
        #)
        #response = pipe(prompt)

        with torch.no_grad():
            input_ids = self.tokenizer(prompt, return_tensors='pt').to("cuda")
            #start = time.perf_counter()
            output = self.model.generate(**input_ids, max_new_tokens=512)
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            #e2e_inference_time = (time.perf_counter()-start)*1000
            #print(f"the inference time is {e2e_inference_time} ms")

        return LLaMA2FineTunedCompletionResult(response)
        # prompt = CompletionPrompt(prompt).to_formatted_prompt()
        # response = self.llm_math.run(prompt)
        # # The LangChain response comes with `Answer: ` ahead of this, let's strip it out
        # response = response.strip("Answer:").strip()
        # record_sampling(prompt=prompt, sampled=response)
        # return LangChainCompletionResult(response)
