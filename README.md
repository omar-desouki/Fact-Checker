# 🔍 Enhanced RAG Fact Checker

An advanced AI-powered fact-checking application that leverages **Gemini 2.5 Flash** to verify the accuracy of statements with confidence scoring and detailed evidence analysis.

## ✨ Features

### 🧠 **Advanced AI Analysis**

- Powered by Google's Gemini 2.5 Flash model
- Enhanced prompting for better accuracy and context
- Adjustable thinking budget (100-5000) for different analysis depths
- Structured output with confidence scoring (1-10 scale)

### 📊 **Intelligent Verification System**

- **Verdict Types**: TRUE, FALSE, PARTIALLY TRUE, INSUFFICIENT EVIDENCE
- **Confidence Scoring**: Get reliability ratings for each fact-check
- **Evidence-Based Analysis**: Detailed explanations with reasoning
- **Context Awareness**: Additional relevant information and suggestions

### 💾 **History & Tracking**

- Automatic saving of fact-check results
- Recent history preview (last 5 entries)
- Timestamp tracking for all analyses
- JSON-based storage for easy data management

### 🎯 **User Experience**

- **Modern Web Interface**: Clean, responsive Gradio-based UI
- **Multiple Tabs**: Fact Checker, History, and About sections
- **Quick Presets**: Fast (500), Standard (1500), Deep (3000) analysis modes
- **Example Facts**: Pre-loaded examples for testing
- **Real-time Status**: Progress indicators and status updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key for Gemini

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/omar-desouki/RAG-Fact-Checker.git
   cd RAG-Fact-Checker
   ```

2. **Set up virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**

   - Open `fact-checker.py`
   - Replace the API key with your own Google API key:
     ```python
     os.environ["GOOGLE_API_KEY"] = "your-api-key-here"
     ```

5. **Run the application**

   ```bash
   python fact-checker.py
   ```

6. **Access the interface**
   - Open your browser and go to `http://localhost:7860`

## 🎮 Usage

### Basic Fact Checking

1. Enter a statement in the "Fact to Verify" text area
2. Adjust the analysis depth slider (higher = more thorough)
3. Enable "Enhanced Analysis Mode" for better accuracy
4. Click "Analyze Fact" and wait for results

### Analysis Modes

- **⚡ Quick (500)**: Fast analysis for simple, well-known facts
- **🎯 Standard (1500)**: Balanced approach for most use cases
- **🔬 Deep (3000)**: Thorough analysis for complex or controversial claims

### Example Facts to Try

- "The Great Wall of China is visible from space with the naked eye"
- "Humans only use 10% of their brain capacity"
- "Lightning never strikes the same place twice"
- "Climate change is caused by human activities"

## 📈 Advanced Features

### Enhanced Prompting

The application uses sophisticated prompting techniques that include:

- Structured analysis framework
- Confidence scoring requirements
- Evidence-based reasoning
- Contextual information integration

### History Management

- All fact-checks are automatically saved to `fact_check_history.json`
- View recent analyses in the History tab
- Clear history when needed
- Maximum of 100 stored entries for performance

### Confidence Scoring

Each analysis includes a confidence level (1-10) that indicates:

- **9-10**: Very high confidence, strong evidence
- **7-8**: High confidence, good evidence
- **5-6**: Moderate confidence, some uncertainty
- **3-4**: Low confidence, limited evidence
- **1-2**: Very low confidence, insufficient data

## 🛠️ Technical Details

### Architecture

- **Frontend**: Gradio web interface with custom CSS
- **Backend**: Python with Google GenAI SDK
- **Model**: Gemini 2.5 Flash with thinking configuration
- **Storage**: Local JSON file for history

### API Configuration

```python
config=types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_budget=budget),
    temperature=0.1,  # Low temperature for factual accuracy
    top_p=0.8,
    max_output_tokens=2048,
)
```

## 📝 File Structure

```
RAG-Fact-Checker/
├── fact-checker.py          # Main application file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── fact_check_history.json # Generated history file
└── test                    # Jupyter notebooks for testing
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Google API key for Gemini access

### Customization Options

- **Server Port**: Change `server_port` in the `main()` function
- **History Limit**: Modify the 100-entry limit in `save_fact_check_history()`
- **Analysis Depth**: Adjust min/max thinking budget values
- **UI Theme**: Customize CSS styling in `create_interface()`

## 🚦 Error Handling

The application includes comprehensive error handling for:

- Invalid API keys or network issues
- Empty input validation
- History file corruption
- Model response errors
- UI state management

## 🔮 Future Enhancements

- [ ] Integration with real web search APIs (Google Custom Search, Bing)
- [ ] Support for fact-checking images and documents
- [ ] Multi-language support
- [ ] Export history to CSV/PDF
- [ ] Batch fact-checking capabilities
- [ ] Citation and source verification
- [ ] Custom model selection (GPT-4, Claude, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Google**: For providing the Gemini 2.5 Flash model
- **Gradio**: For the excellent web interface framework

---

**Version**: 2.0 | **Last Updated**: July 2025 | **Model**: Gemini 2.5 Flash

<img width="1440" height="795" alt="Screenshot 2025-07-21 at 3 36 21 AM" src="https://github.com/user-attachments/assets/29135c3c-5a3d-4b83-828f-d491b15c645a" />

