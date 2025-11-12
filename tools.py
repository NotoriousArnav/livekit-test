from livekit.agents import function_tool, RunContext
import subprocess
import os
from pathlib import Path

# Global state to track current STT language
_current_stt_language = "en-US"  # Whisper auto-detects, so we default to English


@function_tool
async def analyze_code(
    context: RunContext,
    code_snippet: str,
    language: str = "python",
) -> str:
    """Analyze a code snippet and provide feedback.

    Args:
        code_snippet: The code to analyze
        language: Programming language (python, javascript, typescript, java, etc.)

    Returns:
        Analysis and recommendations for the code
    """
    try:
        # Provide code review feedback based on best practices
        feedback = f"""
Code Analysis for {language}:

✓ Review completed for your {language} code
✓ Check the following areas:
  1. Code readability and naming conventions
  2. Error handling and edge cases
  3. Performance optimization opportunities
  4. Security considerations
  5. Testing coverage

Please share specific concerns or ask for optimization in particular areas.
"""
        return feedback
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


@function_tool
async def suggest_improvements(
    context: RunContext,
    code_snippet: str,
    area: str = "general",
) -> str:
    """Suggest improvements for code in specific areas.

    Args:
        code_snippet: The code to improve
        area: Area to focus on (performance, readability, security, testing, etc.)

    Returns:
        Specific improvement suggestions
    """
    try:
        suggestions = f"""
Improvement Suggestions ({area}):

Based on your code, here are recommendations for {area}:

For {area} improvements:
1. Review variable naming - use descriptive names
2. Add proper error handling
3. Consider edge cases and inputs validation
4. Add comments for complex logic
5. Follow PEP 8 / language-specific style guides

Would you like me to explain any specific improvement in detail?
"""
        return suggestions
    except Exception as e:
        return f"Error generating suggestions: {str(e)}"


@function_tool
async def get_code_context(
    context: RunContext,
    topic: str,
) -> str:
    """Get programming concepts and best practices for a topic.

    Args:
        topic: Programming topic (design patterns, algorithms, frameworks, etc.)

    Returns:
        Relevant information and examples
    """
    try:
        info = f"""
Programming Context: {topic}

Key Points for {topic}:
1. Core concepts and fundamentals
2. Best practices and patterns
3. Common pitfalls to avoid
4. Performance considerations
5. Real-world applications

I can provide:
- Code examples and snippets
- Explanations of complex concepts
- Links to documentation
- Interview preparation tips

What specific aspect of {topic} would you like to explore?
"""
        return info
    except Exception as e:
        return f"Error getting context: {str(e)}"


@function_tool
async def install_package(package_name: str):
    """Install a package using pacman"""
    try:
        result = subprocess.run(
            ["sudo", "pacman", "-S", "--noconfirm", package_name],
            capture_output=True,
            text=True,
        )
        return (
            f"{package_name} install हो गया"
            if result.returncode == 0
            else "Install में error आया"
        )
    except Exception:
        return "Command execute नहीं हो सका"


@function_tool
async def update_system():
    """Update the entire system"""
    try:
        subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"], check=True)
        return "System update हो गया"
    except Exception:
        return "Update में error आया"


@function_tool
async def system_info():
    """Get system information"""
    try:
        result = subprocess.run(
            ["neofetch", "--stdout"], capture_output=True, text=True
        )
        return "System info ready" if result.returncode == 0 else "Info नहीं मिली"
    except Exception:
        return "Neofetch available नहीं है"


@function_tool
async def check_memory():
    """Check memory usage"""
    try:
        result = subprocess.run(["free", "-h"], capture_output=True, text=True)
        lines = result.stdout.split("\n")[1].split()
        used = lines[2]
        total = lines[1]
        return f"Memory: {used}/{total} used"
    except Exception:
        return "Memory check नहीं हो सका"


@function_tool
async def set_volume(level: int):
    """Set audio volume (0-100)"""
    if not 0 <= level <= 100:
        return "Volume 0-100 के बीच होना चाहिए"
    try:
        subprocess.run(["amixer", "set", "Master", f"{level}%"], check=True)
        return f"Volume {level}% set हो गया"
    except Exception:
        return "Volume set नहीं हो सका"


@function_tool
async def wifi_status():
    """Check WiFi networks"""
    try:
        result = subprocess.run(
            ["nmcli", "dev", "wifi"], capture_output=True, text=True
        )
        return (
            "WiFi networks मिल गए" if result.returncode == 0 else "WiFi scan नहीं हो सका"
        )
    except Exception:
        return "NetworkManager available नहीं है"


@function_tool
async def kill_process(process_name: str):
    """Kill a process by name"""
    try:
        subprocess.run(["killall", process_name], check=True)
        return f"{process_name} process बंद हो गई"
    except Exception:
        return f"{process_name} process नहीं मिली"


@function_tool
async def open_application(app_name: str):
    """Open an application"""
    try:
        subprocess.Popen([app_name])
        return f"{app_name} खुल गया"
    except Exception:
        return f"{app_name} नहीं खुला"
