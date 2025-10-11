from livekit.agents import function_tool
import subprocess

@function_tool
async def install_package(package_name: str):
    """Install a package using pacman"""
    try:
        result = subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', package_name], 
                              capture_output=True, text=True)
        return f"{package_name} install हो गया" if result.returncode == 0 else "Install में error आया"
    except Exception:
        return "Command execute नहीं हो सका"

@function_tool
async def update_system():
    """Update the entire system"""
    try:
        subprocess.run(['sudo', 'pacman', '-Syu', '--noconfirm'], check=True)
        return "System update हो गया"
    except Exception:
        return "Update में error आया"

@function_tool
async def system_info():
    """Get system information"""
    try:
        result = subprocess.run(['neofetch', '--stdout'], capture_output=True, text=True)
        return "System info ready" if result.returncode == 0 else "Info नहीं मिली"
    except Exception:
        return "Neofetch available नहीं है"

@function_tool
async def check_memory():
    """Check memory usage"""
    try:
        result = subprocess.run(['free', '-h'], capture_output=True, text=True)
        lines = result.stdout.split('\n')[1].split()
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
        subprocess.run(['amixer', 'set', 'Master', f'{level}%'], check=True)
        return f"Volume {level}% set हो गया"
    except Exception:
        return "Volume set नहीं हो सका"

@function_tool
async def wifi_status():
    """Check WiFi networks"""
    try:
        result = subprocess.run(['nmcli', 'dev', 'wifi'], capture_output=True, text=True)
        return "WiFi networks मिल गए" if result.returncode == 0 else "WiFi scan नहीं हो सका"
    except Exception:
        return "NetworkManager available नहीं है"

@function_tool
async def kill_process(process_name: str):
    """Kill a process by name"""
    try:
        subprocess.run(['killall', process_name], check=True)
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
