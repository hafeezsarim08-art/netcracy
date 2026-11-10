# ============================================================================
#               NETCRACY: SYSTEM DEPLOYMENT AUTOMATION MATRIX
# ============================================================================

# Default target rule executed when typing 'make' alone
all: install

install:
	@echo "[*] Granting system-wide execution permissions to core scripts..."
	chmod +x netcracy.py 2>/dev/null || true
	
	@echo "[*] Binding permanent global 'sudo netcracy' execution link..."
	sudo ln -sf /home/kali/netcracy/netcracy.py /usr/bin/netcracy
	
	@echo "[*] Flushing shell path memory caches..."
	hash -r
	@echo "[+] Netcracy installation matrix completed successfully!"

sync:
	@echo "[*] Synchronizing local repository workspace with tablet GitHub commits..."
	git pull origin main
	
	@echo "[*] Re-applying execution permissions and system links..."
	chmod +x *.py 2>/dev/null || true
	sudo ln -sf /home/kali/netcracy/netcracy.py /usr/bin/netcracy
	hash -r
	@echo "[+] Workspace fully synchronized and optimized!"

clean:
	@echo "[*] Purging global binary execution shortcuts..."
	sudo rm -f /usr/bin/netcracy
	
	@echo "[*] Flushing background process caches and stray worker threads..."
	sudo pkill -f netcracy.py || true
	@echo "[+] System sanitized cleanly back to standard baseline."

.PHONY: all install sync clean
