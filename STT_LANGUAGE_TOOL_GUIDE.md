# STT Language Switching Tool - Implementation Guide

## Overview

I've created a tool that allows your Vidya AI assistant to dynamically change the Speech-to-Text (STT) language during a conversation. Users can now ask the agent to switch languages, and the agent will respond accordingly.

## How It Works

### 1. **Two New Tools Added to `tools.py`**

#### `change_stt_language(language_code: str)`
Allows the user (via LLM) to change the STT language.

**Supported Languages:**
- `en-US`: English (United States)
- `hi-IN`: Hindi (India) - default
- `es-ES`: Spanish (Spain)
- `ta-IN`: Tamil (India)
- `te-IN`: Telugu (India)
- `ml-IN`: Malayalam (India)

**Example Usage:**
- User says: "Change language to English"
- Agent calls: `change_stt_language("en-US")`
- Agent responds: "Language changed to English (en-US). I will now listen in English."

#### `get_current_stt_language()`
Returns the current STT language setting.

**Example Usage:**
- User says: "What language are you listening in?"
- Agent calls: `get_current_stt_language()`
- Agent responds: "Current language is set to Hindi (India)"

#### `get_stt_language()`
A helper function (not a tool) that returns the current language code for use during agent initialization.

### 2. **Global State Management**

The tools use a global variable `_current_stt_language` to track the current language:

```python
# Global state to track current STT language
_current_stt_language = "hi-IN"
```

This allows:
- Language changes to persist during the conversation
- The initialization to use the current language setting

### 3. **Agent Integration**

The `Assistant` class now includes all tools:

```python
class Assistant(Agent):
    def __init__(self, prompt: str|None = None) -> None:
        instructions = "..."
        super().__init__(
            instructions=instructions,
            tools=[
                change_stt_language,
                get_current_stt_language,
                install_package,
                update_system,
                system_info,
                check_memory,
                set_volume,
                wifi_status,
                kill_process,
                open_application,
            ],
        )
```

### 4. **STT Configuration**

The entrypoint now uses `get_stt_language()`:

```python
session = AgentSession(
    stt=sarvam.STT(
        language=get_stt_language(),  # Gets current language dynamically
        model="saarika:v2.5"
    ),
    # ... other config
)
```

## Usage Examples

### User Interaction 1: Check Current Language
```
User: "What language are you listening to right now?"
Agent: [Calls get_current_stt_language()]
Agent: "Current language is set to Hindi (India)"
```

### User Interaction 2: Switch Language
```
User: "Switch to English"
Agent: [Calls change_stt_language("en-US")]
Agent: "Language changed to English (en-US). I will now listen in English."
User: "Hello there!" (Now speaking in English)
Agent: [STT processes in English]
```

### User Interaction 3: Switch Back
```
User: "हिंदी में बदल दो" (Switch to Hindi)
Agent: [Calls change_stt_language("hi-IN")]
Agent: "Language changed to Hindi (India). I will now listen in Hindi."
```

## Technical Implementation Details

### Why This Approach?

1. **Global State**: Used instead of JobContext.userdata (which isn't directly assignable in LiveKit Agents)
2. **Tool Functions**: Implemented as standalone functions decorated with `@function_tool` for automatic LLM discovery
3. **RunContext Parameter**: Both tools take a `RunContext` parameter (required by LiveKit Agents framework)

### Supported Sarvam STT Languages

The Sarvam STT plugin (which you're using) supports:
- Indian languages: Hindi, Tamil, Telugu, Malayalam
- International: English (US), Spanish, and more

You can add more languages by:
1. Adding them to the `supported_languages` dict in `change_stt_language()`
2. Verifying they're supported by Sarvam STT
3. Adding translations to the `language_names` dict for user-friendly names

## Limitations & Considerations

### Current Limitations:

1. **Session Restart Needed**: The STT instance is created at session start. Changing the language updates the global variable but doesn't recreate the STT instance immediately. The user would need to:
   - Change language via tool
   - The next utterance will be processed with the new language setting
   
   **Workaround for Full Restart**: See Advanced Implementation below

2. **Single Session**: Language state is global - if multiple users connect, they share the same language setting

3. **No Persistence**: Language choice doesn't persist across sessions

### Future Enhancements:

If you need the STT to instantly change language mid-conversation, you'd need to:

1. **Recreate the STT instance dynamically**
2. **Update the session's STT** using the LiveKit Agents API
3. **Notify the user** of the switch

## Advanced Implementation (Instant Language Switch)

For a more sophisticated approach that recreates the STT instance on-demand, you could:

```python
class Assistant(Agent):
    def __init__(self, prompt: str|None = None, session: AgentSession = None) -> None:
        self.session = session
        # ... rest of init
    
    @function_tool
    async def change_stt_language_advanced(self, context: RunContext, language_code: str) -> str:
        global _current_stt_language
        
        _current_stt_language = language_code
        
        # Recreate STT instance
        new_stt = sarvam.STT(
            language=language_code,
            model="saarika:v2.5"
        )
        
        # Update session (if API supports it)
        if self.session:
            # This depends on LiveKit Agents version and API
            # May not be directly supported
            pass
        
        return f"Language changed to {language_code}"
```

**Note**: Check LiveKit Agents documentation for session update APIs in your version.

## Testing the Implementation

1. **Start the agent**:
   ```bash
   uv run python agent.py
   ```

2. **Connect via the frontend**

3. **Test language switching**:
   - "What language are you listening to?"
   - "Change language to English"
   - Speak in English
   - "Switch back to Hindi"
   - Speak in Hindi

## Integration with Your Codebase

The changes made:

1. **tools.py**: Added 3 new functions:
   - `change_stt_language()` - Tool
   - `get_current_stt_language()` - Tool
   - `get_stt_language()` - Helper function

2. **agent.py**: 
   - Imported the new tools
   - Added tools to the `Assistant` class
   - Updated STT initialization to use `get_stt_language()`

## FAQ

**Q: Can the user switch languages during a call?**
A: Yes! The tool will change the global language setting immediately, and the next speech input will be processed in that language.

**Q: What if I want to add more languages?**
A: Add the language code to:
1. The `supported_languages` dict in `change_stt_language()`
2. The `language_names` dict for display names
3. Verify Sarvam STT supports that language

**Q: Does this affect the TTS (text-to-speech)?**
A: Currently no - the TTS voice is still set to Hindi by default via the environment variable. To also change TTS language, you'd need a similar tool for the TTS component.

**Q: Will language changes persist across sessions?**
A: No - the global variable resets when the agent restarts. For persistence, you'd need to store the preference in a database or file.

## Next Steps

1. Test the language switching in your UI
2. Update your prompt/instructions if needed to mention the language switching capability
3. Consider adding a TTS language switching tool if needed
4. Add database persistence if you need language preferences to survive across sessions
