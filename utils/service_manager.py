import subprocess
import shutil

# --- CONFIGURATION ---
# A list of services that are installed but should not be running on boot.
SERVICES_TO_DISABLE = [
    "apache2",
    "mysql",
]

def disable_startup_services():
    """
    Stops and disables a list of systemd services to prevent them from running on boot.
    """
    print("\n--- Disabling Startup Services ---")

    if not shutil.which('systemctl'):
        print("'systemctl' not found. Skipping service management.")
        return

    for service in SERVICES_TO_DISABLE:
        print(f"\nProcessing service: {service}")
        try:
            # Check if the service is active before trying to stop it
            is_active_cmd = ["systemctl", "is-active", "--quiet", service]
            is_active = subprocess.run(is_active_cmd).returncode == 0

            if is_active:
                print(f"Stopping '{service}'...")
                stop_command = ["sudo", "systemctl", "stop", service]
                subprocess.run(stop_command, check=True, capture_output=True, text=True)
            else:
                print(f"Service '{service}' is already stopped.")

            # Disable the service from starting on boot
            print(f"Disabling '{service}' from starting on boot...")
            disable_command = ["sudo", "systemctl", "disable", service]
            subprocess.run(disable_command, check=True, capture_output=True, text=True)
            print(f"'{service}' is now stopped and disabled.")

        except subprocess.CalledProcessError as e:
            error_message = e.stderr
            if "does not exist" in error_message or "not found" in error_message:
                print(f"Service '{service}' does not appear to be installed. Skipping.")
            else:
                print(f"An error occurred while managing '{service}': {error_message.strip()}")
        except Exception as e:
            print(f"\nAn unexpected error occurred while processing '{service}': {e}")

if __name__ == "__main__":
    disable_startup_services()