from transformers import pipeline, set_seed
from transformers import GPT2Tokenizer, GPT2Model
# text_generation = pipeline('text-generation', model='gpt2')
# prefix_text = 'Jia molest a girl'
# generated_text= text_generation(prefix_text, max_length=100, do_sample=False)[0]
# print(generated_text['generated_text'])
import random
def select_top_k(predictions, k=10):
    predicted_index = random.choice(
        predictions[0, -1, :].sort(descending=True)[1][:10]).item()
    return predicted_index

import torch
import logging
logging.basicConfig(level=logging.INFO)

# 载入预训练模型的分词器
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# 使用 GPT2Tokenizer 对输入进行编码
text = "Yesterday, a man named Jack said he saw an alien,"
indexed_tokens = tokenizer.encode(text)
tokens_tensor = torch.tensor([indexed_tokens])
tokens_tensor.shape
from transformers import GPT2LMHeadModel

# 读取 GPT-2 预训练模型
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

total_predicted_text = text
n = 10  # 预测过程的循环次数
for _ in range(n):
    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    predicted_index = select_top_k(predictions, k=10)
    predicted_text = tokenizer.decode(indexed_tokens + [predicted_index])
    total_predicted_text += tokenizer.decode(predicted_index)

    if '<|endoftext|>' in total_predicted_text:
        # 如果出现文本结束标志，就结束文本生成
        break

    indexed_tokens += [predicted_index]
    tokens_tensor = torch.tensor([indexed_tokens])

print(total_predicted_text)