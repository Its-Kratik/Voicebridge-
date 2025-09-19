import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
from config.settings import INDICTRANS2_MODEL_NAME, INDICTRANS2_LOCAL_PATH

class TranslationModel:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the translation model from local path or download if not exists"""
        try:
            # Try to load from local path first
            if os.path.exists(INDICTRANS2_LOCAL_PATH):
                print("Loading model from local storage...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    INDICTRANS2_LOCAL_PATH, 
                    trust_remote_code=True
                )
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    INDICTRANS2_LOCAL_PATH, 
                    trust_remote_code=True
                )
            else:
                # Download from Hugging Face
                print("Downloading model from Hugging Face...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    INDICTRANS2_MODEL_NAME, 
                    trust_remote_code=True
                )
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    INDICTRANS2_MODEL_NAME, 
                    trust_remote_code=True
                )
                
                # Save locally for future use
                os.makedirs(INDICTRANS2_LOCAL_PATH, exist_ok=True)
                self.tokenizer.save_pretrained(INDICTRANS2_LOCAL_PATH)
                self.model.save_pretrained(INDICTRANS2_LOCAL_PATH)
            
            # Move model to CPU and set to evaluation mode
            self.model = self.model.to("cpu")
            self.model.eval()
            print("Translation model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading translation model: {e}")
            raise
    
    def translate(self, texts, src_lang, tgt_lang):
        """Translate text from source language to target language"""
        outputs = []
        for text in texts:
            try:
                formatted_input = f"{src_lang} {tgt_lang} {text.strip()}"
                inputs = self.tokenizer(
                    formatted_input, 
                    return_tensors="pt", 
                    truncation=True
                ).to("cpu")
                
                with torch.no_grad():
                    output = self.model.generate(
                        input_ids=inputs.input_ids,
                        attention_mask=inputs.attention_mask,
                        max_length=256,
                        num_beams=1,
                        do_sample=False,
                        use_cache=False
                    )
                
                decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
                outputs.append(decoded)
            except Exception as e:
                print(f"Error translating text: {text}, Error: {e}")
                outputs.append("Translation failed")
        
        return outputs

# Create a global instance
translation_model = TranslationModel()
