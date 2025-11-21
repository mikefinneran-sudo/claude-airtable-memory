#!/usr/bin/env python3
"""
Fine-tune Llama 3.1:70b on CrewAI training data using Unsloth.
"""

from unsloth import FastLanguageModel
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# Config
MODEL_NAME = "unsloth/Meta-Llama-3.1-70B-bnb-4bit"  # 4-bit quantized
MAX_SEQ_LENGTH = 2048
LOAD_IN_4BIT = True

print("=" * 60)
print("CrewAI Training Academy - Llama 3.1:70b Fine-tuning")
print("=" * 60)

# 1. Load model with 4-bit quantization
print("\n[1/5] Loading Llama 3.1:70b (4-bit)...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,  # Auto-detect
    load_in_4bit=LOAD_IN_4BIT,
)

# 2. Prepare for QLoRA fine-tuning
print("[2/5] Adding LoRA adapters...")
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,  # Optimized to 0
    bias="none",
    use_gradient_checkpointing="unsloth",  # Unsloth's optimized checkpointing
    random_state=3407,
)

# 3. Load training data
print("[3/5] Loading training dataset...")
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")

print(f"  → Training examples: {len(dataset)}")

# Format function
alpaca_prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

def formatting_func(examples):
    instructions = examples["instruction"]
    inputs = examples["input"]
    outputs = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        text = alpaca_prompt.format(instruction, input, output) + tokenizer.eos_token
        texts.append(text)
    return {"text": texts}

dataset = dataset.map(formatting_func, batched=True)

# 4. Training config
print("[4/5] Configuring training...")
training_args = TrainingArguments(
    output_dir="./llama-crewai-finetuned",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=5,
    max_steps=100,  # Start small, increase later
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=3407,
    save_strategy="steps",
    save_steps=25,
)

# 5. Create trainer
print("[5/5] Starting fine-tuning...")
print(f"  → Batch size: {training_args.per_device_train_batch_size}")
print(f"  → Gradient accumulation: {training_args.gradient_accumulation_steps}")
print(f"  → Total steps: {training_args.max_steps}")
print(f"  → Learning rate: {training_args.learning_rate}")
print()

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    dataset_num_proc=2,
    packing=False,  # Can make training 5x faster for short sequences
    args=training_args,
)

# Train!
print("Training started...")
print("=" * 60)
trainer_stats = trainer.train()

# Save model
print("\n" + "=" * 60)
print("Training complete! Saving model...")
model.save_pretrained("llama-crewai-final")
tokenizer.save_pretrained("llama-crewai-final")

print("\n✓ Model saved to: ./llama-crewai-final")
print("✓ Ready to deploy to Ollama!")
print("=" * 60)
