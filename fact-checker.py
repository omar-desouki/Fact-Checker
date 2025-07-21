import os
import gradio as gr
import json
import datetime
from typing import Dict, List, Tuple
import requests
from urllib.parse import quote_plus
from config_template import GOOGLE_API_KEY

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

print("✅ Gemini API key set!")

from google import genai
from google.genai import types

client = genai.Client()


def search_web_sources(query: str, num_results: int = 3) -> List[Dict]:
    """
    Search for web sources to provide additional context for fact-checking.
    This is a placeholder function - in a real implementation you'd use APIs like:
    - Google Custom Search API
    - Bing Search API
    - Wikipedia API
    """
    # For demonstration, return some mock sources
    mock_sources = [
        {
            "title": f"Source about: {query[:50]}...",
            "url": f"https://example.com/source1",
            "snippet": f"Relevant information about {query}...",
        }
    ]
    return mock_sources[:num_results]


def get_enhanced_prompt(fact: str, sources: List[Dict] = None) -> str:
    """Create an enhanced prompt with context and sources."""
    base_prompt = """You are an expert fact-checker with access to reliable sources. Your task is to:

1. VERIFY the factual accuracy of the given statement
2. PROVIDE EVIDENCE from reliable sources when available
3. RATE CONFIDENCE on a scale of 1-10 (10 = completely certain)
4. EXPLAIN REASONING behind your assessment
5. SUGGEST related facts or context if relevant

Please structure your response EXACTLY as follows (without using ** for bold formatting):

Verdict: TRUE/FALSE/PARTIALLY TRUE/INSUFFICIENT EVIDENCE
Confidence: X/10
Evidence: [Detailed explanation with sources]
Context: [Additional relevant information]
Sources: [If available]

Be thorough but concise. If uncertain, clearly state limitations. Do not use markdown formatting like ** or * for bold text."""

    if sources:
        source_context = "\n\nAdditional Context Sources:\n"
        for i, source in enumerate(sources, 1):
            source_context += f"{i}. {source['title']}\n   {source['snippet']}\n   URL: {source['url']}\n"
        base_prompt += source_context

    return base_prompt + f"\n\nFact to verify: {fact}"


def get_gemini_response(msg, thinking_budget=500, use_enhanced_prompt=True):
    """Generate a response from the Gemini model.
    Args:
        msg (str): The message to send to the model.
        thinking_budget (int): The thinking budget for the model, defaults to 500.
        use_enhanced_prompt (bool): Whether to use enhanced prompting.
    Returns:
        str: The response text from the model.
    """
    if use_enhanced_prompt:
        # Get web sources for additional context (placeholder)
        sources = search_web_sources(msg, num_results=2)
        prompt = get_enhanced_prompt(msg, sources)
    else:
        prompt = (
            """You are a fact checker. Please fact-check this statement and provide evidence. 

Structure your response as:
Verdict: TRUE/FALSE/PARTIALLY TRUE/INSUFFICIENT EVIDENCE
Confidence: X/10
Evidence: [Your analysis]

Do not use markdown formatting like ** or * for bold text.

Statement to verify: """
            + msg
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=thinking_budget),
                temperature=0.1,  # Lower temperature for more factual responses
                top_p=0.8,
                max_output_tokens=2048,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


def save_fact_check_history(fact: str, result: str, confidence: str = "N/A"):
    """Save fact-check results to a local history file."""
    history_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "fact": fact,
        "result": result,
        "confidence": confidence,
    }

    try:
        # Load existing history
        try:
            with open("fact_check_history.json", "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        # Add new entry
        history.append(history_entry)

        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]

        # Save updated history
        with open("fact_check_history.json", "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")


def extract_confidence_score(response: str) -> str:
    """Extract confidence score from the response."""
    lines = response.split("\n")
    for line in lines:
        if "**confidence**:" in line.lower() and "/10" in line:
            # Extract just the score part, e.g., "8/10"
            parts = line.split(":")
            if len(parts) > 1:
                score_part = parts[1].strip()
                # Remove any markdown formatting
                score_part = score_part.replace("*", "").strip()
                return score_part
    return "N/A"


def clean_response_formatting(response: str) -> str:
    """Clean up the response formatting for better display."""
    # Replace markdown bold with HTML bold for better Gradio display
    cleaned = response.replace("**", "")

    # Fix common formatting issues
    lines = cleaned.split("\n")
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("Verdict:"):
            formatted_lines.append(f"🔍 {line}")
        elif line.startswith("Confidence:"):
            formatted_lines.append(f"📊 {line}")
        elif line.startswith("Evidence:"):
            formatted_lines.append(f"📋 {line}")
        elif line.startswith("Context:"):
            formatted_lines.append(f"🔗 {line}")
        elif line.startswith("Sources:"):
            formatted_lines.append(f"📚 {line}")
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)


def fact_check(fact_text, thinking_budget, use_enhanced_mode, save_history):
    """
    Fact check the provided text using Gemini AI.

    Args:
        fact_text (str): The fact to be checked
        thinking_budget (int): The thinking budget for the AI model
        use_enhanced_mode (bool): Whether to use enhanced prompting
        save_history (bool): Whether to save to history

    Returns:
        Tuple[str, str]: The fact-check result and status message
    """
    if not fact_text.strip():
        return "⚠️ Please enter a fact to check.", "❌ No input provided"

    try:
        # Add timestamp to response
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = get_gemini_response(
            fact_text.strip(),
            int(thinking_budget),
            use_enhanced_prompt=use_enhanced_mode,
        )

        # Clean and format the response
        cleaned_response = clean_response_formatting(response)

        # Extract confidence score (after cleaning)
        confidence = extract_confidence_score(response)

        # Save to history if requested
        if save_history:
            save_fact_check_history(fact_text.strip(), response, confidence)

        # Format final response with metadata
        formatted_response = f"""🕒 Analysis completed at: {timestamp}
📊 Confidence Level: {confidence}

{cleaned_response}

---
💾 Saved to history: {'Yes' if save_history else 'No'}
"""

        return formatted_response, "✅ Fact-check completed successfully"

    except Exception as e:
        error_msg = f"❌ Error occurred: {str(e)}"
        return error_msg, "❌ Analysis failed"


def load_history_preview() -> str:
    """Load and display recent fact-check history."""
    try:
        with open("fact_check_history.json", "r") as f:
            history = json.load(f)

        if not history:
            return "📝 No fact-check history found."

        # Show last 5 entries
        recent_entries = history[-5:]
        preview = "📚 **Recent Fact-Checks:**\n\n"

        for i, entry in enumerate(reversed(recent_entries), 1):
            timestamp = entry["timestamp"][:19].replace("T", " ")
            fact = (
                entry["fact"][:100] + "..."
                if len(entry["fact"]) > 100
                else entry["fact"]
            )
            confidence = entry.get("confidence", "N/A")

            preview += f"**{i}.** {timestamp}\n"
            preview += f"   📝 *{fact}*\n"
            preview += f"   📊 Confidence: {confidence}\n\n"

        return preview

    except FileNotFoundError:
        return "📝 No fact-check history found."
    except Exception as e:
        return f"❌ Error loading history: {str(e)}"


# Create Gradio interface
def create_interface():
    """Create and configure the enhanced Gradio interface."""

    with gr.Blocks(
        title="Enhanced RAG Fact Checker",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .title {
            text-align: center;
            font-size: 2.8em;
            font-weight: bold;
            background: linear-gradient(45deg, #2E8B57, #4169E1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        .status-box {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        """,
    ) as interface:

        # Title
        gr.HTML('<div class="title">🔍 Enhanced RAG Fact Checker</div>')

        gr.Markdown(
            """
        ### 🚀 Advanced AI-Powered Fact Verification System
        **Powered by Gemini 2.5 Flash** | Enhanced with contextual analysis and confidence scoring
        """
        )

        with gr.Tabs():
            # Main Fact Checking Tab
            with gr.Tab("🔍 Fact Checker", elem_id="main-tab"):
                with gr.Row():
                    with gr.Column(scale=2):
                        # Input for fact to check
                        fact_input = gr.Textbox(
                            label="📝 Fact to Verify",
                            placeholder="Enter the statement you want to fact-check...\n\nExample: 'The human brain uses only 10% of its capacity'",
                            lines=5,
                            max_lines=15,
                        )

                        with gr.Row():
                            # Enhanced mode toggle
                            enhanced_mode = gr.Checkbox(
                                label="🧠 Enhanced Analysis Mode",
                                value=True,
                                info="Uses advanced prompting for better analysis",
                            )

                            # Save history toggle
                            save_history = gr.Checkbox(
                                label="💾 Save to History",
                                value=True,
                                info="Save fact-check results for future reference",
                            )

                    with gr.Column(scale=1):
                        # Thinking budget control
                        budget_input = gr.Slider(
                            minimum=100,
                            maximum=5000,
                            value=1500,
                            step=100,
                            label="🧠 Analysis Depth",
                            info="Higher values = more thorough analysis",
                        )

                        # Quick presets
                        gr.Markdown("**Quick Settings:**")
                        quick_light = gr.Button("⚡ Quick (500)", size="sm")
                        quick_standard = gr.Button("🎯 Standard (1500)", size="sm")
                        quick_deep = gr.Button("🔬 Deep (3000)", size="sm")

                # Submit button
                submit_btn = gr.Button(
                    "🔍 Analyze Fact", variant="primary", size="lg", scale=1
                )

                # Status display
                status_output = gr.HTML(label="Status")

                # Output area
                result_output = gr.Textbox(
                    label="📋 Analysis Results",
                    lines=20,
                    max_lines=30,
                    interactive=False,
                    show_copy_button=True,
                )

                # Control buttons
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear All", variant="secondary")
                    refresh_btn = gr.Button("🔄 Refresh", variant="secondary")

            # History Tab
            with gr.Tab("📚 History", elem_id="history-tab"):
                history_output = gr.Markdown(label="Recent Fact-Checks")
                refresh_history_btn = gr.Button("🔄 Refresh History")
                clear_history_btn = gr.Button("🗑️ Clear History", variant="stop")

            # About Tab
            with gr.Tab("ℹ️ About", elem_id="about-tab"):
                gr.Markdown(
                    """
                ## 🔍 Enhanced RAG Fact Checker
                
                ### Features:
                - **🧠 Advanced AI Analysis**: Powered by Gemini 2.5 Flash with enhanced prompting
                - **📊 Confidence Scoring**: Get reliability ratings for each fact-check
                - **💾 History Tracking**: Automatic saving of fact-check results
                - **🎯 Flexible Analysis**: Adjustable thinking budget for different analysis depths
                - **🌐 Web Context**: Enhanced prompting with contextual information
                
                ### How to Use:
                1. **Enter your fact** in the text area
                2. **Choose analysis depth** with the thinking budget slider
                3. **Enable enhanced mode** for better accuracy
                4. **Click "Analyze Fact"** and wait for results
                5. **Review the verdict** with confidence score and evidence
                
                ### Analysis Modes:
                - **⚡ Quick (500)**: Fast analysis for simple facts
                - **🎯 Standard (1500)**: Balanced speed and accuracy
                - **🔬 Deep (3000)**: Thorough analysis for complex claims
                
                ### Verdict Types:
                - **✅ TRUE**: Statement is factually correct
                - **❌ FALSE**: Statement is factually incorrect
                - **⚠️ PARTIALLY TRUE**: Statement has both correct and incorrect elements
                - **❓ INSUFFICIENT EVIDENCE**: Cannot determine accuracy with available information
                
                ---
                **Version**: 2.0 | **Model**: Gemini 2.5 Flash | **Updated**: July 2025
                """
                )

        # Event Handlers
        def update_status(message, is_error=False):
            css_class = "error" if is_error else "success"
            return f'<div class="status-box {css_class}">{message}</div>'

        # Quick preset buttons
        quick_light.click(lambda: 500, outputs=budget_input)
        quick_standard.click(lambda: 1500, outputs=budget_input)
        quick_deep.click(lambda: 3000, outputs=budget_input)

        # Main fact-check function
        def handle_fact_check(fact_text, thinking_budget, enhanced_mode, save_history):
            result, status = fact_check(
                fact_text, thinking_budget, enhanced_mode, save_history
            )
            status_html = update_status(status, "Error" in status)
            return result, status_html

        # Submit handlers
        submit_btn.click(
            fn=handle_fact_check,
            inputs=[fact_input, budget_input, enhanced_mode, save_history],
            outputs=[result_output, status_output],
            show_progress=True,
        )

        fact_input.submit(
            fn=handle_fact_check,
            inputs=[fact_input, budget_input, enhanced_mode, save_history],
            outputs=[result_output, status_output],
            show_progress=True,
        )

        # Clear function
        def clear_all():
            return "", "", update_status("Interface cleared")

        clear_btn.click(
            fn=clear_all, outputs=[fact_input, result_output, status_output]
        )

        # History handlers
        refresh_history_btn.click(fn=load_history_preview, outputs=history_output)

        def clear_history():
            try:
                if os.path.exists("fact_check_history.json"):
                    os.remove("fact_check_history.json")
                return "✅ History cleared successfully"
            except Exception as e:
                return f"❌ Error clearing history: {str(e)}"

        clear_history_btn.click(fn=clear_history, outputs=history_output)

        # Load initial history
        interface.load(fn=load_history_preview, outputs=history_output)

        # Enhanced Examples
        gr.Examples(
            examples=[
                [
                    "The Great Wall of China is visible from space with the naked eye",
                    1500,
                    True,
                    True,
                ],
                ["Humans only use 10% of their brain capacity", 2000, True, True],
                ["Lightning never strikes the same place twice", 1200, True, False],
                ["Goldfish have a 3-second memory span", 1000, True, False],
                ["The Earth is flat", 800, False, False],
                ["Vaccines cause autism", 2500, True, True],
                ["Climate change is caused by human activities", 2000, True, True],
            ],
            inputs=[fact_input, budget_input, enhanced_mode, save_history],
            outputs=[result_output, status_output],
            fn=handle_fact_check,
            cache_examples=False,
            label="📎 Example Facts to Check",
        )

    return interface


def main():
    """Launch the enhanced Gradio interface."""
    print("🚀 Starting Enhanced RAG Fact Checker...")
    print("📊 Features: Advanced prompting, confidence scoring, history tracking")
    print("🌐 Access: http://localhost:7860")

    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,  # Default Gradio port
        share=False,  # Set to True for public sharing
        debug=False,  # Disable debug for production
        show_error=True,  # Show errors in UI
        favicon_path=None,  # You can add a custom favicon
        app_kwargs={"docs_url": "/docs"},  # Enable API docs
    )


if __name__ == "__main__":
    main()
