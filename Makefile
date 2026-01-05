PREFIX ?= /usr

build:
	@echo "Nothing to build"

install:
	# python backend
	install -d $(DESTDIR)$(PREFIX)/lib/etahta
	install -m 755 chrome-osk.py \
		$(DESTDIR)$(PREFIX)/lib/etahta/chrome-osk.py

	# autostart desktop
	install -d $(DESTDIR)/etc/xdg/autostart
	install -m 644 etahta-chrome-osk.desktop \
		$(DESTDIR)/etc/xdg/autostart/etahta-chrome-osk.desktop

