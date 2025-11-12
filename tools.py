from livekit.agents import function_tool, RunContext
import subprocess

# Global state to track current STT language
_current_stt_language = "hi-IN"


@function_tool
async def change_stt_language(
    context: RunContext,
    language_code: str,
) -> str:
    """Change the speech-to-text language for the agent.

    Args:
        language_code: The language code to switch to (e.g., 'en-US', 'hi-IN', 'es-ES')

    Supported languages:
    - 'en-US': English (United States)
    - 'hi-IN': Hindi (India)
    - 'es-ES': Spanish (Spain)
    - 'ta-IN': Tamil (India)
    - 'te-IN': Telugu (India)
    - 'ml-IN': Malayalam (India)
    """
    global _current_stt_language

    supported_languages = {
        "en-US": "English",
        "hi-IN": "Hindi",
        "es-ES": "Spanish",
        "ta-IN": "Tamil",
        "te-IN": "Telugu",
        "ml-IN": "Malayalam",
    }

    if language_code not in supported_languages:
        return f"Language {language_code} is not supported. Supported languages: {', '.join(supported_languages.keys())}"

    try:
        _current_stt_language = language_code
        lang_name = supported_languages[language_code]
        return f"Language changed to {lang_name} ({language_code}). I will now listen in {lang_name}."

    except Exception as e:
        return f"Error changing language: {str(e)}"


@function_tool
async def get_current_stt_language(
    context: RunContext,
) -> str:
    """Get the current speech-to-text language setting."""
    global _current_stt_language

    try:
        language_names = {
            "en-US": "English (United States)",
            "hi-IN": "Hindi (India)",
            "es-ES": "Spanish (Spain)",
            "ta-IN": "Tamil (India)",
            "te-IN": "Telugu (India)",
            "ml-IN": "Malayalam (India)",
        }

        lang_name = language_names.get(_current_stt_language, _current_stt_language)
        return f"Current language is set to {lang_name}"
    except Exception as e:
        return f"Error getting language: {str(e)}"


def get_stt_language() -> str:
    """Get the current STT language for use in agent initialization."""
    global _current_stt_language
    return _current_stt_language


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
