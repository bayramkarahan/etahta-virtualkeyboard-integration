PREFIX ?= /usr

build:
	@echo "Nothing to build"

install:
	# binaries
	# python backend ve wrapper
	install -d $(DESTDIR)$(PREFIX)/lib/etahta
	install -m 755 chrome-osk.py \
		$(DESTDIR)$(PREFIX)/lib/etahta/chrome-osk.py

	# systemd user service
	install -d $(DESTDIR)/etc/xdg/autostart
	install -m 755 etahta-chrome-osk.desktop \
		$(DESTDIR)/etc/xdg/autostart/etahta-chrome-osk.desktop

