# dialer/consumers.py
import json
import base64
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from groq import AsyncGroq
from django.conf import settings

# Initialize Groq (LLM)
groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class AIAudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.call_history = [
            {"role": "system", "content": "You are a short, polite AI caller for a marketing campaign. If they say yes, you say excellent and we will book an appointment. Keep responses under 2 sentences."}
        ]
        # Here you would typically initialize the Deepgram connection
        # self.deepgram_socket = await connect_to_deepgram()
        print("Call connected. WebSocket open.")

    async def disconnect(self, close_code):
        print("Call ended.")
        # Here you would save the final self.call_history transcript to the CallLog model

    async def receive(self, text_data=None, bytes_data=None):
        """
        The SIP provider sends audio chunks here.
        """
        if text_data:
            data = json.loads(text_data)
            
            # 1. Receive audio from phone
            if data['event'] == 'media':
                raw_audio = data['media']['payload'] # Base64 encoded audio chunk
                
                # 2. Send to Deepgram for STT
                # await self.deepgram_socket.send(raw_audio)
                
                # ... (Deepgram returns text asynchronously) ...
                # For demonstration, let's assume Deepgram returned: "Yes I am interested"
                user_text = "Yes I am interested"
                await self.process_llm_and_speak(user_text)

    async def process_llm_and_speak(self, user_text):
        """
        Takes transcribed text, gets AI response, converts to audio, sends to phone.
        """
        self.call_history.append({"role": "user", "content": user_text})
        
        # 3. Get AI Response from Groq (Llama 3)
        chat_completion = await groq_client.chat.completions.create(
            messages=self.call_history,
            model="llama3-8b-8192",
        )
        ai_response = chat_completion.choices[0].message.content
        self.call_history.append({"role": "assistant", "content": ai_response})
        
        # 4. Convert AI text to Audio (Google Cloud TTS)
        # audio_content = await synthesize_speech_google(ai_response)
        audio_base64 = "base64_encoded_audio_bytes_from_google" 
        
        # 5. Stream audio back to the SIP Provider to play on the phone
        payload = {
            "event": "media",
            "media": {
                "payload": audio_base64
            }
        }
        await self.send(text_data=json.dumps(payload))