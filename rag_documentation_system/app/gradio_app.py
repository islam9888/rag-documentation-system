"""
Gradio UI for RAG Documentation System
"""
import gradio as gr
from datetime import datetime
from typing import List, Tuple

from src.indexer import RAGIndexer
from src.query_engine import QueryEngine
from src.config import config
from src.utils import setup_logging

logger = setup_logging(log_level="INFO")


class RAGApp:
    """Gradio application wrapper"""
    
    def __init__(self):
        self.indexer = None
        self.query_engine = None
        self.is_ready = False
        self._initialize()
    
    def _initialize(self):
        """Initialize the RAG system"""
        try:
            logger.info("Initializing RAG system...")
            
            # Setup config
            config.setup()
            
            # Load index
            self.indexer = RAGIndexer()
            index = self.indexer.build_index()
            
            # Create query engine
            self.query_engine = QueryEngine(index)
            
            self.is_ready = True
            logger.info("RAG system ready!")
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            raise
    
    def chat(
        self, 
        message: str, 
        history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Handle chat interaction
        
        Args:
            message: User message
            history: Chat history
            
        Returns:
            Updated history
        """
        if not self.is_ready:
            error_msg = "❌ System not ready. Please check logs."
            history.append((message, error_msg))
            return "", history
        
        if not message.strip():
            return "", history
        
        try:
            # Query with history context
            answer, sources = self.query_engine.query(
                message, 
                use_history=True
            )
            
            # Format response with sources
            response = self.query_engine.format_response(answer, sources)
            
            # Update history
            history.append((message, response))
            
            return "", history
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            error_msg = f"❌ Error: {str(e)}"
            history.append((message, error_msg))
            return "", history
    
    def export_chat(self) -> str:
    """Export chat history"""
    if not self.query_engine:
        return "No chat history to export"
    
    history = self.query_engine.get_history()
    
    if not history:
        return "No chat history to export"
    
    # Build export text
    from datetime import datetime
    text = f"# Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    for i, item in enumerate(history, 1):

        timestamp = item.get('timestamp', datetime.now().strftime('%H:%M:%S'))
        
        text += f"## [{timestamp}] Q{i}\n\n"
        text += f"**Question:** {item['question']}\n\n"
        text += f"**Answer:** {item['answer']}\n\n"
        
        if item.get('sources'):
            text += "**Sources:**\n"
            for source in item['sources']:
                text += f"- {source}\n"
        
        text += "\n---\n\n"
    
    return text
    
    def clear_chat(self) -> List:
        """Clear chat history"""
        if self.query_engine:
            self.query_engine.clear_history()
        return []
    
    def create_interface(self) -> gr.Blocks:
        """Create Gradio interface"""
        
        with gr.Blocks(
            title="RAG Documentation Assistant",
            theme=gr.themes.Soft()
        ) as app:
            
            gr.Markdown(
                """
                # 🤖 RAG Documentation Assistant
                
                Ask questions about **Python**, **FastAPI**, **LangChain**, and **LlamaIndex** documentation.
                """
            )
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="Chat",
                        height=500,
                        show_copy_button=True
                    )
                    
                    msg = gr.Textbox(
                        placeholder="Ask your question here...",
                        label="Your Question",
                        lines=2
                    )
                    
                    with gr.Row():
                        send_btn = gr.Button("Send 📤", variant="primary")
                        clear_btn = gr.Button("Clear 🗑️")
                    
                    gr.Examples(
                        examples=[
                            "What is a Python decorator and how do I use it?",
                            "How do I create a FastAPI endpoint with path parameters?",
                            "Explain LangChain chains and how they work",
                            "What is the difference between VectorStoreIndex and ListIndex in LlamaIndex?"
                        ],
                        inputs=msg,
                        label="Example Questions"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 System Info")
                    
                    stats = self.indexer.get_stats() if self.indexer else {}
                    
                    gr.Markdown(
                        f"""
                        - **Status:** {'✅ Ready' if self.is_ready else '❌ Not Ready'}
                        - **Documents:** {stats.get('documents_loaded', 0)}
                        - **Model:** {config.models.llm_model}
                        - **Embeddings:** {config.models.embedding_model.split('/')[-1]}
                        """
                    )
                    
                    gr.Markdown("### 💾 Export")
                    export_btn = gr.Button("Download Chat 📥")
                    export_text = gr.Textbox(
                        label="Chat History",
                        lines=10,
                        max_lines=20
                    )
            
            # Event handlers
            msg.submit(self.chat, [msg, chatbot], [msg, chatbot])
            send_btn.click(self.chat, [msg, chatbot], [msg, chatbot])
            clear_btn.click(self.clear_chat, None, chatbot)
            export_btn.click(self.export_chat, None, export_text)
        
        return app


def main():
    """Launch the Gradio app"""
    print("Starting RAG Documentation Assistant...")
    
    try:
        app = RAGApp()
        interface = app.create_interface()
        
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False
        )
        
    except Exception as e:
        logger.error(f"Failed to start app: {e}")
        raise


if __name__ == "__main__":
    main()
