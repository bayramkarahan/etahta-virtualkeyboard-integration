PREFIX ?= /usr

build:
	@echo "Nothing to build"

install:
	# binaries
	# python backend ve wrapper
	install -d $(DESTDIR)$(PREFIX)/lib/etahta
	install -m 755 chrome-osk.py \
		$(DESTDIR)$(PREFIX)/lib/etahta/chrome-osk.py
		
	install -m 755 chrome-osk-wrapper.sh \
		$(DESTDIR)$(PREFIX)/lib/etahta/chrome-osk-wrapper.sh
    

	# systemd user service
	install -d $(DESTDIR)$(PREFIX)/lib/systemd/user
	install -m 644 etahta-chrome-osk.service \
		$(DESTDIR)$(PREFIX)/lib/systemd/user/etahta-chrome-osk.service

	# systemd user preset
	install -d $(DESTDIR)$(PREFIX)/lib/systemd/user-preset
	install -m 644 90-etahta.preset \
		$(DESTDIR)$(PREFIX)/lib/systemd/user-preset/90-etahta.preset

