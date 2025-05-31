import ollama
import cv2
import os
import tempfile
import torch
import soundfile as sf
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from app.utils.logger import logger_msg

class OllamaClient:
    #------------------Text Embeddings------------------
    @staticmethod
    def get_text_embeddings(text):
        logger_msg("Generating text embeddings.", "info")
        response = ollama.embeddings(model='nomic-embed-text', prompt=text)
        return response['embedding']
    
    #------------------Image Embeddings------------------
    @staticmethod
    def describe_image(image_path):
        logger_msg(f"Describing image: {image_path}", "info")
        with open(image_path, 'rb') as image_file:
            response = ollama.generate(
                model='llava:7b',
                prompt='Describe the contents of this image.',
                images=[image_file.read()]
            )
        return response['response']
    
    #------------------Audio Embeddings------------------
    @staticmethod
    def transcribe_audio(audio_path):
        logger_msg(f"Transcribing audio: {audio_path}", "info")

        # Load the audio file
        speech, sampling_rate = sf.read(audio_path)

        # Load the processor and model
        processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")
        model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")

        # Prepare the inputs
        inputs = processor(speech, sampling_rate=sampling_rate, return_tensors="pt")

        # Generate transcription
        with torch.no_grad():
            generated_ids = model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])

        # Decode the transcription
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return transcription
    
    #------------------Text Summarization------------------
    @staticmethod
    def summarize_text(text):
        logger_msg("Summarizing text.", "info")
        response = ollama.generate(
            model='llama3.2:3b',
            prompt=f"Summarize the following text:\n\n{text}"
        )
        return response['response']
    
    #------------------Video Summarization------------------
    @staticmethod
    def describe_video(video_path, frame_interval=5):
        logger_msg(f"Describing video: {video_path}", "info")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger_msg("Cannot open video file.", "error")
            return "Error: Cannot open video file."
        
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        interval_frames = int(frame_rate * frame_interval)

        descriptions = []
        frame_count = 0
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % interval_frames == 0:
                    frame_file = os.path.join(tmpdirname, f'frame_{frame_count}.jpg')
                    cv2.imwrite(frame_file, frame)
                    description = OllamaClient.describe_image(frame_file)
                    descriptions.append(description)
                
                frame_count += 1
        
        cap.release()

        # Combine descriptions into a summary
        combined_descriptions = " ".join(descriptions)
        video_summary = OllamaClient.summarize_text(combined_descriptions)

        return video_summary