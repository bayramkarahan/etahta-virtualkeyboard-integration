build:
	: run make install
install:
	mkdir -p $(DESTDIR)/usr/bin
	cp -prfv eta-chrome-osk $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/lib/etahta
	cp -prfv chrome-osk.py $(DESTDIR)/usr/lib/etahta/
	mkdir -p $(DESTDIR)/usr/lib/systemd/user
	cp -prfv eta-chrome-osk.service $(DESTDIR)/usr/lib/systemd/user/
	mkdir -p $(DESTDIR)/usr/lib/systemd/user-preset
	cp -prfv 90-eta.preset $(DESTDIR)/usr/lib/systemd/user-preset/
