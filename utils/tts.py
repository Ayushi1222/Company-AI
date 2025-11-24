import logging
from typing import Optional
import streamlit as st

logger = logging.getLogger(__name__)


class TextToSpeech:
    def __init__(self, prefer_online: bool = True):
        self.prefer_online = prefer_online
        self.gtts_available = False
        self.pyttsx3_available = False
        
        try:
            import gtts
            self.gtts_available = True
            logger.info("gTTS available")
        except ImportError:
            logger.warning("gTTS not available")
        
        try:
            import pyttsx3
            self.pyttsx3_available = True
            logger.info("pyttsx3 available")
        except ImportError:
            logger.warning("pyttsx3 not available")
    
    def speak(self, text: str, language: str = 'en') -> Optional[str]:
        if not text or not text.strip():
            return None
        
        if self.prefer_online and self.gtts_available:
            return self._speak_gtts(text, language)
        
        if self.pyttsx3_available:
            return self._speak_pyttsx3(text)
        
        if self.gtts_available:
            return self._speak_gtts(text, language)
        
        logger.error("No TTS backend available")
        return None
    
    def _speak_gtts(self, text: str, language: str) -> Optional[str]:
        try:
            from gtts import gTTS
            import tempfile
            import os
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(temp_path)
            
            logger.info(f"Generated TTS audio: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"gTTS failed: {str(e)}")
            return None
    
    def _speak_pyttsx3(self, text: str) -> Optional[str]:
        try:
            import pyttsx3
            import tempfile
            
            engine = pyttsx3.init()
            
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_path = temp_file.name
            temp_file.close()
            
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            logger.info(f"Generated TTS audio: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"pyttsx3 failed: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return self.gtts_available or self.pyttsx3_available


def create_tts_player(text: str, key: str = "tts") -> bool:
    try:
        tts = TextToSpeech()
        
        if not tts.is_available():
            st.info("🔇 Text-to-speech is not available. Install gtts or pyttsx3 to enable.")
            return False
        
        audio_path = tts.speak(text)
        
        if audio_path:
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
            
            import os
            try:
                os.unlink(audio_path)
            except:
                pass
            
            return True
        else:
            st.warning("⚠️ Could not generate audio")
            return False
            
    except Exception as e:
        logger.error(f"TTS player creation failed: {str(e)}")
        return False


def add_tts_button(text: str, button_text: str = "🔊 Listen", key: str = "tts_btn"):
    if st.button(button_text, key=key):
        with st.spinner("Generating audio..."):
            create_tts_player(text, key=f"{key}_player")
