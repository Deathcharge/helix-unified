"""
AI Image Generation Integration
Supports DALL-E, Stable Diffusion, and other image generation APIs
"""
import os
import asyncio
import logging
from typing import Dict, Any, Optional, List
import requests
import base64
from io import BytesIO
from datetime import datetime
import openai

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Multi-provider AI image generation system"""
    
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.stability_key = os.getenv('STABILITY_API_KEY')
        self.replicate_key = os.getenv('REPLICATE_API_KEY')
        
        self.providers = {}
        self._initialize_providers()
        
        # Generation history
        self.generation_history = []
        self.max_history = 100
    
    def _initialize_providers(self):
        """Initialize available image generation providers"""
        
        # DALL-E (OpenAI)
        if self.openai_key:
            try:
                openai.api_key = self.openai_key
                self.providers['dalle'] = DALLEGenerator(self.openai_key)
                logger.info("DALL-E image generator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize DALL-E: {e}")
        
        # Stable Diffusion (Stability AI)
        if self.stability_key:
            try:
                self.providers['stable_diffusion'] = StableDiffusionGenerator(self.stability_key)
                logger.info("Stable Diffusion generator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Stable Diffusion: {e}")
        
        # Replicate (Multiple models)
        if self.replicate_key:
            try:
                self.providers['replicate'] = ReplicateGenerator(self.replicate_key)
                logger.info("Replicate generator initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Replicate: {e}")
    
    async def generate_image(
        self,
        prompt: str,
        provider: str = 'dalle',
        size: str = '1024x1024',
        style: Optional[str] = None,
        quality: str = 'standard',
        n: int = 1
    ) -> Dict[str, Any]:
        """Generate image using specified provider"""
        
        if provider not in self.providers:
            available = list(self.providers.keys())
            return {
                'success': False,
                'error': f'Provider {provider} not available. Available: {available}',
                'images': []
            }
        
        try:
            result = await self.providers[provider].generate(
                prompt=prompt,
                size=size,
                style=style,
                quality=quality,
                n=n
            )
            
            # Add to history
            if result['success']:
                self.generation_history.append({
                    'prompt': prompt,
                    'provider': provider,
                    'timestamp': datetime.utcnow().isoformat(),
                    'image_count': len(result['images'])
                })
                
                # Trim history
                if len(self.generation_history) > self.max_history:
                    self.generation_history = self.generation_history[-self.max_history:]
            
            logger.info(f"Image generation via {provider}: {result['success']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Image generation failed with {provider}: {e}")
            return {
                'success': False,
                'error': str(e),
                'images': []
            }
    
    def get_available_providers(self) -> List[str]:
        """Get list of available image generation providers"""
        return list(self.providers.keys())
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get image generation statistics"""
        
        if not self.generation_history:
            return {
                'total_generations': 0,
                'providers_used': [],
                'average_images_per_generation': 0
            }
        
        providers_used = list(set(h['provider'] for h in self.generation_history))
        total_images = sum(h['image_count'] for h in self.generation_history)
        
        return {
            'total_generations': len(self.generation_history),
            'providers_used': providers_used,
            'average_images_per_generation': total_images / len(self.generation_history),
            'recent_prompts': [h['prompt'] for h in self.generation_history[-5:]]
        }

class DALLEGenerator:
    """DALL-E image generation provider"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
    
    async def generate(
        self,
        prompt: str,
        size: str = '1024x1024',
        style: Optional[str] = None,
        quality: str = 'standard',
        n: int = 1
    ) -> Dict[str, Any]:
        """Generate images using DALL-E"""
        
        try:
            # DALL-E 3 parameters
            params = {
                'model': 'dall-e-3',
                'prompt': prompt,
                'size': size,
                'quality': quality,
                'n': 1  # DALL-E 3 only supports n=1
            }
            
            if style:
                params['style'] = style
            
            response = await asyncio.to_thread(
                openai.images.generate,
                **params
            )
            
            images = []
            for image_data in response.data:
                images.append({
                    'url': image_data.url,
                    'revised_prompt': getattr(image_data, 'revised_prompt', prompt)
                })
            
            return {
                'success': True,
                'images': images,
                'provider': 'dalle',
                'model': 'dall-e-3'
            }
            
        except Exception as e:
            logger.error(f"DALL-E generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'images': []
            }

class StableDiffusionGenerator:
    """Stable Diffusion image generation provider"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v1/generation"
    
    async def generate(
        self,
        prompt: str,
        size: str = '1024x1024',
        style: Optional[str] = None,
        quality: str = 'standard',
        n: int = 1
    ) -> Dict[str, Any]:
        """Generate images using Stable Diffusion"""
        
        try:
            # Parse size
            width, height = map(int, size.split('x'))
            
            # Prepare request
            url = f"{self.base_url}/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'text_prompts': [{'text': prompt}],
                'cfg_scale': 7,
                'height': height,
                'width': width,
                'samples': n,
                'steps': 30
            }
            
            response = await asyncio.to_thread(
                requests.post,
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                images = []
                for artifact in data.get('artifacts', []):
                    if artifact.get('base64'):
                        images.append({
                            'base64': artifact['base64'],
                            'seed': artifact.get('seed')
                        })
                
                return {
                    'success': True,
                    'images': images,
                    'provider': 'stable_diffusion',
                    'model': 'sdxl-1.0'
                }
            else:
                return {
                    'success': False,
                    'error': f'API error: {response.status_code} - {response.text}',
                    'images': []
                }
                
        except Exception as e:
            logger.error(f"Stable Diffusion generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'images': []
            }

class ReplicateGenerator:
    """Replicate image generation provider (supports multiple models)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.replicate.com/v1/predictions"
    
    async def generate(
        self,
        prompt: str,
        size: str = '1024x1024',
        style: Optional[str] = None,
        quality: str = 'standard',
        n: int = 1
    ) -> Dict[str, Any]:
        """Generate images using Replicate"""
        
        try:
            # Use SDXL model on Replicate
            model_version = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
            
            headers = {
                'Authorization': f'Token {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'version': model_version,
                'input': {
                    'prompt': prompt,
                    'num_outputs': n
                }
            }
            
            # Create prediction
            response = await asyncio.to_thread(
                requests.post,
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction['id']
                
                # Poll for completion
                max_attempts = 30
                for _ in range(max_attempts):
                    await asyncio.sleep(2)
                    
                    status_response = await asyncio.to_thread(
                        requests.get,
                        f"{self.base_url}/{prediction_id}",
                        headers=headers,
                        timeout=10
                    )
                    
                    if status_response.status_code == 200:
                        result = status_response.json()
                        
                        if result['status'] == 'succeeded':
                            images = []
                            for url in result.get('output', []):
                                images.append({'url': url})
                            
                            return {
                                'success': True,
                                'images': images,
                                'provider': 'replicate',
                                'model': 'sdxl'
                            }
                        elif result['status'] == 'failed':
                            return {
                                'success': False,
                                'error': result.get('error', 'Generation failed'),
                                'images': []
                            }
                
                return {
                    'success': False,
                    'error': 'Generation timeout',
                    'images': []
                }
            else:
                return {
                    'success': False,
                    'error': f'API error: {response.status_code}',
                    'images': []
                }
                
        except Exception as e:
            logger.error(f"Replicate generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'images': []
            }

# Global image generator instance
image_generator = ImageGenerator()