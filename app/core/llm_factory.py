from app.core.config import settings, LLMProvider

class LLMFactory: 
    @staticmethod
    def get_provider(provider: str = None, temperature: float = None, model: str = None):
        """
        Initialize and return appropriate LLM based on provider
        """
        target_provider = provider or settings.DEFAULT_PROVIDER
        target_temp = temperature if temperature is not None else settings.TEMPERATURE
        target_model = model if model is not None else settings.DEFAULT_MODEL

        match target_provider:
            case "gemini" | "google" | LLMProvider.GOOGLE:
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model = target_model,
                    api_key = settings.GOOGLE_API_KEY,
                    temperature = target_temp
                )
            case "openai":
                from langchain_openai import ChatOpenAI
                return ChatOpenAI( 
                    model = target_model,
                    api_key = settings.OPENAI_API_KEY,
                    temperature = target_temp
                )
            case "groq" | LLMProvider.GROQ:
                from langchain_groq import ChatGroq
                return ChatGroq(
                    model_name = target_model, # Groq dùng model_name hoặc model
                    api_key = settings.GROQ_API_KEY,
                    temperature = target_temp
                )
            case _:
                raise ValueError("Invalid Provider")

if __name__ == "__main__": 
    print("--- Testing Default Model ---")
    try:
        model = LLMFactory.get_provider()
        print(f"✅ Success! Type: {type(model)}")
        print(f"Model Name: {model.model}") 
    except Exception as e:
        print(f"❌ Failed: {e}")

    print("\n--- Testing OpenAI Model ---")
    try:
        # Lưu ý: Nếu chưa có OPENAI_API_KEY trong .env thì bước này có thể báo lỗi Auth
        model_oa = LLMFactory.get_provider(provider="openai", model="gpt-4o-mini")
        print(f"✅ Success! Type: {type(model_oa)}")
    except Exception as e:
        print(f"❌ Failed (Expected if no key): {e}")
